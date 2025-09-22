# context_memory.py - نظام الذاكرة السياقية المتقدم
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import re

@dataclass
class ConversationContext:
    """سياق المحادثة المتقدم"""
    timestamp: str
    user_message: str
    nano_response: str
    emotion_detected: str
    topic_category: str
    cultural_markers: List[str]
    confidence_level: float
    memory_importance: int  # 1-10 scale

@dataclass
class PersonalityProfile:
    """ملف الشخصية المستخدم"""
    name: Optional[str]
    preferred_topics: List[str]
    communication_style: str
    emotional_patterns: Dict[str, int]
    cultural_background: str
    interaction_history: List[str]
    relationship_level: str  # stranger, acquaintance, friend, family

class AdvancedContextMemory:
    """نظام الذاكرة السياقية المتقدم لنانو"""
    
    def __init__(self, memory_path="nano_memory.json"):
        self.memory_path = memory_path
        self.conversation_history = []
        self.personality_profiles = {}
        self.cultural_patterns = self.initialize_cultural_patterns()
        self.emotion_keywords = self.initialize_emotion_keywords()
        self.topic_classifiers = self.initialize_topic_classifiers()
        
        # Pre-compile keyword sets for faster lookup
        self._compile_pattern_sets()
        self.load_memory()
        
    def initialize_cultural_patterns(self) -> Dict[str, List[str]]:
        """تهيئة أنماط ثقافية سعودية"""
        return {
            "religious": [
                "الله", "الحمدلله", "ان شاء الله", "ما شاء الله", "بإذن الله",
                "استغفر الله", "بسم الله", "صلى الله عليه وسلم", "رحمه الله",
                "جزاك الله خير", "بارك الله فيك", "هداك الله", "الله يعطيك العافية"
            ],
            "greetings": [
                "السلام عليكم", "أهلا وسهلا", "مرحبا", "حياك الله", "أهلين",
                "يا هلا", "نورت", "تشرفنا", "منور", "عساك بخير"
            ],
            "hospitality": [
                "تفضل", "اتفضل", "بيتك", "أهل وسهل", "كرامة", "شرفتنا",
                "قهوة", "عشا", "غدا", "ضيف", "كريم", "عزيز"
            ],
            "respect": [
                "أستاذ", "أبو", "أم", "عمي", "خالي", "عمتي", "خالتي",
                "حضرتك", "الكريم", "المحترم", "الفاضل", "المكرم"
            ],
            "emotions": [
                "فرحان", "مبسوط", "سعيد", "حزين", "متضايق", "خايف",
                "قلقان", "مرتاح", "متحمس", "زعلان", "مستانس"
            ]
        }
    
    def initialize_emotion_keywords(self) -> Dict[str, List[str]]:
        """تهيئة كلمات المشاعر"""
        return {
            "joy": ["فرحان", "مبسوط", "سعيد", "مستانس", "فرحة", "سعادة", "بهجة"],
            "sadness": ["حزين", "زعلان", "متضايق", "حزن", "ضيق", "كآبة", "أسى"],
            "fear": ["خايف", "قلقان", "متوتر", "خوف", "قلق", "توتر", "رعب"],
            "anger": ["زعلان", "غضبان", "متنرفز", "غضب", "زعل", "انفعال", "حنق"],
            "love": ["محب", "أحب", "عاشق", "حب", "عشق", "غرام", "هيام"],
            "excitement": ["متحمس", "متشوق", "حماس", "شوق", "نشاط", "حيوية"],
            "calmness": ["هادي", "مرتاح", "ساكن", "هدوء", "راحة", "سكينة", "طمأنينة"],
            "gratitude": ["شكر", "امتنان", "تقدير", "شاكر", "ممتن", "مقدر"]
        }
    
    def initialize_topic_classifiers(self) -> Dict[str, List[str]]:
        """تهيئة مصنفات المواضيع"""
        return {
            "family": ["أهل", "عائلة", "والدين", "اخوان", "أخوات", "أطفال", "بيت", "منزل"],
            "work": ["شغل", "عمل", "وظيفة", "مدير", "زميل", "راتب", "دوام", "مكتب"],
            "education": ["دراسة", "جامعة", "مدرسة", "طالب", "امتحان", "درجات", "تعليم"],
            "health": ["صحة", "مرض", "مستشفى", "دكتور", "دواء", "علاج", "فحص"],
            "food": ["أكل", "طعام", "طبخ", "مطعم", "وجبة", "إفطار", "غدا", "عشا"],
            "travel": ["سفر", "رحلة", "مطار", "فندق", "سياحة", "إجازة", "بلد"],
            "technology": ["جوال", "كمبيوتر", "إنترنت", "تقنية", "برنامج", "تطبيق"],
            "sports": ["رياضة", "كرة", "فريق", "لاعب", "مباراة", "نادي", "تمرين"],
            "weather": ["طقس", "مطر", "شمس", "برد", "حر", "غيوم", "رياح"],
            "shopping": ["تسوق", "شراء", "مول", "سوق", "سعر", "خصم", "متجر"]
        }
        
    def _compile_pattern_sets(self):
        """Pre-compile keyword sets for faster pattern matching"""
        # Emotion keyword sets (lowercase)
        self._emotion_sets = {}
        for emotion, keywords in self.emotion_keywords.items():
            self._emotion_sets[emotion] = set(kw.lower() for kw in keywords)
            
        # Topic classifier sets (lowercase)
        self._topic_sets = {}
        for topic, keywords in self.topic_classifiers.items():
            self._topic_sets[topic] = set(kw.lower() for kw in keywords)
            
        # Cultural pattern sets (lowercase)
        self._cultural_sets = {}
        for category, patterns in self.cultural_patterns.items():
            self._cultural_sets[category] = set(p.lower() for p in patterns)
    
    def detect_emotion(self, text: str) -> Tuple[str, float]:
        """كشف المشاعر من النص (محسّن الأداء)"""
        text_lower = text.lower()
        text_words = set(text_lower.split())
        
        emotion_scores = {}
        for emotion, keyword_set in self._emotion_sets.items():
            matches = len(text_words & keyword_set)
            if matches > 0:
                emotion_scores[emotion] = matches
        
        if not emotion_scores:
            return "neutral", 0.5
        
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(emotion_scores[dominant_emotion] / len(text_words), 1.0)
        
        return dominant_emotion, confidence
    
    def classify_topic(self, text: str) -> str:
        """تصنيف موضوع النص (محسّن الأداء)"""
        text_words = set(text.lower().split())
        
        topic_scores = {}
        for topic, keyword_set in self._topic_sets.items():
            matches = len(text_words & keyword_set)
            if matches > 0:
                topic_scores[topic] = matches
        
        if not topic_scores:
            return "general"
        
        return max(topic_scores, key=topic_scores.get)
    
    def extract_cultural_markers(self, text: str) -> List[str]:
        """استخراج العلامات الثقافية (محسّن الأداء)"""
        text_words = set(text.lower().split())
        markers = []
        
        for category, pattern_set in self._cultural_sets.items():
            matches = text_words & pattern_set
            for match in matches:
                markers.append(f"{category}:{match}")
        
        return markers
    
    def calculate_memory_importance(self, context: ConversationContext) -> int:
        """حساب أهمية الذاكرة"""
        importance = 5  # Base importance
        
        # زيادة الأهمية للمشاعر القوية
        if context.emotion_detected in ["joy", "sadness", "fear", "love"]:
            importance += 2
        
        # زيادة الأهمية للمعلومات الشخصية
        personal_keywords = ["اسمي", "أنا", "بيتي", "عائلتي", "شغلي"]
        if any(keyword in context.user_message.lower() for keyword in personal_keywords):
            importance += 3
        
        # زيادة الأهمية للعلامات الثقافية
        if len(context.cultural_markers) > 2:
            importance += 1
        
        # زيادة الأهمية للثقة العالية
        if context.confidence_level > 0.8:
            importance += 1
        
        return min(importance, 10)
    
    def add_conversation_context(self, user_message: str, nano_response: str) -> ConversationContext:
        """إضافة سياق محادثة جديد"""
        emotion, confidence = self.detect_emotion(user_message)
        topic = self.classify_topic(user_message)
        cultural_markers = self.extract_cultural_markers(user_message + " " + nano_response)
        
        context = ConversationContext(
            timestamp=datetime.now().isoformat(),
            user_message=user_message,
            nano_response=nano_response,
            emotion_detected=emotion,
            topic_category=topic,
            cultural_markers=cultural_markers,
            confidence_level=confidence,
            memory_importance=0  # Will be calculated
        )
        
        context.memory_importance = self.calculate_memory_importance(context)
        self.conversation_history.append(context)
        
        # الاحتفاظ بآخر 1000 محادثة فقط
        if len(self.conversation_history) > 1000:
            self.conversation_history = self.conversation_history[-1000:]
        
        return context
    
    def get_relevant_context(self, current_message: str, limit: int = 5) -> List[ConversationContext]:
        """استرجاع السياق ذي الصلة"""
        current_emotion, _ = self.detect_emotion(current_message)
        current_topic = self.classify_topic(current_message)
        current_markers = self.extract_cultural_markers(current_message)
        
        # تسجيل نقاط للمحادثات السابقة
        scored_contexts = []
        for context in self.conversation_history[-50:]:  # آخر 50 محادثة
            score = 0
            
            # نفس المشاعر
            if context.emotion_detected == current_emotion:
                score += 3
            
            # نفس الموضوع
            if context.topic_category == current_topic:
                score += 2
            
            # علامات ثقافية مشتركة
            common_markers = set(context.cultural_markers) & set(current_markers)
            score += len(common_markers)
            
            # أهمية الذاكرة
            score += context.memory_importance / 2
            
            # حداثة المحادثة
            age_hours = (datetime.now() - datetime.fromisoformat(context.timestamp)).total_seconds() / 3600
            if age_hours < 24:
                score += 2
            elif age_hours < 168:  # أسبوع
                score += 1
            
            scored_contexts.append((context, score))
        
        # ترتيب حسب النقاط
        scored_contexts.sort(key=lambda x: x[1], reverse=True)
        
        return [context for context, score in scored_contexts[:limit]]
    
    def generate_contextual_response_hints(self, user_message: str) -> Dict[str, Any]:
        """توليد تلميحات للرد السياقي"""
        relevant_contexts = self.get_relevant_context(user_message)
        emotion, confidence = self.detect_emotion(user_message)
        topic = self.classify_topic(user_message)
        cultural_markers = self.extract_cultural_markers(user_message)
        
        hints = {
            "detected_emotion": emotion,
            "emotion_confidence": confidence,
            "topic_category": topic,
            "cultural_markers": cultural_markers,
            "relevant_history": [
                {
                    "user_said": ctx.user_message,
                    "nano_responded": ctx.nano_response,
                    "emotion": ctx.emotion_detected,
                    "topic": ctx.topic_category
                }
                for ctx in relevant_contexts
            ],
            "conversation_patterns": self.analyze_conversation_patterns(),
            "suggested_tone": self.suggest_response_tone(emotion, cultural_markers),
            "memory_triggers": self.find_memory_triggers(user_message)
        }
        
        return hints
    
    def analyze_conversation_patterns(self) -> Dict[str, Any]:
        """تحليل أنماط المحادثة"""
        if len(self.conversation_history) < 5:
            return {"insufficient_data": True}
        
        recent_emotions = [ctx.emotion_detected for ctx in self.conversation_history[-10:]]
        recent_topics = [ctx.topic_category for ctx in self.conversation_history[-10:]]
        
        emotion_frequency = defaultdict(int)
        topic_frequency = defaultdict(int)
        
        for emotion in recent_emotions:
            emotion_frequency[emotion] += 1
        
        for topic in recent_topics:
            topic_frequency[topic] += 1
        
        return {
            "dominant_emotion": max(emotion_frequency, key=emotion_frequency.get) if emotion_frequency else "neutral",
            "frequent_topics": list(topic_frequency.keys()),
            "conversation_mood": self.assess_conversation_mood(recent_emotions),
            "engagement_level": self.calculate_engagement_level()
        }
    
    def suggest_response_tone(self, emotion: str, cultural_markers: List[str]) -> str:
        """اقتراح نبرة الرد"""
        tone_mapping = {
            "joy": "enthusiastic_supportive",
            "sadness": "empathetic_comforting", 
            "fear": "reassuring_calming",
            "anger": "understanding_diplomatic",
            "love": "warm_appreciative",
            "excitement": "matching_enthusiasm",
            "calmness": "peaceful_gentle",
            "gratitude": "humble_gracious"
        }
        
        base_tone = tone_mapping.get(emotion, "neutral_friendly")
        
        # تعديل النبرة حسب العلامات الثقافية
        religious_markers = [m for m in cultural_markers if m.startswith("religious:")]
        if religious_markers:
            base_tone += "_respectful"
        
        formal_markers = [m for m in cultural_markers if m.startswith("respect:")]
        if formal_markers:
            base_tone += "_formal"
        
        return base_tone
    
    def find_memory_triggers(self, message: str) -> List[str]:
        """العثور على محفزات الذاكرة"""
        triggers = []
        message_lower = message.lower()
        
        # البحث في المحادثات السابقة عن مواضيع مشابهة
        for context in self.conversation_history[-100:]:
            user_words = set(context.user_message.lower().split())
            message_words = set(message_lower.split())
            
            common_words = user_words & message_words
            if len(common_words) > 2:
                triggers.append(f"similar_to: {context.user_message[:50]}...")
        
        return triggers[:3]  # أهم 3 محفزات
    
    def assess_conversation_mood(self, emotions: List[str]) -> str:
        """تقييم مزاج المحادثة"""
        positive_emotions = ["joy", "love", "excitement", "gratitude"]
        negative_emotions = ["sadness", "fear", "anger"]
        
        positive_count = sum(1 for e in emotions if e in positive_emotions)
        negative_count = sum(1 for e in emotions if e in negative_emotions)
        
        if positive_count > negative_count * 1.5:
            return "positive"
        elif negative_count > positive_count * 1.5:
            return "negative"
        else:
            return "balanced"
    
    def calculate_engagement_level(self) -> float:
        """حساب مستوى التفاعل"""
        if len(self.conversation_history) < 3:
            return 0.5
        
        recent_contexts = self.conversation_history[-10:]
        
        # قياس طول الرسائل
        avg_message_length = sum(len(ctx.user_message.split()) for ctx in recent_contexts) / len(recent_contexts)
        
        # قياس تنوع المواضيع
        unique_topics = len(set(ctx.topic_category for ctx in recent_contexts))
        
        # قياس العمق العاطفي
        emotional_depth = sum(1 for ctx in recent_contexts if ctx.confidence_level > 0.7)
        
        engagement = min((avg_message_length / 10 + unique_topics / 5 + emotional_depth / 10) / 3, 1.0)
        
        return engagement
    
    def save_memory(self):
        """حفظ الذاكرة إلى ملف"""
        memory_data = {
            "conversation_history": [asdict(ctx) for ctx in self.conversation_history[-500:]],  # آخر 500 محادثة
            "personality_profiles": self.personality_profiles,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)
    
    def load_memory(self):
        """تحميل الذاكرة من ملف"""
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            # تحميل المحادثات
            self.conversation_history = [
                ConversationContext(**ctx_data) 
                for ctx_data in memory_data.get("conversation_history", [])
            ]
            
            # تحميل ملفات الشخصية
            self.personality_profiles = memory_data.get("personality_profiles", {})
            
        except FileNotFoundError:
            self.conversation_history = []
            self.personality_profiles = {}
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """احصائيات الذاكرة"""
        total_conversations = len(self.conversation_history)
        
        if total_conversations == 0:
            return {"total_conversations": 0, "message": "لا توجد محادثات مسجلة بعد"}
        
        emotion_stats = defaultdict(int)
        topic_stats = defaultdict(int)
        
        for ctx in self.conversation_history:
            emotion_stats[ctx.emotion_detected] += 1
            topic_stats[ctx.topic_category] += 1
        
        return {
            "total_conversations": total_conversations,
            "most_common_emotion": max(emotion_stats, key=emotion_stats.get),
            "most_discussed_topic": max(topic_stats, key=topic_stats.get),
            "average_confidence": sum(ctx.confidence_level for ctx in self.conversation_history) / total_conversations,
            "high_importance_memories": sum(1 for ctx in self.conversation_history if ctx.memory_importance > 7),
            "memory_span_days": (
                datetime.now() - datetime.fromisoformat(self.conversation_history[0].timestamp)
            ).days if self.conversation_history else 0
        }

if __name__ == "__main__":
    # اختبار النظام
    print("🧠 نظام الذاكرة السياقية المتقدم لنانو")
    
    memory_system = AdvancedContextMemory()
    
    # محاكاة محادثة
    test_conversations = [
        ("السلام عليكم، كيف الحال؟", "وعليكم السلام، الحمدلله بخير وأنت كيفك؟"),
        ("الحمدلله، أنا فرحان اليوم لأن حصلت على وظيفة جديدة", "مبروك عليك! الله يبارك لك في الوظيفة الجديدة"),
        ("أشكرك، بس قلقان شوي من التحدي الجديد", "هذا طبيعي، بإذن الله تتأقلم بسرعة وتنجح"),
        ("كيف أتعامل مع ضغط العمل؟", "المهم تنظم وقتك وتاخذ راحة بين الفترات")
    ]
    
    for user_msg, nano_resp in test_conversations:
        context = memory_system.add_conversation_context(user_msg, nano_resp)
        print(f"\n📝 محادثة جديدة:")
        print(f"المستخدم: {user_msg}")
        print(f"نانو: {nano_resp}")
        print(f"المشاعر: {context.emotion_detected}")
        print(f"الموضوع: {context.topic_category}")
        print(f"أهمية الذاكرة: {context.memory_importance}/10")
    
    # عرض الإحصائيات
    stats = memory_system.get_memory_stats()
    print(f"\n📊 إحصائيات الذاكرة:")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # حفظ الذاكرة
    memory_system.save_memory()
    print("\n💾 تم حفظ الذاكرة بنجاح!")