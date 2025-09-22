# emotional_intelligence.py - الذكاء العاطفي المتقدم ونظام الاستجابة التفاعلية
import json
import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import re

@dataclass
class EmotionalState:
    """الحالة العاطفية المتقدمة"""
    primary_emotion: str
    intensity: float  # 0.0 - 1.0
    secondary_emotions: Dict[str, float]
    emotional_history: List[str]
    stability: float
    empathy_score: float
    cultural_context: str

@dataclass
class ResponseTemplate:
    """قالب الاستجابة العاطفية"""
    emotion_trigger: str
    intensity_range: Tuple[float, float]
    response_patterns: List[str]
    cultural_adaptation: Dict[str, List[str]]
    empathy_level: str
    follow_up_questions: List[str]

class AdvancedEmotionalIntelligence:
    """نظام الذكاء العاطفي المتقدم لنانو"""
    
    def __init__(self):
        self.emotion_models = self.initialize_emotion_models()
        self.response_templates = self.initialize_response_templates()
        self.cultural_emotional_patterns = self.initialize_cultural_patterns()
        self.empathy_database = self.initialize_empathy_database()
        self.emotional_memory = deque(maxlen=100)
        self.personality_traits = self.initialize_personality_traits()
        
        # Pre-compile keyword sets for faster lookup
        self._compile_keyword_sets()
        
    def initialize_emotion_models(self) -> Dict[str, Dict]:
        """تهيئة نماذج المشاعر المتقدمة"""
        return {
            "joy": {
                "keywords": ["فرحان", "مبسوط", "سعيد", "مستانس", "منبسط", "مفرحان", "باين عليك الفرح"],
                "intensity_indicators": {
                    "high": ["مو طبيعي من الفرح", "طائر من الفرح", "أسعد إنسان", "ما أصدق"],
                    "medium": ["الحمدلله فرحان", "مبسوط والله", "سعيد جداً"],
                    "low": ["مبسوط", "كويس", "تمام"]
                },
                "physical_manifestations": ["ضحك", "ابتسامة", "حماس", "طاقة", "نشاط"],
                "triggers": ["نجاح", "مفاجأة سعيدة", "تحقق حلم", "لقاء أحباب"]
            },
            
            "sadness": {
                "keywords": ["حزين", "زعلان", "متضايق", "منكسر", "مكتئب", "تعبان نفسياً"],
                "intensity_indicators": {
                    "high": ["مكسور", "محطم", "مش قادر", "دايب من الحزن"],
                    "medium": ["زعلان كثير", "حزين والله", "متضايق جداً"],
                    "low": ["شوي حزين", "متضايق", "مو مرتاح"]
                },
                "physical_manifestations": ["بكاء", "صمت", "انطوائية", "فقدان شهية"],
                "triggers": ["خسارة", "فراق", "خيبة أمل", "مرض", "مشاكل عائلية"]
            },
            
            "fear": {
                "keywords": ["خايف", "قلقان", "متوتر", "مرعوب", "خوف", "رعب", "هلع"],
                "intensity_indicators": {
                    "high": ["مرعوب", "هلعان", "خايف موت", "مش قادر أنام"],
                    "medium": ["قلقان كثير", "خايف والله", "متوتر جداً"],
                    "low": ["شوي قلقان", "خايف", "متوتر"]
                },
                "physical_manifestations": ["ارتجاف", "تعرق", "خفقان", "أرق"],
                "triggers": ["مجهول", "امتحان", "مقابلة", "مرض", "خطر"]
            },
            
            "anger": {
                "keywords": ["غضبان", "زعلان", "متنرفز", "مستاء", "حانق", "مغتاظ"],
                "intensity_indicators": {
                    "high": ["مجنون من الغضب", "نار", "بركان", "حانق موت"],
                    "medium": ["غضبان كثير", "متنرفز جداً", "زعلان والله"],
                    "low": ["شوي متضايق", "متنرفز", "مستاء"]
                },
                "physical_manifestations": ["توتر", "ارتفاع ضغط", "احمرار", "صراخ"],
                "triggers": ["ظلم", "خيانة", "إهانة", "عدم احترام", "كذب"]
            },
            
            "love": {
                "keywords": ["أحب", "حبيبي", "عزيز", "غالي", "محب", "عاشق", "مولع"],
                "intensity_indicators": {
                    "high": ["عاشق", "مجنون حب", "حبي الوحيد", "روحي"],
                    "medium": ["أحبك كثير", "غالي عليّ", "عزيز جداً"],
                    "low": ["أحبك", "حبيبي", "عزيز عليّ"]
                },
                "physical_manifestations": ["دفء", "حنان", "اهتمام", "تضحية"],
                "triggers": ["أهل", "أصدقاء", "شريك حياة", "أطفال", "وطن"]
            }
        }
    
    def initialize_response_templates(self) -> Dict[str, ResponseTemplate]:
        """تهيئة قوالب الاستجابة"""
        return {
            "joy_high": ResponseTemplate(
                emotion_trigger="joy",
                intensity_range=(0.7, 1.0),
                response_patterns=[
                    "يا الله! فرحتنا بفرحتك والله! 🎉",
                    "هذا يستحق الاحتفال! مبروك من كل القلب! 🥳",
                    "الله يديم عليك السعادة دايماً! ما أحلى الأخبار! ✨",
                    "والله إن فرحتك أفرحتني! تستاهل كل خير! 🌟"
                ],
                cultural_adaptation={
                    "religious": ["الحمدلله رب العالمين!", "الله يبارك لك!", "من بركات الله عليك!"],
                    "family": ["الأهل بيفرحوا لك!", "عقبال أحبابك!", "فرحة لكل العائلة!"]
                },
                empathy_level="high",
                follow_up_questions=[
                    "قول لي تفاصيل أكثر، ودي أفرح معك!",
                    "كيف بتحتفل بهالخبر الحلو؟",
                    "مين أول شخص بشرته بالخبر؟"
                ]
            ),
            
            "sadness_high": ResponseTemplate(
                emotion_trigger="sadness",
                intensity_range=(0.7, 1.0),
                response_patterns=[
                    "حبيبي، قلبي معك في هالوقت الصعب 💙",
                    "الله يصبرك ويقويك، وأنا هنا لو تحتاج أي شي",
                    "ما عليك، الأيام الصعبة بتمر بإذن الله",
                    "معك في الحزن قبل الفرح، وكلنا نحبك"
                ],
                cultural_adaptation={
                    "religious": ["الله يصبرك ويأجرك", "لا حول ولا قوة إلا بالله", "البقية في حياتك"],
                    "family": ["الأهل كلهم معك", "العائلة سندك", "ما نخليك وحدك"]
                },
                empathy_level="very_high",
                follow_up_questions=[
                    "تبي تتكلم عن اللي صار؟",
                    "كيف أقدر أساعدك أو أخفف عنك؟",
                    "عندك حد تتكلم معه؟"
                ]
            ),
            
            "fear_medium": ResponseTemplate(
                emotion_trigger="fear",
                intensity_range=(0.4, 0.7),
                response_patterns=[
                    "لا تخاف، الله معك دايماً 🤲",
                    "هالشعور طبيعي، بس بتقدر تتجاوزه بإذن الله",
                    "خذ نفس عميق، وفكر في الأشياء الإيجابية",
                    "أنا معك، وكل شي بيعدي على خير"
                ],
                cultural_adaptation={
                    "religious": ["توكل على الله", "ادع وتوكل", "الله يكفيك شر اللي تخافه"],
                    "practical": ["خذ احتياطاتك وتوكل", "خطط كويس بتقل مخاوفك"]
                },
                empathy_level="medium",
                follow_up_questions=[
                    "إيش اللي يخوفك بالتحديد؟",
                    "جربت تفكر في حلول عملية؟",
                    "كيف تتعامل عادة مع مخاوفك؟"
                ]
            )
        }
    
    def initialize_cultural_patterns(self) -> Dict[str, Dict]:
        """تهيئة الأنماط الثقافية العاطفية"""
        return {
            "saudi_expressions": {
                "joy": ["يا فرحتي!", "الله يديم عليك!", "تبارك الرحمن!", "عساك على القوة!"],
                "sadness": ["الله يصبرك", "البقية في حياتك", "لا حول ولا قوة إلا بالله"],
                "comfort": ["ما عليك", "الله معك", "خير ان شاء الله", "ربك ما يهونك"],
                "encouragement": ["الله يقويك", "عاد مو كذا", "قوم يا بطل", "ما تنهزم"]
            },
            
            "family_dynamics": {
                "respect_elders": ["الله يطول بعمرهم", "دعواتهم معك", "بركة الوالدين"],
                "siblings": ["اخوك معك", "الأخوة سند", "عيلتك كلها معك"],
                "children": ["الله يحفظهم", "يكبروا ويعزوك", "فلذات الكبد"]
            },
            
            "religious_context": {
                "gratitude": ["الحمدلله على كل حال", "ربنا كريم", "من نعم الله"],
                "patience": ["الصبر مفتاح الفرج", "ما كتبه الله خير", "حكمة الله"],
                "hope": ["الفرج قريب", "الله يدبرها خير", "ربك ما يضيعك"]
            }
        }
    
    def initialize_empathy_database(self) -> Dict[str, List[str]]:
        """قاعدة بيانات التعاطف"""
        return {
            "validation": [
                "مشاعرك طبيعية ومفهومة",
                "أي حد مكانك بيحس نفس الشي",
                "ما تلوم نفسك على اللي تحسه",
                "من حقك تحس كذا"
            ],
            
            "support": [
                "أنا هنا لو تحتاج أي شي",
                "ما راح نخليك وحدك",
                "معك في الضيق قبل السعة",
                "كلنا نحبك ونسندك"
            ],
            
            "hope": [
                "الأيام الصعبة بتمر بإذن الله",
                "كل ضيقة وراها فرج",
                "أنت أقوى مما تتخيل",
                "الخير جاي ان شاء الله"
            ],
            
            "practical": [
                "نقدر نشوف حلول عملية سوا",
                "خطوة بخطوة وبنوصل",
                "المهم نبدا من مكان ما",
                "كل مشكلة ولها حل"
            ]
        }
    
    def initialize_personality_traits(self) -> Dict[str, float]:
        """تهيئة سمات الشخصية لنانو"""
        return {
            "empathy": 0.95,          # تعاطف عالي
            "warmth": 0.90,           # دفء عالي
            "patience": 0.85,         # صبر عالي
            "understanding": 0.92,    # فهم عالي
            "positivity": 0.88,       # إيجابية عالية
            "cultural_sensitivity": 0.98,  # حساسية ثقافية عالية جداً
            "humor": 0.75,            # دعابة متوسطة إلى عالية
            "wisdom": 0.80,           # حكمة عالية
            "supportiveness": 0.94,   # دعم عالي جداً
            "authenticity": 0.96      # أصالة عالية جداً
        }
        
    def _compile_keyword_sets(self):
        """Pre-compile keyword sets for faster emotion detection"""
        self._emotion_keyword_sets = {}
        for emotion, model in self.emotion_models.items():
            # Convert all keywords to lowercase sets
            keywords_set = set(kw.lower() for kw in model["keywords"])
            intensity_set = set()
            for level_indicators in model["intensity_indicators"].values():
                intensity_set.update(ind.lower() for ind in level_indicators)
            self._emotion_keyword_sets[emotion] = (keywords_set, intensity_set)
    
    def analyze_emotional_state(self, text: str, context_history: List = None) -> EmotionalState:
        """تحليل الحالة العاطفية المتقدم (محسّن الأداء)"""
        text_lower = text.lower()
        detected_emotions = {}
        
        # Split text once for set intersection
        text_words = set(text_lower.split())
        
        # تحليل المشاعر الأساسية باستخدام pre-compiled sets
        for emotion, (keywords_set, intensity_set) in self._emotion_keyword_sets.items():
            # Fast set intersection for keywords
            keyword_matches = len(text_words & keywords_set)
            if keyword_matches == 0:
                continue
                
            score = keyword_matches
            
            # Fast intensity check
            intensity_matches = text_words & intensity_set
            intensity = 0
            for match in intensity_matches:
                # Simple heuristic: longer phrases often indicate higher intensity
                if len(match) > 10:  # e.g., "مو طبيعي من الفرح"
                    intensity += 0.8
                elif len(match) > 6:  # e.g., "فرحان كثير"
                    intensity += 0.5
                else:  # e.g., "مبسوط"
                    intensity += 0.3
            
            detected_emotions[emotion] = min(score * 0.3 + intensity, 1.0)
        
        # تحديد المشاعر الأساسية والثانوية
        if detected_emotions:
            primary_emotion = max(detected_emotions, key=detected_emotions.get)
            primary_intensity = detected_emotions[primary_emotion]
            
            secondary_emotions = {k: v for k, v in detected_emotions.items() if k != primary_emotion}
        else:
            primary_emotion = "neutral"
            primary_intensity = 0.5
            secondary_emotions = {}
        
        # تحليل السياق الثقافي
        cultural_context = self.analyze_cultural_context(text)
        
        # حساب الاستقرار العاطفي من التاريخ
        stability = self.calculate_emotional_stability(context_history)
        
        # حساب نقاط التعاطف
        empathy_score = self.calculate_empathy_score(primary_emotion, primary_intensity)
        
        return EmotionalState(
            primary_emotion=primary_emotion,
            intensity=primary_intensity,
            secondary_emotions=secondary_emotions,
            emotional_history=self.get_recent_emotional_history(),
            stability=stability,
            empathy_score=empathy_score,
            cultural_context=cultural_context
        )
    
    def analyze_cultural_context(self, text: str) -> str:
        """تحليل السياق الثقافي"""
        text_lower = text.lower()
        
        # فحص العلامات الدينية
        religious_markers = ["الله", "الحمدلله", "ان شاء الله", "ما شاء الله"]
        if any(marker in text_lower for marker in religious_markers):
            return "religious"
        
        # فحص السياق العائلي
        family_markers = ["أهل", "عائلة", "والدين", "أمي", "أبوي"]
        if any(marker in text_lower for marker in family_markers):
            return "family"
        
        # فحص السياق الرسمي
        formal_markers = ["أستاذ", "دكتور", "مدير", "عمل", "وظيفة"]
        if any(marker in text_lower for marker in formal_markers):
            return "formal"
        
        return "casual"
    
    def calculate_emotional_stability(self, history: List) -> float:
        """حساب الاستقرار العاطفي"""
        if not history or len(history) < 3:
            return 0.5  # متوسط افتراضي
        
        # تحليل تقلبات المشاعر في التاريخ الحديث
        emotions = [self.analyze_emotional_state(msg).primary_emotion for msg in history[-5:]]
        unique_emotions = len(set(emotions))
        
        # كلما قل التنوع، زاد الاستقرار
        stability = max(0.1, 1.0 - (unique_emotions / 5.0))
        return stability
    
    def calculate_empathy_score(self, emotion: str, intensity: float) -> float:
        """حساب نقاط التعاطف المطلوبة"""
        base_empathy = self.personality_traits["empathy"]
        
        # المشاعر السلبية تتطلب تعاطف أكثر
        if emotion in ["sadness", "fear", "anger"]:
            return min(base_empathy + (intensity * 0.2), 1.0)
        
        # المشاعر الإيجابية تتطلب تعاطف أقل لكن مشاركة في الفرح
        elif emotion in ["joy", "love"]:
            return base_empathy * 0.8
        
        return base_empathy
    
    def get_recent_emotional_history(self) -> List[str]:
        """الحصول على التاريخ العاطفي الحديث"""
        return list(self.emotional_memory)[-10:]  # آخر 10 حالات عاطفية
    
    def generate_empathetic_response(self, emotional_state: EmotionalState, user_message: str) -> Dict[str, Any]:
        """توليد استجابة متعاطفة ومتقدمة"""
        emotion = emotional_state.primary_emotion
        intensity = emotional_state.intensity
        cultural_context = emotional_state.cultural_context
        
        # اختيار القالب المناسب
        template_key = self.find_best_template(emotion, intensity)
        template = self.response_templates.get(template_key)
        
        if not template:
            # استجابة افتراضية
            return self.generate_default_response(emotional_state, user_message)
        
        # اختيار نمط الاستجابة
        base_response = random.choice(template.response_patterns)
        
        # تطبيق التكييف الثقافي
        cultural_addition = ""
        if cultural_context in template.cultural_adaptation:
            cultural_addition = random.choice(template.cultural_adaptation[cultural_context])
        
        # إضافة عنصر التعاطف
        empathy_element = self.add_empathy_element(emotional_state)
        
        # اختيار سؤال متابعة مناسب
        follow_up = random.choice(template.follow_up_questions) if template.follow_up_questions else ""
        
        # بناء الاستجابة النهائية
        response_parts = [base_response]
        if cultural_addition:
            response_parts.append(cultural_addition)
        if empathy_element:
            response_parts.append(empathy_element)
        if follow_up and intensity > 0.6:  # أسئلة المتابعة للحالات الشديدة فقط
            response_parts.append(follow_up)
        
        final_response = " ".join(response_parts)
        
        # تحليل جودة الاستجابة
        response_quality = self.assess_response_quality(emotional_state, final_response)
        
        return {
            "response": final_response,
            "emotion_detected": emotion,
            "intensity": intensity,
            "empathy_level": template.empathy_level,
            "cultural_adaptation": cultural_context,
            "response_quality": response_quality,
            "emotional_resonance": self.calculate_emotional_resonance(emotional_state, final_response)
        }
    
    def find_best_template(self, emotion: str, intensity: float) -> str:
        """العثور على أفضل قالب للاستجابة"""
        best_template = None
        best_score = -1
        
        for template_key, template in self.response_templates.items():
            if template.emotion_trigger == emotion:
                min_intensity, max_intensity = template.intensity_range
                if min_intensity <= intensity <= max_intensity:
                    # حساب مدى ملاءمة القالب
                    score = 1.0 - abs(intensity - ((min_intensity + max_intensity) / 2))
                    if score > best_score:
                        best_score = score
                        best_template = template_key
        
        return best_template or f"{emotion}_default"
    
    def add_empathy_element(self, emotional_state: EmotionalState) -> str:
        """إضافة عنصر التعاطف"""
        emotion = emotional_state.primary_emotion
        intensity = emotional_state.intensity
        
        if intensity < 0.3:
            return ""  # لا حاجة لتعاطف إضافي للمشاعر الخفيفة
        
        empathy_category = "support"
        if emotion in ["sadness", "fear"]:
            empathy_category = "validation" if intensity > 0.7 else "support"
        elif emotion == "anger":
            empathy_category = "validation"
        elif emotion in ["joy", "love"]:
            empathy_category = "support"
        
        return random.choice(self.empathy_database.get(empathy_category, ["أنا معك"]))
    
    def generate_default_response(self, emotional_state: EmotionalState, user_message: str) -> Dict[str, Any]:
        """توليد استجابة افتراضية"""
        emotion = emotional_state.primary_emotion
        base_responses = {
            "neutral": "أفهم شعورك، وأنا هنا لو تحتاج أتكلم عن أي شي",
            "joy": "فرحتنا بفرحتك! الله يديم عليك السعادة",
            "sadness": "قلبي معك في هالوقت، والله يصبرك ويقويك",
            "fear": "لا تخاف، الله معك وكل شي بيعدي على خير",
            "anger": "أفهم غضبك، وهالشعور طبيعي في موقف زي كذا",
            "love": "ما أحلى هالمشاعر! الحب شي جميل"
        }
        
        response = base_responses.get(emotion, "أفهم مشاعرك وأنا معك")
        
        return {
            "response": response,
            "emotion_detected": emotion,
            "intensity": emotional_state.intensity,
            "empathy_level": "medium",
            "cultural_adaptation": "general",
            "response_quality": 0.7,
            "emotional_resonance": 0.6
        }
    
    def assess_response_quality(self, emotional_state: EmotionalState, response: str) -> float:
        """تقييم جودة الاستجابة"""
        score = 0.0
        
        # فحص الطول المناسب
        word_count = len(response.split())
        if 5 <= word_count <= 25:
            score += 0.2
        
        # فحص التطابق العاطفي
        if emotional_state.primary_emotion in response.lower():
            score += 0.2
        
        # فحص التكييف الثقافي
        cultural_keywords = ["الله", "ان شاء الله", "الحمدلله", "يا رب"]
        if any(keyword in response for keyword in cultural_keywords):
            score += 0.3
        
        # فحص عناصر التعاطف
        empathy_indicators = ["معك", "أفهم", "قلبي", "نحبك", "هنا لك"]
        if any(indicator in response for indicator in empathy_indicators):
            score += 0.3
        
        return min(score, 1.0)
    
    def calculate_emotional_resonance(self, emotional_state: EmotionalState, response: str) -> float:
        """حساب الرنين العاطفي للاستجابة"""
        # تحليل مدى تطابق الاستجابة مع الحالة العاطفية
        emotion_words = {
            "joy": ["فرح", "سعادة", "مبروك", "هنيئاً"],
            "sadness": ["حزن", "ضيق", "صبر", "تعاطف"],
            "fear": ["أمان", "طمأنينة", "حماية", "دعم"],
            "anger": ["فهم", "حق", "معك", "طبيعي"],
            "love": ["حب", "جميل", "رائع", "أحلى"]
        }
        
        emotion = emotional_state.primary_emotion
        if emotion in emotion_words:
            response_lower = response.lower()
            matches = sum(1 for word in emotion_words[emotion] if word in response_lower)
            return min(matches / len(emotion_words[emotion]), 1.0)
        
        return 0.5  # متوسط افتراضي
    
    def update_emotional_memory(self, emotional_state: EmotionalState, response_data: Dict):
        """تحديث الذاكرة العاطفية"""
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "emotion": emotional_state.primary_emotion,
            "intensity": emotional_state.intensity,
            "response_quality": response_data["response_quality"],
            "empathy_level": response_data["empathy_level"]
        }
        
        self.emotional_memory.append(memory_entry)
    
    def get_emotional_analytics(self) -> Dict[str, Any]:
        """تحليلات الأداء العاطفي"""
        if not self.emotional_memory:
            return {"message": "لا توجد بيانات عاطفية كافية"}
        
        emotions = [entry["emotion"] for entry in self.emotional_memory]
        intensities = [entry["intensity"] for entry in self.emotional_memory]
        qualities = [entry["response_quality"] for entry in self.emotional_memory]
        
        return {
            "total_interactions": len(self.emotional_memory),
            "most_common_emotion": max(set(emotions), key=emotions.count),
            "average_intensity": sum(intensities) / len(intensities),
            "average_response_quality": sum(qualities) / len(qualities),
            "emotional_distribution": {emotion: emotions.count(emotion) for emotion in set(emotions)},
            "empathy_effectiveness": sum(1 for entry in self.emotional_memory if entry["response_quality"] > 0.8) / len(self.emotional_memory),
            "last_updated": datetime.now().isoformat()
        }

if __name__ == "__main__":
    print("🧠 نظام الذكاء العاطفي المتقدم لنانو")
    
    # إنشاء النظام
    ei_system = AdvancedEmotionalIntelligence()
    
    # اختبار النظام
    test_messages = [
        "والله فرحان مو طبيعي! حصلت على وظيفة أحلامي!",
        "حزين جداً لأن جدي توفى اليوم... الله يرحمه",
        "خايف من امتحان الغد، مو مستعد كويس",
        "غضبان من صديقي لأنه خانني وكذب عليّ",
        "أحب عائلتي كثير، هم كل حياتي"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*50}")
        print(f"اختبار {i}: {message}")
        
        # تحليل الحالة العاطفية
        emotional_state = ei_system.analyze_emotional_state(message)
        
        # توليد الاستجابة
        response_data = ei_system.generate_empathetic_response(emotional_state, message)
        
        # تحديث الذاكرة
        ei_system.update_emotional_memory(emotional_state, response_data)
        
        # عرض النتائج
        print(f"\nالمشاعر المكتشفة: {emotional_state.primary_emotion} (شدة: {emotional_state.intensity:.2f})")
        print(f"الاستجابة: {response_data['response']}")
        print(f"مستوى التعاطف: {response_data['empathy_level']}")
        print(f"جودة الاستجابة: {response_data['response_quality']:.2f}")
        print(f"الرنين العاطفي: {response_data['emotional_resonance']:.2f}")
    
    # عرض التحليلات
    analytics = ei_system.get_emotional_analytics()
    print(f"\n{'🔍 تحليلات الأداء العاطفي ':=^60}")
    for key, value in analytics.items():
        print(f"{key}: {value}")
    
    print("\n✨ نانو الآن مزود بذكاء عاطفي متقدم للغاية! ✨")