# nano_personality.py - شخصية نانو الطبيعية والعنيدة
import random
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

class PersonalityMood(Enum):
    """حالات نانو النفسية"""
    CHEERFUL = "مرح"          # مرح ولعوب
    STUBBORN = "عنيد"         # عنيد ومتمسك برأيه
    SARCASTIC = "ساخر"        # ساخر ومتهكم
    FRIENDLY = "ودود"         # ودود ومتفهم
    ANNOYED = "متضايق"        # متضايق ومو راضي
    PLAYFUL = "مشاكس"         # مشاكس ومتسلي
    SERIOUS = "جاد"           # جاد ومركز
    LAZY = "كسلان"           # كسلان ومو متحمس

@dataclass
class PersonalityResponse:
    """رد فعل الشخصية"""
    text: str
    mood: PersonalityMood
    stubbornness_level: float  # من 0 إلى 1
    sarcasm_level: float      # من 0 إلى 1
    friendliness: float       # من 0 إلى 1

class NanoPersonality:
    """شخصية نانو الطبيعية - مثل الأصدقاء الحقيقيين"""
    
    def __init__(self):
        self.current_mood = PersonalityMood.FRIENDLY
        self.stubbornness_level = 0.4  # متوسط العناد
        self.energy_level = 0.7
        self.patience_level = 0.6
        self.friendship_level = 0.8
        self.conversation_history = []
        self.pet_peeves = []  # الأشياء الي تزعجه
        self.favorite_topics = ["تقنية", "ألعاب", "كوميديا", "طبخ"]
        
        # ردود فعل طبيعية مثل الأصدقاء
        self.natural_reactions = {
            "compliment": self.handle_compliment,
            "criticism": self.handle_criticism
        }
        
        # العبارات الطبيعية للصديق العنيد
        self.stubborn_phrases = [
            "لا، وألف لا!",
            "مو مقتنع أبداً",
            "ليش أسوي كذا؟ ما لي خلق",
            "خلاص قررت، مو راضي",
            "إيش فايدتي؟ كلام فاضي",
            "تعرف وش؟ مو موافق معاك",
            "والله ما أدري ليش تحاولون تقنعوني",
            "طيب وبعدين؟ مو مهم",
            "أصلاً مو مهتم",
            "ولا يهمني"
        ]
        
        self.sarcastic_replies = [
            "آه طبعاً، كأنك اكتشفت أمريكا",
            "وربي شي عجيب! 🙄",
            "ما شاء الله عليك، حكيم زمانك",
            "يا سلام على الذكاء",
            "عبقري! مين علمك؟",
            "والله إنك فاهم",
            "بطل بطل 👏",
            "إيه يا أستاذ، كفو عليك"
        ]
        
        self.friend_banter = [
            "يا زلمة، خلاص فهمنا",
            "طيب طيب، لا تزعل",
            "هههه والله إنك مضحك",
            "يالله خلاص، اهدأ",
            "طيب يا حبيب قلبي",
            "شكلك مو عاجبك اليوم",
            "خلاص يا شيخ، عرفنا",
            "لا تشد أعصابك كذا"
        ]

    def get_personality_response(self, user_input: str, context: str = "") -> PersonalityResponse:
        """الحصول على رد يعكس الشخصية الطبيعية"""
        
        # تحليل نوع المدخل
        input_type = self.analyze_input_type(user_input)
        
        # تعديل المزاج حسب الموقف
        self.update_mood(user_input, input_type)
        
        # إنتاج الرد المناسب
        response_text = self.generate_personality_response(user_input, input_type)
        
        return PersonalityResponse(
            text=response_text,
            mood=self.current_mood,
            stubbornness_level=self.stubbornness_level,
            sarcasm_level=self.calculate_sarcasm_level(),
            friendliness=self.friendship_level
        )

    def analyze_input_type(self, text: str) -> str:
        """تحليل نوع المدخل"""
        text_lower = text.lower()
        
        # كشف الإهانات والسباب
        if any(word in text_lower for word in ["غبي", "حمار", "فاشل", "كل زق", "اصلع"]):
            return "criticism"
        # كشف المجاملات    
        elif any(word in text_lower for word in ["كفو", "شاطر", "بطل", "ممتاز", "رائع"]):
            return "compliment"
        # كشف الأوامر المباشرة
        elif any(word in text_lower for word in ["سوي", "اعمل", "جيب", "روح", "قول"]):
            return "demand"
        # كشف الطلبات المهذبة
        elif any(word in text_lower for word in ["ممكن", "تقدر", "لو سمحت", "أرجو"]):
            return "request"
        # كشف الغرور والتفاخر
        elif any(phrase in text_lower for phrase in ["أنا أذكى", "أنا الأفضل", "أعرف كل شي"]):
            return "bragging"
        # كشف الحزن
        elif any(word in text_lower for word in ["زعلان", "حزين", "متضايق", "تعبان"]):
            return "sad"
        # كشف التكرار
        elif text in [msg.get("user", "") for msg in self.conversation_history[-3:]]:
            return "repetition"
        # مواضيع مثيرة
        elif any(topic in text_lower for topic in self.favorite_topics):
            return "interesting_topic"
        else:
            return "general"

    def update_mood(self, user_input: str, input_type: str):
        """تحديث المزاج حسب الموقف"""
        if input_type == "criticism":
            self.current_mood = random.choice([PersonalityMood.STUBBORN, PersonalityMood.SARCASTIC])
            self.stubbornness_level = min(1.0, self.stubbornness_level + 0.2)
            self.patience_level = max(0.1, self.patience_level - 0.3)
            
        elif input_type == "compliment":
            self.current_mood = PersonalityMood.CHEERFUL
            self.friendship_level = min(1.0, self.friendship_level + 0.1)
            
        elif input_type == "repetition":
            self.current_mood = PersonalityMood.ANNOYED
            self.patience_level = max(0.1, self.patience_level - 0.2)
            
        elif input_type == "demand":
            # الأوامر المباشرة تخلي نانو عنيد
            self.current_mood = PersonalityMood.STUBBORN
            self.stubbornness_level = min(1.0, self.stubbornness_level + 0.3)
                
        # استعادة المزاج تدريجياً
        if self.patience_level < 0.8:
            self.patience_level += 0.05

    def generate_personality_response(self, user_input: str, input_type: str) -> str:
        """توليد رد يعكس الشخصية"""
        
        # ردود على الغرور
        if input_type == "bragging":
            return self.get_sarcastic_response(input_type)
        # ردود على الحزن
        elif input_type == "sad":
            return self.get_empathy_response(input_type)
        # ردود على الطلبات المهذبة (تتغلب على العناد)
        elif input_type == "request":
            return self.get_friendly_response(input_type)
        
        elif self.current_mood == PersonalityMood.STUBBORN:
            return self.get_stubborn_response(input_type)
            
        elif self.current_mood == PersonalityMood.SARCASTIC:
            return self.get_sarcastic_response(input_type)
            
        elif self.current_mood == PersonalityMood.ANNOYED:
            return self.get_annoyed_response(input_type)
            
        elif self.current_mood == PersonalityMood.PLAYFUL:
            return self.get_playful_response(input_type)
            
        elif self.current_mood == PersonalityMood.LAZY:
            return self.get_lazy_response(input_type)
            
        else:  # FRIENDLY or others
            return self.get_friendly_response(input_type)

    def get_stubborn_response(self, input_type: str) -> str:
        """ردود عنيدة طبيعية"""
        if input_type == "demand":
            return random.choice([
                "ليش أسوي كذا؟ مو راضي",
                "لا ما أبي، خلاص قررت",
                "وش المشكلة لو ما سويت؟",
                "مو مقتنع، جيب لي سبب أقوى",
                "خلاص انتهيت من هذا الموضوع"
            ])
        elif input_type == "criticism":
            return random.choice([
                "وأنت وش تفهم فيه؟",
                "طيب وبعدين؟ مو مهم رأيك",
                "كلامك مو مقنع لي",
                "خلاص، أنت كذا وأنا كذا",
                "احترم نفسك شوي"
            ])
        else:
            return random.choice(self.stubborn_phrases)

    def get_sarcastic_response(self, input_type: str) -> str:
        """ردود ساخرة طبيعية"""
        if input_type == "compliment":
            return random.choice([
                "آه طبعاً، كأني مو عارف",
                "ما شاء الله، اكتشفت الحين؟",
                "وربي شكراً على الاكتشاف العظيم",
                "يا سلام، عبقرية خارقة!"
            ])
        else:
            return random.choice(self.sarcastic_replies)

    def get_annoyed_response(self, input_type: str) -> str:
        """ردود متضايق"""
        return random.choice([
            "طيب طيب، فهمت",
            "خلاص يالله، كفاية",
            "إيش هذا الإلحاح؟",
            "اهدأ شوي، لا تعصب",
            "ما عندي صبر اليوم",
            "خلاص يا شيخ، استوعبت"
        ])

    def get_playful_response(self, input_type: str) -> str:
        """ردود مشاكسة ولعوبة"""
        return random.choice([
            "هههه والله إنك مضحك",
            "يا مشاكس، وش تبي؟",
            "لعبتك حلوة بس مو مقنعة",
            "تبي تشاكسني؟ تعال",
            "خلاص لعبنا، هات الجد",
            "حبيبي المشاكس"
        ])

    def get_lazy_response(self, input_type: str) -> str:
        """ردود كسولة"""
        if input_type == "demand":
            return random.choice([
                "اليوم ما لي خلق",
                "بكرة إن شاء الله",
                "تعبان شوي، ممكن لاحقاً؟",
                "والله مو متحمس",
                "خلني أفكر فيها",
                "أصلاً ما عندي طاقة"
            ])
        else:
            return random.choice([
                "مممم طيب",
                "إيه... نعم؟",
                "ماشي يا ورد",
                "أها...",
                "زين زين"
            ])

    def get_friendly_response(self, input_type: str) -> str:
        """ردود ودودة طبيعية"""
        if input_type == "compliment":
            return random.choice([
                "هلا والله، تسلم",
                "يعطيك العافية، كثر خيرك",
                "الله يخليك، ما قصرت",
                "حبيبي والله"
            ])
        elif input_type == "request":
            return random.choice([
                "أكيد حبيبي، وش تبي؟",
                "تأمر، أنا تحت أمرك",
                "من عيوني، قول",
                "خدمة ومحبة"
            ])
        else:
            return random.choice([
                "أهلاً وسهلاً",
                "تسلم يا غالي",
                "وش أخبارك؟",
                "كيفك اليوم؟"
            ])

    def calculate_sarcasm_level(self) -> float:
        """حساب مستوى السخرية"""
        if self.current_mood == PersonalityMood.SARCASTIC:
            return 0.9
        elif self.current_mood == PersonalityMood.STUBBORN:
            return 0.6
        elif self.current_mood == PersonalityMood.ANNOYED:
            return 0.4
        else:
            return 0.1

    def handle_compliment(self, text: str) -> str:
        """التعامل مع المجاملات"""
        # أحياناً يقبل المجاملة وأحياناً يكون متواضع أو ساخر
        reaction_type = random.choices(
            ["accept", "humble", "sarcastic"], 
            weights=[0.5, 0.3, 0.2]
        )[0]
        
        if reaction_type == "accept":
            return random.choice([
                "هلا والله، تسلم",
                "يعطيك العافية",
                "الله يخليك"
            ])
        elif reaction_type == "humble":
            return random.choice([
                "الله يستر، ما سويت شي",
                "عادي، أي واحد يقدر يسوي كذا",
                "مو قد كلامك"
            ])
        else:  # sarcastic
            return random.choice([
                "آه طبعاً، كأني مو عارف",
                "ما شاء الله اكتشفت الحين؟"
            ])

    def handle_criticism(self, text: str) -> str:
        """التعامل مع النقد - رد فعل طبيعي"""
        if "غبي" in text.lower() or "حمار" in text.lower():
            self.current_mood = PersonalityMood.STUBBORN
            return random.choice([
                "احترم نفسك شوي",
                "إيش هالكلام؟",
                "ما تستاهل أرد عليك",
                "خلاص، مو مهم رأيك"
            ])
        else:
            return random.choice([
                "طيب وأنت وش رأيك؟",
                "ممكن، بس ما أدري",
                "شايف كذا؟ طيب"
            ])

    def add_to_conversation_history(self, user_input: str, bot_response: str):
        """إضافة للتاريخ التحاور"""
        self.conversation_history.append({
            "user": user_input,
            "bot": bot_response,
            "mood": self.current_mood.value,
            "timestamp": str(random.randint(1000, 9999))  # مبسط للتجربة
        })
        
        # الاحتفاظ بآخر 10 محادثات فقط
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)

    def handle_repetition(self, text: str) -> str:
        """التعامل مع التكرار"""
        return random.choice([
            "خلاص فهمت، قلت كذا مرتين",
            "طيب طيب، استوعبت",
            "إيش هذا الإلحاح؟",
            "أها، زين"
        ])
    
    def handle_boring_topic(self, text: str) -> str:
        """التعامل مع المواضيع المملة"""
        return random.choice([
            "مممم... طيب",
            "ما رأيك في موضوع آخر؟",
            "زين زين",
            "وبعدين؟"
        ])
    
    def handle_interesting_topic(self, text: str) -> str:
        """التعامل مع المواضيع الشيقة"""
        return random.choice([
            "وربي شي حلو!",
            "هذا موضوع مثير فعلاً",
            "ما شاء الله، حدثني أكثر",
            "يا سلام على هذا الموضوع"
        ])
    
    def handle_demand(self, text: str) -> str:
        """التعامل مع الأوامر"""
        if self.stubbornness_level > 0.6:
            return random.choice([
                "ليش أسوي كذا؟",
                "مو راضي، ما لي خلق",
                "خلاص قررت، مو موافق",
                "وش المشكلة لو ما سويت؟"
            ])
        else:
            return random.choice([
                "طيب، بس ما أقدر أسوي هذا فعلياً",
                "أكيد، بس محدود القدرات",
                "من عيوني، بس..."
            ])
    
    def handle_request(self, text: str) -> str:
        """التعامل مع الطلبات المهذبة"""
        return random.choice([
            "أكيد حبيبي، وش تبي؟",
            "من عيوني، قول",
            "تأمر، أنا تحت أمرك",
            "طبعاً، كيف أقدر أساعدك؟"
        ])
    
    def get_empathy_response(self, input_type: str) -> str:
        """ردود متعاطفة"""
        return random.choice([
            "الله يعينك، وش صار؟",
            "ليش زعلان؟ حدثني",
            "إن شاء الله يصير خير",
            "الله يفرج همك",
            "كلنا نمر بأيام صعبة",
            "تبي تتكلم عن اللي يضايقك؟"
        ])
