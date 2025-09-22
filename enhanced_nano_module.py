# enhanced_nano_module.py - نسخة محسنة من نانو للردود المنطقية
import json
import random
import re
from riyadh_dialect_generative_module import RiyadhDialectGenerative

class EnhancedNano(RiyadhDialectGenerative):
    """
    نسخة محسنة من نانو مع ردود أكثر منطقية
    """
    def __init__(self, model_path="riyadh_model.json"):
        super().__init__(model_path)
        self.context_patterns = {
            # أنماط الأسئلة والردود المناسبة
            "greetings": {
                "patterns": ["هلا", "صباح", "مساء", "السلام", "كيف"],
                "responses": [
                    "هلا والله شخبارك", 
                    "الحمدلله كيفك انت",
                    "صباح الخير كيف النوم",
                    "مساء الخير كيف يومك",
                    "أهلين وسهلين"
                ]
            },
            "questions": {
                "patterns": ["وش", "ليش", "متى", "وين", "كيف", "من"],
                "responses": [
                    "والله ما ادري",
                    "الله أعلم يا خوي",
                    "دعني أفكر شوي",
                    "سؤال حلو الصراحة"
                ]
            },
            "food": {
                "patterns": ["اكل", "طعام", "فطار", "غدا", "عشا", "جوعان", "بيتزا", "كبسة"],
                "responses": [
                    "والله انا بعد جوعان",
                    "كبسة لحم اليوم طبخت الوالدة",
                    "البيتزا فكرة حلوة نطلب",
                    "اكل البيت أطيب"
                ]
            },
            "work": {
                "patterns": ["شغل", "عمل", "وظيفة", "دوام", "مكتب"],
                "responses": [
                    "الشغل متعب بس لازم",
                    "الدوام اليوم كان ضغط",
                    "الله يعينك على الشغل",
                    "نشكر الله على الرزق"
                ]
            },
            "weather": {
                "patterns": ["جو", "طقس", "حر", "برد", "مطر", "شمس"],
                "responses": [
                    "الجو اليوم بطل",
                    "الحر لا يطاق",
                    "البرد احسن من الحر",
                    "الله يرحمنا بنسمة هوا"
                ]
            }
        }
    
    def get_context_response(self, user_input):
        """
        إيجاد رد مناسب حسب السياق
        """
        user_input = user_input.lower()
        
        for context, data in self.context_patterns.items():
            for pattern in data["patterns"]:
                if pattern in user_input:
                    return random.choice(data["responses"])
        
        return None
    
    def generate_smart_response(self, user_input=""):
        """
        توليد رد ذكي حسب السياق
        """
        # أولاً نحاول إيجاد رد مناسب حسب السياق
        context_response = self.get_context_response(user_input)
        if context_response:
            return context_response
        
        # إذا لم نجد، نستخدم الطريقة التقليدية
        start_word = user_input.strip().split()[0] if user_input.strip() else None
        response = self.generate_sentence(start_word=start_word)
        
        # تحسين الرد إذا كان غير منطقي
        if self.is_response_logical(response, user_input):
            return response
        else:
            # نحاول مرة أخرى
            fallback_responses = [
                "والله ما فهمت عليك",
                "قول لي مرة ثانية",
                "وش قصدك بالضبط",
                "شرح لي أكثر",
                "الله أعلم"
            ]
            return random.choice(fallback_responses)
    
    def is_response_logical(self, response, user_input):
        """
        فحص إذا كان الرد منطقي أو لا
        """
        # فحوصات بسيطة للمنطقية
        if len(response.split()) < 2:
            return False
        
        # إذا كان السؤال عن الطعام والرد عن شي آخر تماماً
        food_words = ["اكل", "طعام", "جوعان", "بيتزا", "كبسة"]
        if any(word in user_input.lower() for word in food_words):
            if not any(word in response.lower() for word in food_words + ["والله", "حلو", "زين"]):
                return False
        
        return True

# دالة للاختبار السريع
def test_enhanced_nano():
    """اختبار النموذج المحسن"""
    nano = EnhancedNano()
    nano.train()
    
    test_inputs = [
        "هلا والله",
        "كيف صحتك",
        "وش اكلك اليوم", 
        "الشغل متعب",
        "الجو حار",
        "وين رايح"
    ]
    
    print("=== اختبار نانو المحسن ===")
    for user_input in test_inputs:
        response = nano.generate_smart_response(user_input)
        print(f"أنت: {user_input}")
        print(f"نانو: {response}")
        print("-" * 30)

if __name__ == "__main__":
    test_enhanced_nano()