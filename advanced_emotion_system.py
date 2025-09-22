# advanced_emotion_system.py - نظام الذكاء العاطفي المتقدم والسياقي
import json
import re
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import math

@dataclass
class AdvancedEmotionResult:
    """نتيجة التحليل العاطفي المتقدم"""
    primary_emotion: str
    intensity: float
    confidence: float
    context_type: str
    subtle_indicators: List[str]
    insult_detected: bool
    sarcasm_detected: bool
    implicit_meaning: str
    cultural_context: str
    response_tone_needed: str

class AdvancedEmotionalIntelligence:
    """نظام الذكاء العاطفي المتقدم مع فهم السياق والتلميحات"""
    
    def __init__(self):
        self.insult_patterns = self.initialize_insult_patterns()
        self.compliment_patterns = self.initialize_compliment_patterns()
        self.sarcasm_indicators = self.initialize_sarcasm_indicators()
        self.contextual_emotion_map = self.initialize_contextual_emotions()
        self.cultural_sensitivity_map = self.initialize_cultural_sensitivity()
        self.implicit_meaning_detector = self.initialize_implicit_meanings()
        self.tone_patterns = self.initialize_tone_patterns()
        
    def initialize_insult_patterns(self) -> Dict[str, Dict]:
        """قاعدة بيانات الإهانات والسباب الصريحة والمبطنة"""
        return {
            # سباب صريحة
            "explicit_insults": {
                "direct": ["كل زق", "روح تموت", "يا حمار", "يا غبي", "يا أهبل", 
                          "خلاص كفاية", "اسكت", "ما تفهم", "انت مجنون"],
                "vulgar": ["تف عليك", "يا كلب", "يا حيوان", "الله يلعنك"],
                "intensity": 0.9,
                "response_type": "defensive_polite"
            },
            
            # إهانات مبطنة  
            "implicit_insults": {
                "appearance": ["يا أصلع", "يا قصير", "يا طويل", "يا أسود", "يا أحول",
                             "شكلك مو عادي", "وجهك مو حلو", "ما تعرف تلبس"],
                "intelligence": ["ما تفهم", "مخك صغير", "ما عندك عقل", "جاهل", 
                               "مو فاهم", "ما تقرا", "تفكيرك بسيط"],
                "personality": ["ما عندك شخصية", "ضعيف", "جبان", "كذاب", 
                              "حقير", "وضيع", "ما تستاهل"],
                "intensity": 0.7,
                "response_type": "hurt_defensive"
            },
            
            # تلميحات سلبية
            "negative_hints": {
                "dismissive": ["يالله", "طيب", "ماشي", "كما تشاء", "عادي"],
                "patronizing": ["مسكين", "حبيبي", "يا عزيزي", "الله يهديك"],
                "questioning": ["وش فيك", "ليش كذا", "إيش مشكلتك", "تمام كذا"],
                "intensity": 0.5,
                "response_type": "cautious_inquiry"
            }
        }
    
    def initialize_compliment_patterns(self) -> Dict[str, Dict]:
        """أنماط المجاملات والثناء"""
        return {
            "genuine_compliments": {
                "words": ["ممتاز", "رائع", "جميل", "حلو", "كفو", "بطل", "شاطر",
                         "الله يعطيك العافية", "ما شاء الله عليك", "تبارك الرحمن"],
                "intensity": 0.8,
                "response_type": "grateful_humble"
            },
            
            "sarcastic_compliments": {
                "patterns": ["ما شاء الله عليك", "كفو والله", "شاطر كثير", 
                           "الله يعطيك العافية"],
                "context_indicators": ["بعد خطأ", "مع تنهد", "بطريقة مستهزئة"],
                "intensity": 0.6,
                "response_type": "detect_sarcasm"
            }
        }
    
    def initialize_sarcasm_indicators(self) -> List[str]:
        """مؤشرات السخرية والاستهزاء"""
        return [
            # أدوات استهزاء
            "آه طبعاً", "أيوه صح", "ما شاء الله", "الله يعطيك العافية", 
            "كفو والله", "يا سلام", "وربي شي عجيب",
            
            # تعبيرات ساخرة
            "مبروك عليك", "هنيئاً لك", "تستاهل", "عقبالك",
            "أحسنت", "بارك الله فيك", "وفقك الله",
            
            # أسئلة استنكارية
            "وش هالشي", "إيش هذا", "جد كذا", "متأكد", 
            "تقصد جد", "وربي", "والله"
        ]
    
    def initialize_contextual_emotions(self) -> Dict[str, Dict]:
        """خريطة المشاعر السياقية"""
        return {
            "anger_triggers": {
                "injustice": ["ظلم", "مو عدل", "حرام", "ما يصير كذا"],
                "betrayal": ["خان", "كذب", "غدر", "طعن في الظهر"],
                "disrespect": ["استهزأ", "احتقر", "قلل احترام", "ما قدر"],
                "frustration": ["زهقت", "تعبت", "ما عاد أقدر", "خلاص كفى"]
            },
            
            "sadness_triggers": {
                "loss": ["فقد", "مات", "ضاع", "انتهى", "راح"],
                "loneliness": ["وحيد", "مهجور", "نسوني", "ما حد معي"],
                "disappointment": ["خيبة أمل", "ما توقعت", "صدمة", "انكسر قلبي"]
            },
            
            "joy_triggers": {
                "achievement": ["نجح", "حقق", "فاز", "أنجز", "وصل"],
                "surprise": ["مفاجأة", "ما توقعت", "فرحة عارمة"],
                "love": ["أحب", "عشق", "تزوج", "خطب", "حب"]
            }
        }
    
    def initialize_cultural_sensitivity(self) -> Dict[str, Dict]:
        """الحساسية الثقافية السعودية"""
        return {
            "family_honor": {
                "triggers": ["أهلك", "عيلتك", "أمك", "أبوك", "أختك"],
                "severity": "very_high",
                "response": "defend_family_honor"
            },
            
            "religious_sensitivity": {
                "triggers": ["الله", "الدين", "القرآن", "الرسول", "الصلاة"],
                "severity": "extreme",
                "response": "religious_respect"
            },
            
            "personal_appearance": {
                "triggers": ["أصلع", "قصير", "طويل", "سمين", "نحيف"],
                "severity": "medium",
                "response": "polite_deflection"
            }
        }
    
    def initialize_implicit_meanings(self) -> Dict[str, str]:
        """كاشف المعاني الضمنية"""
        return {
            # تعبيرات الموافقة المتردد
            "طيب": "reluctant_agreement",
            "ماشي": "passive_acceptance", 
            "كما تشاء": "dismissive_agreement",
            "عادي": "indifferent_response",
            
            # تعبيرات التشكيك
            "متأكد؟": "doubt_questioning",
            "جد كذا؟": "disbelief",
            "وربي؟": "seeking_confirmation",
            
            # تعبيرات التعب/الضجر
            "يالله": "impatience",
            "خلاص": "frustration_end",
            "كفاية": "enough_stop"
        }
    
    def initialize_tone_patterns(self) -> Dict[str, List[str]]:
        """أنماط النبرة والأسلوب"""
        return {
            "aggressive": ["!", "!!!", "كل زق", "اسكت", "روح"],
            "passive_aggressive": ["طيب", "ماشي", "كما تشاء", "عادي"],
            "sarcastic": ["ما شاء الله", "كفو", "يا سلام", "عجيب"],
            "dismissive": ["يالله", "خلاص", "كفاية", "طيب طيب"],
            "questioning": ["ليش", "إيش", "وش", "كيف", "متى"],
            "emotional": ["والله", "حبيبي", "يا قلبي", "روحي"]
        }
    
    def analyze_advanced_emotion(self, text: str, context: str = None) -> AdvancedEmotionResult:
        """التحليل العاطفي المتقدم والسياقي"""
        text_clean = text.strip().lower()
        
        # كشف الإهانات والسباب
        insult_result = self.detect_insults(text_clean)
        
        # كشف السخرية  
        sarcasm_result = self.detect_sarcasm(text_clean, context)
        
        # تحليل النبرة
        tone_analysis = self.analyze_tone(text_clean)
        
        # كشف المعنى الضمني
        implicit_meaning = self.detect_implicit_meaning(text_clean)
        
        # التحليل العاطفي الأساسي
        base_emotion = self.analyze_base_emotion(text_clean)
        
        # تحليل السياق الثقافي
        cultural_analysis = self.analyze_cultural_context(text_clean)
        
        # دمج النتائج
        final_emotion = self.synthesize_emotion_results(
            base_emotion, insult_result, sarcasm_result, 
            tone_analysis, cultural_analysis
        )
        
        # تحديد نوع الاستجابة المطلوبة
        response_tone = self.determine_response_tone(final_emotion, insult_result, cultural_analysis)
        
        return AdvancedEmotionResult(
            primary_emotion=final_emotion["emotion"],
            intensity=final_emotion["intensity"], 
            confidence=final_emotion["confidence"],
            context_type=tone_analysis["primary_tone"],
            subtle_indicators=final_emotion["indicators"],
            insult_detected=insult_result["detected"],
            sarcasm_detected=sarcasm_result["detected"],
            implicit_meaning=implicit_meaning,
            cultural_context=cultural_analysis["context"],
            response_tone_needed=response_tone
        )
    
    def detect_insults(self, text: str) -> Dict:
        """كشف الإهانات الصريحة والمبطنة"""
        result = {
            "detected": False,
            "type": None,
            "severity": 0.0,
            "specific_insults": []
        }
        
        for category, data in self.insult_patterns.items():
            if category == "intensity":
                continue
                
            for insult_type, patterns in data.items():
                if insult_type == "intensity" or insult_type == "response_type":
                    continue
                    
                for pattern in patterns:
                    if pattern in text:
                        result["detected"] = True
                        result["type"] = category
                        result["severity"] = max(result["severity"], data.get("intensity", 0.5))
                        result["specific_insults"].append(pattern)
        
        return result
    
    def detect_sarcasm(self, text: str, context: str = None) -> Dict:
        """كشف السخرية والاستهزاء"""
        result = {
            "detected": False,
            "indicators": [],
            "confidence": 0.0
        }
        
        sarcasm_count = 0
        for indicator in self.sarcasm_indicators:
            if indicator in text:
                result["indicators"].append(indicator)
                sarcasm_count += 1
        
        # تحليل إضافي للسياق
        if context:
            # إذا كان السياق إيجابي لكن التعبيرات توحي بالسخرية
            positive_words = ["ممتاز", "رائع", "جميل", "كفو"]
            negative_context = ["خطأ", "فشل", "مشكلة", "سيء"]
            
            has_positive = any(word in text for word in positive_words)
            has_negative_context = any(word in context.lower() for word in negative_context)
            
            if has_positive and has_negative_context:
                sarcasm_count += 2
                result["indicators"].append("contextual_sarcasm")
        
        if sarcasm_count > 0:
            result["detected"] = True
            result["confidence"] = min(sarcasm_count / 3.0, 1.0)
        
        return result
    
    def analyze_tone(self, text: str) -> Dict:
        """تحليل النبرة والأسلوب"""
        tone_scores = defaultdict(int)
        
        for tone, patterns in self.tone_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    tone_scores[tone] += 1
        
        if not tone_scores:
            return {"primary_tone": "neutral", "confidence": 0.5}
        
        primary_tone = max(tone_scores, key=tone_scores.get)
        confidence = tone_scores[primary_tone] / len(text.split())
        
        return {
            "primary_tone": primary_tone,
            "confidence": min(confidence, 1.0),
            "all_tones": dict(tone_scores)
        }
    
    def detect_implicit_meaning(self, text: str) -> str:
        """كشف المعنى الضمني للعبارات"""
        for phrase, meaning in self.implicit_meaning_detector.items():
            if phrase in text:
                return meaning
        
        return "direct_meaning"
    
    def analyze_base_emotion(self, text: str) -> Dict:
        """التحليل العاطفي الأساسي المحسّن"""
        emotion_scores = defaultdict(float)
        indicators = []
        
        # تحليل العواطف السياقية
        for emotion_category, triggers_dict in self.contextual_emotion_map.items():
            base_emotion = emotion_category.split('_')[0]  # anger, sadness, joy
            
            for trigger_type, patterns in triggers_dict.items():
                for pattern in patterns:
                    if pattern in text:
                        emotion_scores[base_emotion] += 1.0
                        indicators.append(f"{base_emotion}:{pattern}")
        
        # تحليل المشاعر الأساسية بالكلمات المفتاحية
        basic_emotions = {
            "anger": ["غضبان", "زعلان", "متنرفز", "حانق", "مستاء"],
            "sadness": ["حزين", "متضايق", "مكتئب", "زعلان", "متألم"],
            "joy": ["فرحان", "سعيد", "مبسوط", "مستانس", "مسرور"],
            "fear": ["خايف", "قلقان", "متوتر", "مرعوب", "هلعان"],
            "love": ["أحب", "عاشق", "محب", "مولع", "معجب"]
        }
        
        for emotion, keywords in basic_emotions.items():
            for keyword in keywords:
                if keyword in text:
                    emotion_scores[emotion] += 0.8
                    indicators.append(f"{emotion}:{keyword}")
        
        if not emotion_scores:
            return {
                "emotion": "neutral",
                "intensity": 0.5,
                "confidence": 0.5,
                "indicators": []
            }
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        intensity = min(emotion_scores[primary_emotion] / 2.0, 1.0)
        confidence = min(len(indicators) / 3.0, 1.0)
        
        return {
            "emotion": primary_emotion,
            "intensity": intensity,
            "confidence": confidence,
            "indicators": indicators
        }
    
    def analyze_cultural_context(self, text: str) -> Dict:
        """تحليل السياق الثقافي والحساسيات"""
        result = {
            "context": "general",
            "sensitivity_level": "low",
            "triggered_areas": []
        }
        
        for area, data in self.cultural_sensitivity_map.items():
            for trigger in data["triggers"]:
                if trigger in text:
                    result["context"] = area
                    result["sensitivity_level"] = data["severity"]
                    result["triggered_areas"].append(area)
        
        return result
    
    def synthesize_emotion_results(self, base_emotion: Dict, insult_result: Dict, 
                                  sarcasm_result: Dict, tone_analysis: Dict, 
                                  cultural_analysis: Dict) -> Dict:
        """دمج نتائج التحليلات المختلفة"""
        
        # تعديل العاطفة الأساسية بناءً على الإهانات
        if insult_result["detected"]:
            if insult_result["severity"] > 0.7:
                final_emotion = "anger"
                intensity = 0.9
            else:
                final_emotion = "hurt"  # شعور بالأذى
                intensity = 0.7
        else:
            final_emotion = base_emotion["emotion"]
            intensity = base_emotion["intensity"]
        
        # تعديل بناءً على السخرية
        if sarcasm_result["detected"]:
            if final_emotion == "neutral":
                final_emotion = "confused"  # الحيرة من السخرية
            intensity = min(intensity + 0.3, 1.0)
        
        # تعديل بناءً على النبرة
        tone = tone_analysis["primary_tone"]
        if tone == "aggressive":
            intensity = min(intensity + 0.4, 1.0)
        elif tone == "passive_aggressive":
            final_emotion = "irritated"  # الانزعاج المكتوم
            intensity = 0.6
        
        # تعديل بناءً على الحساسية الثقافية
        if cultural_analysis["sensitivity_level"] in ["high", "very_high", "extreme"]:
            intensity = min(intensity + 0.5, 1.0)
            if cultural_analysis["context"] == "family_honor":
                final_emotion = "deeply_offended"  # إهانة عميقة
        
        confidence = min(
            base_emotion["confidence"] + 
            (0.3 if insult_result["detected"] else 0) +
            (0.2 if sarcasm_result["detected"] else 0) +
            (0.1 if tone_analysis["confidence"] > 0.5 else 0),
            1.0
        )
        
        return {
            "emotion": final_emotion,
            "intensity": intensity,
            "confidence": confidence,
            "indicators": base_emotion["indicators"] + insult_result["specific_insults"]
        }
    
    def determine_response_tone(self, emotion_result: Dict, insult_result: Dict, 
                               cultural_analysis: Dict) -> str:
        """تحديد نبرة الاستجابة المناسبة"""
        
        # إذا تم اكتشاف إهانة
        if insult_result["detected"]:
            if insult_result["severity"] > 0.8:
                return "defensive_firm"  # دفاع حازم ولكن مهذب
            elif cultural_analysis["sensitivity_level"] in ["high", "very_high"]:
                return "hurt_disappointed"  # تأثر وخيبة أمل
            else:
                return "polite_deflection"  # تجاهل مهذب
        
        # بناءً على العاطفة الأساسية
        emotion = emotion_result["emotion"]
        if emotion in ["anger", "deeply_offended"]:
            return "calm_assertive"  # هدوء واثق
        elif emotion in ["hurt", "sad"]:
            return "gentle_sad"  # حزن لطيف
        elif emotion in ["confused", "irritated"]:
            return "seeking_clarification"  # طلب توضيح
        else:
            return "friendly_neutral"  # ودود ومحايد
    
    def generate_contextual_response(self, emotion_result: AdvancedEmotionResult, 
                                   user_message: str) -> Dict[str, str]:
        """توليد استجابة تتناسب مع السياق العاطفي"""
        
        response_templates = {
            "defensive_firm": [
                "أقدر إنك تعبر عن رأيك بطريقة أكثر احتراماً",
                "كلامك يؤذي المشاعر، وأتمنى نحافظ على أدب الحوار",
                "ما أحب هالطريقة في الكلام، نقدر نختلف باحترام"
            ],
            
            "hurt_disappointed": [
                "كلامك أثر فيّ بصراحة، ما توقعت منك هالطريقة",
                "حسيت بالأذى من كلامك، رغم إني أحترمك",
                "صعب عليّ أسمع هالكلام منك"
            ],
            
            "polite_deflection": [
                "أفهم إنك متضايق، بس نقدر نتكلم بطريقة أحسن",
                "ما عليك، الكل يمر بأوقات صعبة",
                "أعذرك لأنك في حالة مو طبيعية"
            ],
            
            "calm_assertive": [
                "أنا هنا عشان أساعد، مو عشان أتحمل الإهانة",
                "نقدر نحل أي مشكلة بدون استخدام هالأسلوب",
                "الاحترام المتبادل أساس أي حوار ناجح"
            ],
            
            "gentle_sad": [
                "كلامك خلاني أحزن، كنت أتمنى نفهم بعض أكثر",
                "أسف إذا كان في شي من ناحيتي ضايقك",
                "أتمنى نقدر نصلح الأمور بيننا"
            ],
            
            "seeking_clarification": [
                "مو فاهم قصدك بالضبط، ممكن توضح أكثر؟",
                "حسيت إن في سوء فهم، ممكن نتكلم بصراحة؟",
                "كلامك مو واضح لي، أقدر أعرف إيش تقصد؟"
            ],
            
            "friendly_neutral": [
                "أهلاً وسهلاً، كيف أقدر أساعدك؟",
                "تشرفت بكلامك، إيش اللي تحتاجه؟",
                "أنا في الخدمة، قول لي وش تبي"
            ]
        }
        
        template_key = emotion_result.response_tone_needed
        templates = response_templates.get(template_key, response_templates["friendly_neutral"])
        
        import random
        selected_response = random.choice(templates)
        
        return {
            "response": selected_response,
            "emotion_detected": emotion_result.primary_emotion,
            "intensity": f"{emotion_result.intensity:.1f}",
            "confidence": f"{emotion_result.confidence:.1f}",
            "insult_detected": "نعم" if emotion_result.insult_detected else "لا",
            "sarcasm_detected": "نعم" if emotion_result.sarcasm_detected else "لا",
            "response_tone": emotion_result.response_tone_needed,
            "cultural_context": emotion_result.cultural_context
        }

if __name__ == "__main__":
    # اختبار النظام
    print("🧠 نظام الذكاء العاطفي المتقدم والسياقي")
    print("=" * 60)
    
    emotion_system = AdvancedEmotionalIntelligence()
    
    # جمل اختبار متنوعة
    test_messages = [
        "كل زق يا نانو",  # سبة صريحة
        "يا أصلع، إيش رأيك؟",  # إهانة مبطنة
        "ما شاء الله عليك، شاطر كثير!",  # سخرية محتملة  
        "طيب، كما تشاء",  # موافقة متردد
        "أنت رائع ومفيد جداً",  # مجاملة صادقة
        "والله فرحان إنك معي!",  # مشاعر إيجابية
        "متأكد من كلامك هذا؟",  # تشكيك
        "الله يهديك يا حبيبي",  # استخدام ديني محتمل السخرية
        "أمك علمتك كذا؟",  # إهانة عائلية
        "شكراً لك من كل قلبي"  # امتنان صادق
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'-'*50}")
        print(f"اختبار {i}: {message}")
        
        # تحليل متقدم
        emotion_result = emotion_system.analyze_advanced_emotion(message)
        
        # توليد استجابة
        response_data = emotion_system.generate_contextual_response(emotion_result, message)
        
        # عرض النتائج
        print(f"\n📊 التحليل:")
        print(f"   العاطفة الأساسية: {emotion_result.primary_emotion}")
        print(f"   الشدة: {emotion_result.intensity:.2f}")
        print(f"   الثقة: {emotion_result.confidence:.2f}")
        print(f"   إهانة مكتشفة: {'نعم' if emotion_result.insult_detected else 'لا'}")
        print(f"   سخرية مكتشفة: {'نعم' if emotion_result.sarcasm_detected else 'لا'}")
        print(f"   السياق الثقافي: {emotion_result.cultural_context}")
        print(f"   المعنى الضمني: {emotion_result.implicit_meaning}")
        
        print(f"\n🤖 استجابة نانو: {response_data['response']}")
        print(f"📝 نبرة الرد: {response_data['response_tone']}")
    
    print("\n✨ النظام المتقدم يعمل بكفاءة عالية! ✨")