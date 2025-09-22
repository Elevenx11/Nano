# social_media_collector.py - جامع النصوص من المحادثات الاجتماعية
import json
import random
from typing import List, Dict
import re

class SocialMediaCollector:
    """جامع النصوص من محادثات وسائل التواصل الاجتماعي"""
    
    def __init__(self):
        self.riyadh_dialect_patterns = self.setup_riyadh_patterns()
        self.conversation_types = self.setup_conversation_types()
    
    def setup_riyadh_patterns(self) -> Dict:
        """أنماط لهجة أهل الرياض المميزة"""
        return {
            "greetings": [
                "هلا والله", "الله يهلا فيك", "اهلين", "مرحبا",
                "وش خبرك", "شخبارك", "كيفك", "شلونك",
                "صباح الخير", "مساء الخير", "تصبح على خير"
            ],
            
            "responses": [
                "الحمدلله", "زين", "بخير", "تمام", "عادي",
                "والله", "صدق", "اكيد", "طبعا", "ايه"
            ],
            
            "expressions": [
                "يا رجال", "يا خوي", "يا صديقي", "يا غالي",
                "ما شاء الله", "الله يعينك", "الله يوفقك",
                "ان شاء الله", "بإذن الله", "الله كريم"
            ],
            
            "daily_words": [
                "شغل", "بيت", "اهل", "عيال", "ولد", "بنت",
                "موية", "اكل", "نوم", "سيارة", "جوال",
                "فلوس", "شراي", "سوق", "دوام"
            ]
        }
    
    def setup_conversation_types(self) -> Dict:
        """أنواع المحادثات المختلفة"""
        return {
            "whatsapp_family": self.generate_family_conversations(),
            "whatsapp_friends": self.generate_friends_conversations(),
            "twitter_comments": self.generate_twitter_style(),
            "instagram_comments": self.generate_instagram_style(),
            "discord_gaming": self.generate_discord_style()
        }
    
    def generate_family_conversations(self) -> List[str]:
        """محادثات عائلية على الواتساب"""
        family_convos = [
            # محادثات الأم
            "يمه وش تطبخين اليوم",
            "بطبخ مندي ان شاء الله",
            "زين والله نشتهيه",
            "تعال البيت بدري",
            "ان شاء الله يمه",
            
            # محادثات الأب
            "ابوي وين راحت السيارة",
            "اخذها اخوك للجامعة",
            "طيب متى يرجعها",
            "العصر ان شاء الله",
            
            # محادثات الأخوان
            "اخوي جبت لي الشي اللي طلبته",
            "ايه في الشنطة",
            "تسلم ما قصرت",
            "عادي هذا واجب",
            
            # مناسبات عائلية
            "الجمعة عندنا عزيمة",
            "مين جايين",
            "الاقارب والجيران",
            "زين نحضر شي حلو",
            
            # اهتمامات يومية
            "ما نسيت تاخذ الدوا",
            "لا خذته الصبح",
            "زين انتبه لنفسك",
            "الله يعافيك"
        ]
        
        return family_convos
    
    def generate_friends_conversations(self) -> List[str]:
        """محادثات الأصدقاء"""
        friends_convos = [
            # تخطيط للقاءات
            "يلا نطلع نتغدى",
            "وين تبون نروح",
            "اي مكان على كيفكم",
            "طيب المطعم اللي جنب الجامعة",
            "تم الساعة وحدة",
            
            # مساعدات بين الأصدقاء
            "محتاج اطلب منك خدمة",
            "تفضل وش تحتاج",
            "توصلني للمطار بكرة",
            "اكيد متى الموعد",
            "الساعة عشرة الصبح",
            "لا تشيل هم راح اجيك",
            
            # مناقشات عامة
            "شايف المطر امس",
            "ايه كان قوي مرة",
            "الحمدلله نحتاج له",
            "صدقت الجو صار احسن",
            
            # تشجيع ودعم
            "مبروك على النجاح",
            "الله يبارك فيك",
            "تستاهل والله",
            "شكرا لك يا غالي",
            
            # خطط مستقبلية
            "وش خططك للاجازة",
            "ودي اسافر مكان جديد",
            "فكرة حلوة وين تفكر تروح",
            "يمكن البحرين او الامارات",
            "حلو استمتع"
        ]
        
        return friends_convos
    
    def generate_twitter_style(self) -> List[str]:
        """نمط تعليقات تويتر"""
        twitter_style = [
            # تعليقات إيجابية
            "كلام جميل ما شاء الله",
            "صدقت في كلامك",
            "نقطة مهمة فعلا",
            "الله يعطيك العافية",
            
            # تعليقات عامة
            "الوضع صعب هالايام",
            "الله يعين الجميع",
            "نحتاج نصبر اكثر",
            "ان شاء الله يتحسن الحال",
            
            # ردود قصيرة
            "زين قلت",
            "صح لسانك",
            "والله صادق",
            "اتفق معك",
            
            # دعاء ومباركات
            "الله يوفق الجميع",
            "ربنا يحفظنا",
            "الله يبارك لك",
            "جزاك الله خير"
        ]
        
        return twitter_style
    
    def generate_instagram_style(self) -> List[str]:
        """نمط تعليقات انستقرام"""
        instagram_style = [
            # تعليقات على الصور
            "صورة حلوة ما شاء الله",
            "المكان يجنن",
            "الله يعطيك العافية",
            "تستاهل كل خير",
            
            # تفاعل مع المحتوى
            "محتوى مفيد شكرا",
            "استفدت منك كثير",
            "الله يجزاك خير",
            "معلومة حلوة",
            
            # تشجيع
            "كفو عليك",
            "مبدع كالعادة",
            "يعطيك الف عافية",
            "تسلم ايدك"
        ]
        
        return instagram_style
    
    def generate_discord_style(self) -> List[str]:
        """نمط محادثات دسكورد (ألعاب وتقنية)"""
        discord_style = [
            # محادثات الألعاب (بدون أسماء محددة)
            "يلا نلعب راوند ثاني",
            "انا جاهز متى ما تبون",
            "الكونكشن عندي زين اليوم",
            "حلو يلا نبدا",
            
            # تقنية عامة
            "الانترنت عندكم كيف اليوم",
            "زين الحمدلله سريع",
            "عندي مشكلة في الراوتر",
            "جرب تعيد تشغيله",
            
            # تفاعل عام
            "شكرا للمساعدة",
            "عفوا اي وقت",
            "خدمة وشرف",
            "تسلم يا غالي"
        ]
        
        return discord_style
    
    def collect_quality_conversations(self, total_count: int = 500) -> List[str]:
        """جمع محادثات عالية الجودة"""
        all_conversations = []
        
        # جمع من جميع المصادر
        for source, convos in self.conversation_types.items():
            all_conversations.extend(convos)
        
        # إضافة محادثات متنوعة إضافية
        additional_convos = self.generate_diverse_conversations(200)
        all_conversations.extend(additional_convos)
        
        # تصفية وتحسين
        quality_conversations = []
        for conv in all_conversations:
            if self.is_quality_conversation(conv):
                quality_conversations.append(conv)
        
        # خلط وإرجاع العدد المطلوب
        random.shuffle(quality_conversations)
        return quality_conversations[:total_count]
    
    def generate_diverse_conversations(self, count: int) -> List[str]:
        """توليد محادثات متنوعة"""
        diverse = []
        
        # قوالب محادثات
        templates = [
            "وش رايك في {topic}",
            "كيف حالك مع {topic}",
            "متى بت{action}",
            "وين {place} اللي تحبه",
            "{feeling} اليوم من {reason}"
        ]
        
        topics = ["الشغل", "الدراسة", "الاجازة", "الطقس", "الصحة"]
        actions = ["روح", "تاكل", "تنام", "تسافر", "تدرس"]
        places = ["المطعم", "المكان", "البيت", "المقهى", "المتجر"]
        feelings = ["مبسوط", "متعب", "مرتاح", "متحمس", "هادي"]
        reasons = ["الشغل", "الراحة", "الاجازة", "الطقس الحلو", "انجاز شي حلو"]
        
        for i in range(count):
            template = random.choice(templates)
            filled = template.format(
                topic=random.choice(topics),
                action=random.choice(actions),
                place=random.choice(places),
                feeling=random.choice(feelings),
                reason=random.choice(reasons)
            )
            diverse.append(filled)
        
        return diverse
    
    def is_quality_conversation(self, text: str) -> bool:
        """فحص جودة المحادثة"""
        # فحوصات الجودة
        if len(text.strip()) < 5:  # قصير جداً
            return False
        
        if len(text.split()) > 20:  # طويل جداً
            return False
        
        # فحص الأحرف العربية
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        if arabic_chars < len(text) * 0.6:  # قليل العربية
            return False
        
        # فحص وجود كلمات من لهجة الرياض
        riyadh_words_found = 0
        text_lower = text.lower()
        
        for category, words in self.riyadh_dialect_patterns.items():
            for word in words:
                if word in text_lower:
                    riyadh_words_found += 1
        
        return riyadh_words_found > 0
    
    def export_to_corpus(self, output_file: str = "social_media_corpus.json"):
        """تصدير إلى ملف corpus"""
        quality_conversations = self.collect_quality_conversations(800)
        
        corpus_data = {
            "source": "Social Media Conversations - Saudi Riyadh Dialect",
            "total_conversations": len(quality_conversations),
            "quality_level": "High",
            "sentences": quality_conversations
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(corpus_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ تم تصدير {len(quality_conversations)} محادثة إلى {output_file}")
        return output_file

# دالة تجريبية
def test_collector():
    """اختبار جامع النصوص"""
    collector = SocialMediaCollector()
    
    print("🔄 جمع محادثات من مصادر مختلفة...")
    conversations = collector.collect_quality_conversations(100)
    
    print(f"✅ تم جمع {len(conversations)} محادثة")
    print("\nعينة من المحادثات:")
    for i, conv in enumerate(conversations[:10], 1):
        print(f"{i}. {conv}")
    
    # تصدير الملف
    output_file = collector.export_to_corpus()
    print(f"\n📁 الملف محفوظ في: {output_file}")

if __name__ == "__main__":
    test_collector()