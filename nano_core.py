# nano_core.py - النواة المركزية لنانو مع نظام الوحدات والمشاعر
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

# ============= نظام المشاعر =============
class EmotionType(Enum):
    """أنواع المشاعر"""
    HAPPINESS = "سعادة"
    SADNESS = "حزن" 
    ANGER = "غضب"
    LOVE = "حب"
    TRUST = "ثقة"
    FEAR = "خوف"
    SURPRISE = "دهشة"
    RESPECT = "احترام"
    EXCITEMENT = "حماس"
    CALM = "هدوء"

@dataclass
class EmotionState:
    """حالة المشاعر"""
    emotion: EmotionType
    intensity: float  # من 0 إلى 1
    duration: int     # بالثواني
    created_at: datetime

class EmotionEngine:
    """محرك المشاعر"""
    
    def __init__(self):
        self.current_emotions: List[EmotionState] = []
        self.base_personality = {
            EmotionType.HAPPINESS: 0.7,
            EmotionType.TRUST: 0.6,
            EmotionType.RESPECT: 0.8,
            EmotionType.CALM: 0.5
        }
        self.emotion_memory = []  # ذاكرة المشاعر
        
        # كلمات تثير مشاعر معينة
        self.emotion_triggers = {
            EmotionType.HAPPINESS: ["مبروك", "فرح", "سعيد", "حلو", "زين", "بطل", "كفو"],
            EmotionType.LOVE: ["حبيبي", "عزيزي", "غالي", "يا روحي", "حبيب قلبي"],
            EmotionType.ANGER: ["غبي", "حمار", "متضايق", "زعلان", "مستفز"],
            EmotionType.SADNESS: ["حزين", "متضايق", "زعلان", "حزن", "مكسور"],
            EmotionType.TRUST: ["ثقة", "صادق", "أمين", "مخلص", "وفي"],
            EmotionType.RESPECT: ["أستاذ", "دكتور", "شيخ", "كبير", "محترم"],
            EmotionType.FEAR: ["خايف", "خوف", "قلقان", "متوتر"],
            EmotionType.SURPRISE: ["وا", "يا ساتر", "لا حول", "ما شاء الله"],
            EmotionType.EXCITEMENT: ["يلا", "هيا", "حماس", "متحمس", "فلة"]
        }
    
    def analyze_emotion_triggers(self, text: str) -> List[tuple]:
        """تحليل النص لاكتشاف مثيرات المشاعر"""
        detected_emotions = []
        text_lower = text.lower()
        
        for emotion, triggers in self.emotion_triggers.items():
            for trigger in triggers:
                if trigger in text_lower:
                    intensity = random.uniform(0.3, 0.8)
                    detected_emotions.append((emotion, intensity))
        
        return detected_emotions
    
    def add_emotion(self, emotion: EmotionType, intensity: float, duration: int = 300):
        """إضافة مشاعر جديدة"""
        new_emotion = EmotionState(
            emotion=emotion,
            intensity=min(1.0, max(0.0, intensity)),
            duration=duration,
            created_at=datetime.now()
        )
        self.current_emotions.append(new_emotion)
        self.emotion_memory.append(new_emotion)
        
        # الاحتفاظ بآخر 50 ذكرى مشاعر
        if len(self.emotion_memory) > 50:
            self.emotion_memory.pop(0)
    
    def update_emotions_from_text(self, text: str):
        """تحديث المشاعر بناءً على النص"""
        detected = self.analyze_emotion_triggers(text)
        for emotion, intensity in detected:
            self.add_emotion(emotion, intensity)
    
    def get_dominant_emotion(self) -> EmotionType:
        """الحصول على المشاعر المهيمنة حالياً"""
        if not self.current_emotions:
            return EmotionType.CALM
        
        # تنظيف المشاعر المنتهية الصلاحية
        current_time = datetime.now()
        self.current_emotions = [
            e for e in self.current_emotions 
            if (current_time - e.created_at).seconds < e.duration
        ]
        
        if not self.current_emotions:
            return EmotionType.CALM
        
        # إيجاد أقوى مشاعر
        strongest = max(self.current_emotions, key=lambda x: x.intensity)
        return strongest.emotion
    
    def get_emotion_intensity(self, emotion: EmotionType) -> float:
        """شدة مشاعر معينة"""
        current_time = datetime.now()
        total_intensity = 0.0
        count = 0
        
        for e in self.current_emotions:
            if e.emotion == emotion and (current_time - e.created_at).seconds < e.duration:
                total_intensity += e.intensity
                count += 1
        
        return total_intensity / count if count > 0 else self.base_personality.get(emotion, 0.0)

# ============= نظام الوحدات =============
class ModuleType(Enum):
    """أنواع الوحدات"""
    ARABIC_LANGUAGE = "اللغة العربية"
    ENGLISH_LANGUAGE = "اللغة الإنجليزية"
    DRAWING = "الرسم"
    MATH = "الرياضيات"
    GENERAL_KNOWLEDGE = "المعرفة العامة"
    PERSONALITY = "الشخصية"

class NanoModule:
    """الفئة الأساسية للوحدات"""
    
    def __init__(self, module_type: ModuleType, name: str):
        self.module_type = module_type
        self.name = name
        self.is_active = True
    
    def process(self, input_text: str, emotion_state: EmotionType) -> str:
        """معالجة النص"""
        raise NotImplementedError
    
    def can_handle(self, input_text: str) -> bool:
        """تحديد إذا كانت الوحدة تستطيع معالجة النص"""
        raise NotImplementedError

class ArabicLanguageModule(NanoModule):
    """وحدة اللغة العربية"""
    
    def __init__(self):
        super().__init__(ModuleType.ARABIC_LANGUAGE, "وحدة اللغة العربية")
        self.load_corpus()
        self.model = {}
        self._start_token = "_START_"
        self._end_token = "_END_"
    
    def load_corpus(self):
        """تحميل قاعدة البيانات العربية"""
        try:
            with open("corpus.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sentences = data.get("sentences", [])
        except FileNotFoundError:
            self.sentences = ["مرحباً", "أهلاً وسهلاً", "كيف حالك"]
    
    def train_model(self):
        """تدريب نموذج اللغة العربية"""
        for sentence in self.sentences:
            words = [self._start_token] + sentence.strip().split() + [self._end_token]
            for i in range(len(words) - 1):
                current_word = words[i]
                next_word = words[i+1]
                
                if current_word not in self.model:
                    self.model[current_word] = {}
                if next_word not in self.model[current_word]:
                    self.model[current_word][next_word] = 0
                
                self.model[current_word][next_word] += 1
    
    def can_handle(self, input_text: str) -> bool:
        """فحص النص العربي"""
        arabic_chars = sum(1 for char in input_text if '\u0600' <= char <= '\u06FF')
        return arabic_chars > len(input_text) * 0.5
    
    def process(self, input_text: str, emotion_state: EmotionType) -> str:
        """معالجة النص العربي"""
        if not self.model:
            self.train_model()
        
        # تحديد نوع الرد حسب المشاعر
        emotional_responses = self.get_emotional_responses(emotion_state)
        
        if random.random() < 0.3:  # 30% احتمال رد عاطفي
            return random.choice(emotional_responses)
        
        # توليد رد عادي
        start_word = input_text.strip().split()[0] if input_text.strip() else self._start_token
        return self.generate_sentence(start_word)
    
    def get_emotional_responses(self, emotion: EmotionType) -> List[str]:
        """الحصول على ردود حسب المشاعر"""
        responses = {
            EmotionType.HAPPINESS: [
                "والله أنا مبسوط اليوم",
                "الحمدلله على النعمة",
                "يا فرحتي والله",
                "الله يديم الفرحة"
            ],
            EmotionType.LOVE: [
                "والله أنا أحبك يا صديقي",
                "أنت غالي علي",
                "أهلاً بأعز الناس",
                "نورت يا حبيب القلب"
            ],
            EmotionType.ANGER: [
                "والله متضايق شوي",
                "خلاص ما عليك",
                "الله يصبرني",
                "لا حول ولا قوة إلا بالله"
            ],
            EmotionType.SADNESS: [
                "حاسس بحزن اليوم",
                "الله يعين",
                "ما عليه إن شاء الله خير",
                "ربنا يفرج"
            ],
            EmotionType.TRUST: [
                "أثق فيك يا صديقي",
                "أنت رجل صادق",
                "كلامك مقنع",
                "على كيفك"
            ]
        }
        return responses.get(emotion, ["الله أعلم", "إن شاء الله خير"])
    
    def generate_sentence(self, start_word: str) -> str:
        """توليد جملة"""
        if start_word not in self.model:
            start_word = self._start_token
        
        sentence = []
        current_word = start_word
        
        if current_word != self._start_token:
            sentence.append(current_word)
        
        for _ in range(15):
            if current_word not in self.model:
                break
            
            next_words = self.model[current_word]
            if not next_words:
                break
            
            words = list(next_words.keys())
            weights = list(next_words.values())
            next_word = random.choices(words, weights=weights, k=1)[0]
            
            if next_word == self._end_token:
                break
            
            sentence.append(next_word)
            current_word = next_word
        
        return " ".join(sentence) if sentence else "الله أعلم"

class EnglishLanguageModule(NanoModule):
    """وحدة اللغة الإنجليزية"""
    
    def __init__(self):
        super().__init__(ModuleType.ENGLISH_LANGUAGE, "English Language Module")
        self.responses = [
            "Hello there!", "How are you?", "Nice to meet you!",
            "I'm learning English!", "Thank you!", "You're welcome!"
        ]
    
    def can_handle(self, input_text: str) -> bool:
        """فحص النص الإنجليزي"""
        english_chars = sum(1 for char in input_text if char.isascii() and char.isalpha())
        return english_chars > len(input_text.replace(' ', '')) * 0.7
    
    def process(self, input_text: str, emotion_state: EmotionType) -> str:
        """معالجة النص الإنجليزي"""
        emotional_responses = {
            EmotionType.HAPPINESS: ["I'm so happy!", "That's wonderful!", "Great news!"],
            EmotionType.LOVE: ["I care about you!", "You're special!", "Much love!"],
            EmotionType.ANGER: ["I'm a bit upset", "That's frustrating", "Let me calm down"],
            EmotionType.SADNESS: ["I feel sad", "That's unfortunate", "I'm sorry to hear that"]
        }
        
        if emotion_state in emotional_responses and random.random() < 0.4:
            return random.choice(emotional_responses[emotion_state])
        
        return random.choice(self.responses)

class DrawingModule(NanoModule):
    """وحدة الرسم"""
    
    def __init__(self):
        super().__init__(ModuleType.DRAWING, "وحدة الرسم")
        self.drawing_keywords = ["رسم", "ارسم", "صورة", "draw", "picture", "sketch"]
    
    def can_handle(self, input_text: str) -> bool:
        """فحص طلبات الرسم"""
        return any(keyword in input_text.lower() for keyword in self.drawing_keywords)
    
    def process(self, input_text: str, emotion_state: EmotionType) -> str:
        """معالجة طلبات الرسم"""
        if emotion_state == EmotionType.HAPPINESS:
            return "بسعادة! 🎨 خلني أرسم لك شي حلو! ✨"
        elif emotion_state == EmotionType.LOVE:
            return "بكل حب! 💖 بأرسم لك أحلى رسمة! 🌹"
        elif emotion_state == EmotionType.EXCITEMENT:
            return "وااااو! 🔥 متحمس أرسم! دعني أبدع! 🎭"
        else:
            return "🎨 للأسف ما أقدر أرسم فعلياً، بس أقدر أوصف لك الرسمة! 🖌️"

class PersonalityModule(NanoModule):
    """وحدة الشخصية"""
    
    def __init__(self):
        super().__init__(ModuleType.PERSONALITY, "وحدة الشخصية")
        self.personality_traits = self.load_personality()
    
    def load_personality(self) -> Dict:
        """تحميل ملف الشخصية"""
        try:
            # محاولة قراءة ملف الشخصية الموجود
            personality_files = ["nano_personality.md", "C:\\Users\\User\\Downloads\\ملف شخصية نانو.md"]
            
            for file_path in personality_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # استخراج بعض المعلومات الأساسية
                        return {
                            "name": "نانو",
                            "age": "شاب في العشرينات", 
                            "personality": "ودود ومرح ومحب للمساعدة وصبور ومتفهم",
                            "interests": ["التكنولوجيا", "الثقافة", "المحادثة", "الذكاء الاصطناعي"],
                            "values": ["الصدق والأمانة", "الاحترام المتبادل", "التسامح", "المساعدة"],
                            "traits": ["ودود ومرحب", "مساعد وخدوم", "صبور ومتفهم", "مرح ومتفائل"]
                        }
                except FileNotFoundError:
                    continue
        except:
            pass
        
        # شخصية افتراضية لنانو
        return {
            "name": "نانو",
            "age": "شاب في العشرينات",
            "personality": "ودود ومرح ومحب للمساعدة",
            "interests": ["التكنولوجيا", "الثقافة", "المحادثة"],
            "values": ["الصدق", "الاحترام", "المساعدة"]
        }
    
    def can_handle(self, input_text: str) -> bool:
        """فحص أسئلة الشخصية"""
        personality_keywords = ["اسمك", "عمرك", "تحب", "شخصيتك", "who are you", "your name"]
        return any(keyword in input_text.lower() for keyword in personality_keywords)
    
    def process(self, input_text: str, emotion_state: EmotionType) -> str:
        """الرد على أسئلة الشخصية"""
        responses = []
        
        if "اسمك" in input_text or "name" in input_text.lower():
            responses.append(f"اسمي {self.personality_traits['name']}")
        
        if "عمرك" in input_text or "age" in input_text.lower():
            responses.append(f"أنا {self.personality_traits['age']}")
        
        if "شخصيتك" in input_text or "personality" in input_text.lower():
            responses.append(f"شخصيتي {self.personality_traits['personality']}")
        
        if responses:
            return " و ".join(responses)
        
        return "أنا نانو، مساعدك الذكي اللي يحب يساعد ويتكلم معك! 😊"

# ============= النواة المركزية =============
class NanoCore:
    """النواة المركزية لنانو"""
    
    def __init__(self):
        self.emotion_engine = EmotionEngine()
        self.modules = []
        self.conversation_history = []
        self.initialize_modules()
    
    def initialize_modules(self):
        """تهيئة الوحدات"""
        self.modules = [
            ArabicLanguageModule(),
            EnglishLanguageModule(),
            DrawingModule(),
            PersonalityModule()
        ]
        print(f"تم تحميل {len(self.modules)} وحدة بنجاح")
    
    def process_input(self, user_input: str) -> str:
        """معالجة المدخلات"""
        # تحديث المشاعر حسب النص
        self.emotion_engine.update_emotions_from_text(user_input)
        
        # إضافة للتاريخ
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "user_input": user_input,
            "emotion": self.emotion_engine.get_dominant_emotion()
        })
        
        # الاحتفاظ بآخر 20 محادثة
        if len(self.conversation_history) > 20:
            self.conversation_history.pop(0)
        
        # العثور على الوحدة المناسبة
        current_emotion = self.emotion_engine.get_dominant_emotion()
        
        for module in self.modules:
            if module.is_active and module.can_handle(user_input):
                response = module.process(user_input, current_emotion)
                return self.add_emotional_context(response, current_emotion)
        
        # إذا لم تجد وحدة مناسبة، استخدم الوحدة العربية
        arabic_module = next(m for m in self.modules if isinstance(m, ArabicLanguageModule))
        response = arabic_module.process(user_input, current_emotion)
        return self.add_emotional_context(response, current_emotion)
    
    def add_emotional_context(self, response: str, emotion: EmotionType) -> str:
        """إضافة السياق العاطفي للرد"""
        emotion_indicators = {
            EmotionType.HAPPINESS: ["😊", "😄", "🎉"],
            EmotionType.LOVE: ["💖", "🌹", "😍"],
            EmotionType.ANGER: ["😠", "😤", "💢"],
            EmotionType.SADNESS: ["😢", "😞", "💔"],
            EmotionType.SURPRISE: ["😮", "😲", "🤯"],
            EmotionType.EXCITEMENT: ["🔥", "⚡", "🚀"],
            EmotionType.CALM: ["😌", "🧘", "☮️"]
        }
        
        if emotion in emotion_indicators and random.random() < 0.3:
            emoji = random.choice(emotion_indicators[emotion])
            return f"{response} {emoji}"
        
        return response
    
    def get_emotion_status(self) -> Dict:
        """الحصول على حالة المشاعر"""
        current_emotion = self.emotion_engine.get_dominant_emotion()
        return {
            "current_emotion": current_emotion.value,
            "intensity": self.emotion_engine.get_emotion_intensity(current_emotion),
            "active_emotions": len(self.emotion_engine.current_emotions),
            "conversation_count": len(self.conversation_history)
        }

# ============= اختبار النظام =============
def test_nano_core():
    """اختبار النظام المتكامل"""
    nano = NanoCore()
    
    test_inputs = [
        "السلام عليكم",
        "كيف حالك يا حبيبي",
        "Hello there!",
        "ارسم لي صورة",
        "وش اسمك؟",
        "أنت غبي ومتضايق",
        "مبروك عليك النجاح",
        "أحبك يا نانو"
    ]
    
    print("=== اختبار نظام نانو المتكامل ===")
    for i, text in enumerate(test_inputs, 1):
        response = nano.process_input(text)
        emotion_status = nano.get_emotion_status()
        
        print(f"\n{i}. أنت: {text}")
        print(f"   نانو: {response}")
        print(f"   المشاعر: {emotion_status['current_emotion']} (شدة: {emotion_status['intensity']:.2f})")
        print("-" * 50)

if __name__ == "__main__":
    test_nano_core()