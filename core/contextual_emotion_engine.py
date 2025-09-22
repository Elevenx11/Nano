# contextual_emotion_engine.py - محرك المشاعر السياقي الذكي
import json
import re
import math
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import pickle
import os

@dataclass
class EmotionContext:
    """سياق المشاعر"""
    text: str
    emotion: str
    intensity: float
    context_features: Dict[str, float]
    timestamp: datetime
    confidence: float

@dataclass
class ConversationPattern:
    """نمط المحادثة"""
    pattern_type: str
    triggers: List[str]
    typical_response: str
    emotion_shift: Dict[str, float]
    confidence_score: float

class ContextualEmotionEngine:
    """محرك المشاعر السياقي - يتعلم من التفاعلات"""
    
    def __init__(self, learning_data_path: str = "data/emotion_learning.pkl"):
        self.learning_data_path = learning_data_path
        
        # الأنواع الأساسية للمشاعر
        self.emotion_types = [
            "سعادة", "حزن", "غضب", "حب", "ثقة", "خوف", 
            "دهشة", "احترام", "ازدراء", "فخر", "خيبة أمل", "حماس"
        ]
        
        # تاريخ المحادثات للتعلم
        self.conversation_history = deque(maxlen=100)
        self.emotion_patterns = {}
        self.contextual_features = {}
        
        # نماذج التعلم
        self.situation_emotion_map = defaultdict(lambda: defaultdict(float))
        self.context_weights = defaultdict(float)
        self.learned_patterns = []
        
        # إحصائيات التعلم
        self.learning_stats = {
            "total_conversations": 0,
            "emotion_accuracy": 0.0,
            "pattern_confidence": 0.0,
            "last_updated": datetime.now()
        }
        
        self.load_learning_data()
        self.initialize_context_analyzers()

    def initialize_context_analyzers(self):
        """تهيئة محللات السياق"""
        
        # محلل النبرة
        self.tone_patterns = {
            "aggressive": {
                "indicators": ["!", "كل", "روح", "اسكت", "ما تفهم"],
                "punctuation_weight": 0.3,
                "caps_weight": 0.2
            },
            "sarcastic": {
                "indicators": ["طبعاً", "ما شاء الله", "كفو", "عجيب"],
                "context_dependent": True,
                "timing_sensitive": True
            },
            "affectionate": {
                "indicators": ["حبيبي", "عزيزي", "يا قلبي", "روحي"],
                "relationship_dependent": True
            },
            "dismissive": {
                "indicators": ["طيب", "ماشي", "كما تشاء", "عادي"],
                "repetition_sensitive": True
            }
        }
        
        # محلل السياق الاجتماعي  
        self.social_contexts = {
            "congratulations": {
                "triggers": ["مبروك", "تهانينا", "فرحان", "نجح"],
                "expected_emotion": "سعادة",
                "response_type": "positive_reinforcement"
            },
            "complaint": {
                "triggers": ["مشكلة", "متضايق", "زعلان", "تعبان"],
                "expected_emotion": "حزن",
                "response_type": "empathy"
            },
            "achievement": {
                "triggers": ["حققت", "وصلت", "كسبت", "فزت"],
                "expected_emotion": "فخر",
                "response_type": "celebration"
            },
            "disappointment": {
                "triggers": ["خيبة أمل", "فشلت", "ما نجح", "خسرت"],
                "expected_emotion": "خيبة أمل", 
                "response_type": "consolation"
            }
        }

    def extract_context_features(self, text: str, conversation_context: List[str] = None) -> Dict[str, float]:
        """استخراج خصائص السياق من النص"""
        features = {}
        text_lower = text.lower().strip()
        
        # 1. تحليل الكلمات والعبارات
        words = text_lower.split()
        features["word_count"] = len(words)
        features["avg_word_length"] = sum(len(w) for w in words) / len(words) if words else 0
        
        # 2. تحليل علامات الترقيم والتأكيد
        features["exclamation_marks"] = text.count("!")
        features["question_marks"] = text.count("?") + text.count("؟")
        features["caps_ratio"] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        # 3. تحليل التكرار
        if conversation_context:
            features["repetition_score"] = self.calculate_repetition_score(text, conversation_context)
        else:
            features["repetition_score"] = 0.0
        
        # 4. تحليل النبرة
        tone_scores = self.analyze_tone_patterns(text_lower)
        features.update(tone_scores)
        
        # 5. تحليل السياق الاجتماعي
        social_scores = self.analyze_social_context(text_lower)
        features.update(social_scores)
        
        # 6. تحليل العاطفة الضمنية
        implicit_scores = self.analyze_implicit_emotion(text_lower)
        features.update(implicit_scores)
        
        return features

    def analyze_tone_patterns(self, text: str) -> Dict[str, float]:
        """تحليل أنماط النبرة"""
        tone_scores = {}
        
        for tone, pattern in self.tone_patterns.items():
            score = 0.0
            
            # فحص المؤشرات المباشرة
            for indicator in pattern["indicators"]:
                if indicator in text:
                    score += 0.3
            
            # وزن علامات الترقيم
            if "punctuation_weight" in pattern:
                punct_count = text.count("!") + text.count("؟")
                score += punct_count * pattern["punctuation_weight"]
            
            # تطبيع النتيجة
            tone_scores[f"tone_{tone}"] = min(1.0, score)
        
        return tone_scores

    def analyze_social_context(self, text: str) -> Dict[str, float]:
        """تحليل السياق الاجتماعي"""
        social_scores = {}
        
        for context, data in self.social_contexts.items():
            score = 0.0
            
            for trigger in data["triggers"]:
                if trigger in text:
                    score += 0.4
            
            social_scores[f"social_{context}"] = min(1.0, score)
        
        return social_scores

    def analyze_implicit_emotion(self, text: str) -> Dict[str, float]:
        """تحليل المشاعر الضمنية"""
        implicit_scores = {}
        
        # تحليل أنماط الرفض الضمني
        dismissive_patterns = ["طيب", "ماشي", "كما تشاء", "عادي"]
        dismissive_score = sum(1 for p in dismissive_patterns if p in text) * 0.3
        implicit_scores["implicit_dismissive"] = min(1.0, dismissive_score)
        
        # تحليل أنماط الحماس الضمني
        enthusiasm_patterns = ["والله", "ما شاء الله", "يلا", "هيا"]
        enthusiasm_score = sum(1 for p in enthusiasm_patterns if p in text) * 0.3
        implicit_scores["implicit_enthusiasm"] = min(1.0, enthusiasm_score)
        
        # تحليل أنماط التردد
        hesitation_patterns = ["ما أدري", "ممكن", "يمكن", "مو متأكد"]
        hesitation_score = sum(1 for p in hesitation_patterns if p in text) * 0.3
        implicit_scores["implicit_hesitation"] = min(1.0, hesitation_score)
        
        return implicit_scores

    def calculate_repetition_score(self, text: str, context: List[str]) -> float:
        """حساب درجة التكرار"""
        if not context:
            return 0.0
        
        # فحص التكرار في آخر 3 رسائل
        recent_context = context[-3:] if len(context) > 3 else context
        similarity_scores = []
        
        for prev_text in recent_context:
            # حساب التشابه البسيط
            words1 = set(text.lower().split())
            words2 = set(prev_text.lower().split())
            
            if len(words1.union(words2)) > 0:
                similarity = len(words1.intersection(words2)) / len(words1.union(words2))
                similarity_scores.append(similarity)
        
        return max(similarity_scores) if similarity_scores else 0.0

    def predict_emotion_contextual(self, text: str, conversation_context: List[str] = None) -> Tuple[str, float, Dict]:
        """توقع المشاعر بناءً على السياق الكامل"""
        
        # استخراج خصائص السياق
        features = self.extract_context_features(text, conversation_context)
        
        # حساب احتماليات المشاعر
        emotion_probabilities = {}
        
        for emotion in self.emotion_types:
            prob = self.calculate_emotion_probability(emotion, features)
            emotion_probabilities[emotion] = prob
        
        # اختيار أقوى مشاعر
        predicted_emotion = max(emotion_probabilities.keys(), 
                              key=lambda k: emotion_probabilities[k])
        
        confidence = emotion_probabilities[predicted_emotion]
        
        # إضافة تفاصيل التحليل
        analysis_details = {
            "features": features,
            "emotion_probabilities": emotion_probabilities,
            "context_factors": self.analyze_context_factors(features)
        }
        
        return predicted_emotion, confidence, analysis_details

    def calculate_emotion_probability(self, emotion: str, features: Dict[str, float]) -> float:
        """حساب احتمالية مشاعر معينة بناءً على الخصائص"""
        
        # الأوزان المتعلمة للخصائص المختلفة
        if emotion not in self.situation_emotion_map:
            # إذا لم نتعلم عن هذه المشاعر بعد، نستخدم القيم الافتراضية
            return self.calculate_default_emotion_probability(emotion, features)
        
        emotion_weights = self.situation_emotion_map[emotion]
        probability = 0.0
        
        for feature, value in features.items():
            if feature in emotion_weights:
                probability += value * emotion_weights[feature]
        
        # تطبيع القيمة بين 0 و 1
        return max(0.0, min(1.0, probability))

    def calculate_default_emotion_probability(self, emotion: str, features: Dict[str, float]) -> float:
        """حساب احتمالية افتراضية للمشاعر الجديدة"""
        
        # قواعد افتراضية بسيطة
        defaults = {
            "سعادة": ["social_congratulations", "social_achievement", "tone_affectionate"],
            "حزن": ["social_complaint", "social_disappointment"],
            "غضب": ["tone_aggressive", "exclamation_marks"],
            "ازدراء": ["tone_sarcastic", "tone_dismissive"],
            "حماس": ["implicit_enthusiasm", "exclamation_marks"],
            "خيبة أمل": ["social_disappointment", "implicit_hesitation"]
        }
        
        if emotion not in defaults:
            return 0.1  # احتمالية منخفضة للمشاعر غير المعروفة
        
        relevant_features = defaults[emotion]
        score = sum(features.get(feature, 0) for feature in relevant_features)
        
        return min(1.0, score / len(relevant_features)) if relevant_features else 0.1

    def analyze_context_factors(self, features: Dict[str, float]) -> Dict[str, str]:
        """تحليل العوامل المؤثرة في السياق"""
        factors = {}
        
        # تحديد العامل المهيمن
        if features.get("tone_aggressive", 0) > 0.5:
            factors["dominant_tone"] = "عدواني"
        elif features.get("tone_sarcastic", 0) > 0.5:
            factors["dominant_tone"] = "ساخر"
        elif features.get("tone_affectionate", 0) > 0.5:
            factors["dominant_tone"] = "حنون"
        else:
            factors["dominant_tone"] = "محايد"
        
        # تحديد السياق الاجتماعي
        social_scores = {k: v for k, v in features.items() if k.startswith("social_")}
        if social_scores:
            dominant_social = max(social_scores.keys(), key=lambda k: social_scores[k])
            factors["social_context"] = dominant_social.replace("social_", "")
        
        # تحديد مستوى التفاعل
        interaction_level = features.get("exclamation_marks", 0) + features.get("question_marks", 0)
        if interaction_level > 2:
            factors["interaction_level"] = "عالي"
        elif interaction_level > 0:
            factors["interaction_level"] = "متوسط"
        else:
            factors["interaction_level"] = "منخفض"
        
        return factors

    def learn_from_interaction(self, user_input: str, predicted_emotion: str, 
                              actual_response_type: str, feedback_score: float = 0.5):
        """التعلم من التفاعل"""
        
        # استخراج خصائص هذا التفاعل
        features = self.extract_context_features(user_input, 
                                               [item['user_input'] for item in self.conversation_history])
        
        # إنشاء سياق المشاعر
        emotion_context = EmotionContext(
            text=user_input,
            emotion=predicted_emotion,
            intensity=feedback_score,
            context_features=features,
            timestamp=datetime.now(),
            confidence=feedback_score
        )
        
        # إضافة للتاريخ
        self.conversation_history.append({
            'user_input': user_input,
            'predicted_emotion': predicted_emotion,
            'response_type': actual_response_type,
            'feedback_score': feedback_score,
            'timestamp': datetime.now(),
            'features': features
        })
        
        # تحديث النماذج المتعلمة
        self.update_emotion_weights(predicted_emotion, features, feedback_score)
        
        # تحديث الإحصائيات
        self.update_learning_stats()

    def update_emotion_weights(self, emotion: str, features: Dict[str, float], feedback_score: float):
        """تحديث أوزان المشاعر بناءً على التغذية الراجعة"""
        
        learning_rate = 0.1  # معدل التعلم
        
        # تحديث الأوزان للمشاعر المتوقعة
        for feature, value in features.items():
            if value > 0:  # فقط الخصائص الموجودة
                # زيادة الوزن إذا كان التوقع صحيحاً، تقليله إذا كان خاطئاً
                adjustment = learning_rate * feedback_score * value
                self.situation_emotion_map[emotion][feature] += adjustment
                
                # الحد من النمو المفرط
                self.situation_emotion_map[emotion][feature] = max(-1.0, 
                    min(1.0, self.situation_emotion_map[emotion][feature]))

    def update_learning_stats(self):
        """تحديث إحصائيات التعلم"""
        self.learning_stats["total_conversations"] += 1
        self.learning_stats["last_updated"] = datetime.now()
        
        # حساب دقة التوقع من آخر 20 محادثة
        if len(self.conversation_history) >= 20:
            recent_feedback = [item['feedback_score'] for item in list(self.conversation_history)[-20:]]
            self.learning_stats["emotion_accuracy"] = sum(recent_feedback) / len(recent_feedback)

    def get_contextual_response_suggestion(self, predicted_emotion: str, 
                                         context_factors: Dict[str, str]) -> str:
        """اقتراح نوع الرد المناسب للسياق"""
        
        response_mapping = {
            ("سعادة", "congratulations"): "celebration",
            ("حزن", "complaint"): "empathy", 
            ("غضب", "عدواني"): "calming",
            ("ازدراء", "ساخر"): "playful_deflection",
            ("حماس", "عالي"): "matching_energy",
            ("خيبة أمل", "disappointment"): "encouragement"
        }
        
        # البحث عن تطابق في السياق
        social_context = context_factors.get("social_context", "")
        dominant_tone = context_factors.get("dominant_tone", "")
        
        # محاولة العثور على تطابق مباشر
        for (emotion, context), response_type in response_mapping.items():
            if predicted_emotion == emotion and (context in social_context or context in dominant_tone):
                return response_type
        
        # fallback للمشاعر الأساسية
        emotion_defaults = {
            "سعادة": "positive_reinforcement",
            "حزن": "empathy",
            "غضب": "calming",
            "حب": "affectionate",
            "ازدراء": "respectful_distance",
            "حماس": "matching_energy"
        }
        
        return emotion_defaults.get(predicted_emotion, "neutral_friendly")

    def save_learning_data(self):
        """حفظ بيانات التعلم"""
        data = {
            'situation_emotion_map': dict(self.situation_emotion_map),
            'context_weights': dict(self.context_weights),
            'learning_stats': self.learning_stats,
            'conversation_history': list(self.conversation_history)
        }
        
        os.makedirs(os.path.dirname(self.learning_data_path), exist_ok=True)
        
        with open(self.learning_data_path, 'wb') as f:
            pickle.dump(data, f)

    def load_learning_data(self):
        """تحميل بيانات التعلم المحفوظة"""
        if os.path.exists(self.learning_data_path):
            try:
                with open(self.learning_data_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.situation_emotion_map = defaultdict(lambda: defaultdict(float), data.get('situation_emotion_map', {}))
                self.context_weights = defaultdict(float, data.get('context_weights', {}))
                self.learning_stats = data.get('learning_stats', self.learning_stats)
                
                # استعادة تاريخ المحادثة
                history_data = data.get('conversation_history', [])
                self.conversation_history = deque(history_data[-100:], maxlen=100)  # آخر 100 محادثة
                
            except Exception as e:
                print(f"خطأ في تحميل بيانات التعلم: {e}")
                # تهيئة بيانات فارغة في حالة الخطأ
                self.situation_emotion_map = defaultdict(lambda: defaultdict(float))
                self.context_weights = defaultdict(float)

    def get_learning_insights(self) -> Dict:
        """الحصول على إحصائيات التعلم"""
        insights = {
            "total_interactions": len(self.conversation_history),
            "emotion_accuracy": self.learning_stats.get("emotion_accuracy", 0.0),
            "most_common_emotions": self.get_most_common_emotions(),
            "learning_progress": self.calculate_learning_progress(),
            "context_factors_importance": self.get_context_importance()
        }
        
        return insights

    def get_most_common_emotions(self) -> Dict[str, int]:
        """الحصول على أكثر المشاعر شيوعاً"""
        emotion_counts = {}
        
        for interaction in self.conversation_history:
            emotion = interaction.get('predicted_emotion', 'غير محدد')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return dict(sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5])

    def calculate_learning_progress(self) -> float:
        """حساب تقدم التعلم"""
        if len(self.conversation_history) < 10:
            return 0.0
        
        # مقارنة أداء أول 10 محادثات مع آخر 10
        first_batch = list(self.conversation_history)[:10]
        last_batch = list(self.conversation_history)[-10:]
        
        first_avg = sum(item.get('feedback_score', 0.5) for item in first_batch) / 10
        last_avg = sum(item.get('feedback_score', 0.5) for item in last_batch) / 10
        
        return max(0.0, (last_avg - first_avg))

    def get_context_importance(self) -> Dict[str, float]:
        """الحصول على أهمية عوامل السياق"""
        feature_importance = {}
        
        for emotion, weights in self.situation_emotion_map.items():
            for feature, weight in weights.items():
                if feature not in feature_importance:
                    feature_importance[feature] = 0.0
                feature_importance[feature] += abs(weight)
        
        # ترتيب حسب الأهمية
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10])