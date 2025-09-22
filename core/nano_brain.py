# nano_brain.py - العقل المركزي لنانو
import json
import random
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# استيراد النظم الفرعية
from .nano_personality import NanoPersonality, PersonalityResponse, PersonalityMood
from .contextual_emotion_engine import ContextualEmotionEngine
from .neural_response_engine import NeuralResponseEngine, ConversationContext

@dataclass 
class NanoThought:
    """فكرة نانو"""
    content: str
    confidence: float
    reasoning: str
    emotion_state: str
    personality_influence: float

@dataclass
class NanoResponse:
    """الرد النهائي من نانو"""
    text: str
    confidence: float
    method_used: str
    personality_mood: str
    emotion_detected: str
    reasoning: str
    thought_process: List[str]

class NanoBrain:
    """العقل المركزي لنانو - يدمج الشخصية والمشاعر والتعلم"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = Path(data_path)
        
        # النظم الفرعية
        self.personality = NanoPersonality()
        self.emotion_engine = ContextualEmotionEngine(str(self.data_path / "emotion_learning.pkl"))
        self.response_engine = NeuralResponseEngine(str(self.data_path))
        
        # ذاكرة المحادثة
        self.conversation_memory = []
        self.user_profile = {
            "personality_type": "unknown",
            "relationship_level": 0.5,
            "interaction_count": 0,
            "preference_patterns": {},
            "last_interaction": None
        }
        
        # إعدادات السلوك (رفع نسبة الشخصية إلى 40%)
        self.behavior_settings = {
            "stubbornness_threshold": 0.6,    # تخفيض عتبة العناد لزيادة الشخصية
            "sarcasm_probability": 0.4,       # زيادة احتمال السخرية
            "learning_rate": 0.08,            # تخفيض معدل التعلم قليلاً
            "personality_adaptation": True,    # التكيف مع شخصية المستخدم
            "emotion_sensitivity": 0.9,       # زيادة حساسية المشاعر
            "personality_weight": 0.4,        # وزن الشخصية 40%
            "neural_weight": 0.25,           # وزن النظام العصبي 25%
            "mixed_weight": 0.35             # وزن الرد المختلط 35%
        }
        
        # إحصائيات الأداء
        self.performance_stats = {
            "total_interactions": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "average_confidence": 0.0,
            "last_reset": datetime.now()
        }
        
        # تحميل البيانات المحفوظة
        self.load_brain_state()

    def think(self, user_input: str, context: Dict = None) -> NanoThought:
        """عملية التفكير - تحليل المدخل وتوليد الأفكار"""
        
        # استخراج سياق المحادثة
        conversation_context = self.build_conversation_context(user_input)
        
        # تحليل المشاعر السياقي
        previous_texts = [msg.get("user_input", "") for msg in self.conversation_memory[-5:]]
        emotion, emotion_confidence, emotion_details = self.emotion_engine.predict_emotion_contextual(
            user_input, previous_texts
        )
        
        # تحليل الشخصية والمزاج
        personality_response = self.personality.get_personality_response(user_input, str(context))
        
        # تقييم الموقف الإجمالي
        situation_assessment = self.assess_situation(user_input, emotion, personality_response)
        
        # إنتاج الفكرة
        thought_content = self.generate_thought_content(
            user_input, emotion, personality_response, situation_assessment
        )
        
        # حساب الثقة الإجمالية (رفع نسبة الشخصية)
        overall_confidence = (
            emotion_confidence * 0.3 + 
            personality_response.friendliness * 0.5 + 
            situation_assessment["clarity"] * 0.2
        )
        
        return NanoThought(
            content=thought_content,
            confidence=overall_confidence,
            reasoning=self.explain_reasoning(emotion_details, personality_response, situation_assessment),
            emotion_state=emotion,
            personality_influence=personality_response.stubbornness_level
        )

    def build_conversation_context(self, user_input: str) -> ConversationContext:
        """بناء سياق المحادثة"""
        
        recent_messages = [msg.get("user_input", "") for msg in self.conversation_memory[-3:]]
        
        # تحديد موضوع المحادثة من التاريخ
        conversation_topic = self.detect_conversation_topic(user_input, recent_messages)
        
        # تحديد المشاعر الحالية
        current_emotion = self.personality.current_mood.value if self.personality.current_mood else "محايد"
        
        return ConversationContext(
            previous_messages=recent_messages,
            current_emotion=current_emotion,
            user_personality_type=self.user_profile["personality_type"],
            relationship_level=self.user_profile["relationship_level"],
            conversation_topic=conversation_topic
        )

    def detect_conversation_topic(self, current_input: str, recent_messages: List[str]) -> str:
        """كشف موضوع المحادثة"""
        
        # مواضيع محتملة
        topic_keywords = {
            "تحية": ["مرحبا", "السلام", "أهلا", "هاي", "صباح", "مساء"],
            "مشكلة": ["مشكلة", "مشكلتي", "متضايق", "زعلان", "تعبان", "صعب"],
            "فرح": ["مبروك", "فرحان", "سعيد", "حققت", "نجحت", "فزت"],
            "سؤال": ["ليش", "إيش", "وش", "كيف", "متى", "وين", "مين"],
            "شكر": ["شكرا", "تسلم", "يعطيك العافية", "كثر خيرك"],
            "نقاش": ["أعتقد", "برأيي", "ما رأيك", "تفكر", "ترى"]
        }
        
        # فحص كل الرسائل (الحالية والسابقة)
        all_text = (current_input + " " + " ".join(recent_messages)).lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                return topic
        
        return "عام"

    def assess_situation(self, user_input: str, emotion: str, personality_response: PersonalityResponse) -> Dict:
        """تقييم الموقف الإجمالي"""
        
        assessment = {
            "complexity": len(user_input.split()) / 10.0,  # تعقيد السؤال
            "urgency": 0.5,  # الإلحاح (افتراضي)
            "clarity": 0.8,  # وضوح الرسالة
            "emotional_intensity": personality_response.stubbornness_level,
            "requires_special_handling": False
        }
        
        # تحديد المواقف الخاصة
        special_triggers = [
            "كل زق", "غبي", "حمار", "اصلع", "ما تفهم", 
            "روح تموت", "خراب", "فاشل"
        ]
        
        if any(trigger in user_input.lower() for trigger in special_triggers):
            assessment["requires_special_handling"] = True
            assessment["urgency"] = 1.0
            assessment["emotional_intensity"] = 1.0
        
        # تحديد مستوى التعقيد
        question_indicators = ["ليش", "إيش", "وش", "كيف", "متى", "وين", "مين"]
        if any(indicator in user_input.lower() for indicator in question_indicators):
            assessment["complexity"] += 0.3
        
        return assessment

    def generate_thought_content(self, user_input: str, emotion: str, 
                                personality_response: PersonalityResponse, 
                                situation_assessment: Dict) -> str:
        """توليد محتوى الفكرة"""
        
        thoughts = []
        
        # تحليل المشاعر
        thoughts.append(f"المشاعر المكتشفة: {emotion}")
        
        # تحليل الشخصية
        thoughts.append(f"المزاج الحالي: {personality_response.mood.value}")
        
        # تقييم الموقف
        if situation_assessment["requires_special_handling"]:
            thoughts.append("موقف حساس - يتطلب تعامل خاص")
        
        if situation_assessment["complexity"] > 0.7:
            thoughts.append("سؤال معقد - يحتاج تفكير أعمق")
        
        # استراتيجية الرد
        if personality_response.stubbornness_level > self.behavior_settings["stubbornness_threshold"]:
            thoughts.append("الوضع يتطلب موقف عنيد")
        elif personality_response.sarcasm_level > 0.6:
            thoughts.append("فرصة للسخرية الطريفة")
        else:
            thoughts.append("رد ودود مناسب")
        
        return " | ".join(thoughts)

    def explain_reasoning(self, emotion_details: Dict, personality_response: PersonalityResponse, 
                         situation_assessment: Dict) -> str:
        """شرح عملية التفكير"""
        
        reasoning_parts = []
        
        # تفسير المشاعر
        if emotion_details.get("features"):
            top_features = sorted(emotion_details["features"].items(), 
                                key=lambda x: x[1], reverse=True)[:3]
            reasoning_parts.append(f"أقوى العوامل العاطفية: {[f[0] for f in top_features]}")
        
        # تفسير الشخصية
        reasoning_parts.append(f"نبرة الشخصية: {personality_response.mood.value}")
        
        if personality_response.stubbornness_level > 0.5:
            reasoning_parts.append("مستوى العناد مرتفع")
        
        # تفسير الموقف
        if situation_assessment["requires_special_handling"]:
            reasoning_parts.append("موقف يتطلب حذر خاص")
        
        return " • ".join(reasoning_parts)

    def generate_response(self, user_input: str, context: Dict = None) -> NanoResponse:
        """توليد الرد النهائي"""
        
        # مرحلة التفكير
        thought = self.think(user_input, context)
        
        # بناء سياق المحادثة للرد
        conversation_context = self.build_conversation_context(user_input)
        
        # توليد مرشحين للرد
        candidate_responses = []
        
        # 1. من الشخصية (أولوية عالية مرفوعة لـ 40%)
        personality_response = self.personality.get_personality_response(user_input)
        candidate_responses.append((
            personality_response.text,
            "personality",
            1.15,  # رفع أولوية الشخصية إلى 40%
            personality_response.mood.value
        ))
        
        # 2. من محرك التعلم الذكي
        if len(self.conversation_memory) > 2:  # فقط إذا كان هناك تاريخ محادثة
            smart_response, smart_confidence, smart_method = self.response_engine.generate_smart_response(
                user_input, thought.emotion_state, conversation_context
            )
            candidate_responses.append((
                smart_response,
                f"neural_{smart_method}",
                smart_confidence * 0.45,  # تخفيض أولوية النظام العصبي لرفع نسبة الشخصية
                "متعلم"
            ))
        
        # 3. رد مختلط (دمج الشخصية والذكاء بنسبة أقل)
        if random.random() < 0.25:  # تقليل احتمال الدمج لرفع نسبة الشخصية
            mixed_response = self.create_mixed_response(personality_response.text, 
                                                      candidate_responses[-1][0] if len(candidate_responses) > 1 else "")
            candidate_responses.append((
                mixed_response,
                "mixed",
                0.65,  # تخفيض أولوية الرد المختلط
                "مختلط"
            ))
        
        # اختيار أفضل رد
        best_response = self.select_final_response(candidate_responses, thought, user_input)
        
        # إضافة التلوين الشخصي النهائي
        final_text = self.apply_personality_coloring(best_response[0], personality_response, thought)
        
        # بناء الرد النهائي
        nano_response = NanoResponse(
            text=final_text,
            confidence=best_response[2],
            method_used=best_response[1],
            personality_mood=personality_response.mood.value,
            emotion_detected=thought.emotion_state,
            reasoning=thought.reasoning,
            thought_process=[thought.content]
        )
        
        # حفظ في الذاكرة والتعلم
        self.save_interaction(user_input, nano_response)
        
        # التعلم من التفاعل
        self.learn_from_interaction(user_input, nano_response)
        
        return nano_response

    def create_mixed_response(self, personality_text: str, neural_text: str) -> str:
        """إنشاء رد مختلط بين الشخصية والذكاء"""
        
        if not neural_text or len(neural_text.strip()) < 3:
            return personality_text
        
        # أساليب الخلط
        mixing_styles = [
            lambda p, n: f"{p}، {n}",  # ربط بسيط
            lambda p, n: f"{n} - {p}",  # عكس الترتيب
            lambda p, n: f"{p[:len(p)//2]} {n}",  # نصف ونصف
            lambda p, n: random.choice([p, n])  # اختيار عشوائي
        ]
        
        mixing_style = random.choice(mixing_styles)
        return mixing_style(personality_text, neural_text)

    def select_final_response(self, candidates: List[Tuple[str, str, float, str]], 
                             thought: NanoThought, user_input: str) -> Tuple[str, str, float, str]:
        """اختيار الرد النهائي من المرشحين"""
        
        if not candidates:
            return ("فهمت كلامك", "fallback", 0.3, "احتياطي")
        
        # تطبيق معايير الاختيار
        scored_candidates = []
        
        for text, method, confidence, mood in candidates:
            score = confidence
            
            # مكافآت إضافية
            if len(text) > 5:  # رد ليس مختصر جداً
                score += 0.1
            
            if method == "personality":
                score += 0.4  # رفع مكافأة الشخصية إلى 40%
                if thought.personality_influence > 0.7:
                    score += 0.3  # مكافأة إضافية في المواقف العاطفية
            
            if method.startswith("neural") and len(self.conversation_memory) > 5:
                score += 0.05  # تخفيض مكافأة التعلم
            
            # عقوبات
            if text == user_input:  # تجنب التكرار المباشر
                score -= 0.8
            
            if len(text.strip()) < 3:  # تجنب الردود الفارغة
                score -= 0.5
            
            scored_candidates.append((text, method, score, mood))
        
        # اختيار الأفضل
        best_candidate = max(scored_candidates, key=lambda x: x[2])
        return best_candidate

    def apply_personality_coloring(self, response: str, personality_response: PersonalityResponse, 
                                  thought: NanoThought) -> str:
        """تطبيق التلوين الشخصي النهائي"""
        
        colored_response = response
        
        # إضافات حسب المزاج
        if personality_response.mood == PersonalityMood.SARCASTIC:
            if random.random() < 0.3:
                colored_response += " 🙄"
        
        elif personality_response.mood == PersonalityMood.CHEERFUL:
            if random.random() < 0.4:
                colored_response += random.choice([" 😊", " هههه", " والله حلو"])
        
        elif personality_response.mood == PersonalityMood.STUBBORN:
            if random.random() < 0.5:
                colored_response = f"خلاص، {colored_response}"
        
        # إضافات حسب مستوى العلاقة
        if self.user_profile["relationship_level"] > 0.8:
            endearments = ["حبيبي", "يا غالي", "عزيزي"]
            if random.random() < 0.3:
                colored_response += f" {random.choice(endearments)}"
        
        # إضافات عشوائية للطبيعية
        natural_additions = ["", " يعني", " الصراحة", " والله", " تدري"]
        if random.random() < 0.2:
            prefix = random.choice(natural_additions)
            if prefix:
                colored_response = f"{prefix} {colored_response}"
        
        return colored_response.strip()

    def save_interaction(self, user_input: str, nano_response: NanoResponse):
        """حفظ التفاعل في الذاكرة"""
        
        interaction = {
            "timestamp": datetime.now(),
            "user_input": user_input,
            "nano_response": nano_response.text,
            "method_used": nano_response.method_used,
            "confidence": nano_response.confidence,
            "mood": nano_response.personality_mood,
            "emotion": nano_response.emotion_detected
        }
        
        self.conversation_memory.append(interaction)
        
        # الاحتفاظ بآخر 50 تفاعل فقط
        if len(self.conversation_memory) > 50:
            self.conversation_memory.pop(0)
        
        # تحديث ملف المستخدم
        self.update_user_profile(user_input, nano_response)

    def update_user_profile(self, user_input: str, nano_response: NanoResponse):
        """تحديث ملف المستخدم"""
        
        self.user_profile["interaction_count"] += 1
        self.user_profile["last_interaction"] = datetime.now()
        
        # تحديث مستوى العلاقة تدريجياً
        if nano_response.confidence > 0.7:
            self.user_profile["relationship_level"] = min(1.0, 
                self.user_profile["relationship_level"] + 0.02)
        elif nano_response.confidence < 0.4:
            self.user_profile["relationship_level"] = max(0.1,
                self.user_profile["relationship_level"] - 0.01)
        
        # تحليل نمط شخصية المستخدم
        self.analyze_user_personality(user_input)

    def analyze_user_personality(self, user_input: str):
        """تحليل شخصية المستخدم من طريقة كلامه"""
        
        # مؤشرات أنماط الشخصية
        patterns = {
            "friendly": ["حبيبي", "عزيزي", "والله", "ما شاء الله", "كفو"],
            "serious": ["أرجو", "من فضلك", "أريد", "أحتاج", "أطلب"],
            "casual": ["هاي", "مرحبا", "شلونك", "وش أخبارك", "كيفك"],
            "emotional": ["تعبان", "فرحان", "زعلان", "متضايق", "سعيد"]
        }
        
        text_lower = user_input.lower()
        
        for personality_type, indicators in patterns.items():
            if any(indicator in text_lower for indicator in indicators):
                # زيادة النقاط لهذا النوع
                if personality_type not in self.user_profile["preference_patterns"]:
                    self.user_profile["preference_patterns"][personality_type] = 0
                
                self.user_profile["preference_patterns"][personality_type] += 1
                
                # تحديث نوع الشخصية الرئيسي
                max_type = max(self.user_profile["preference_patterns"].items(), 
                             key=lambda x: x[1])[0]
                self.user_profile["personality_type"] = max_type

    def learn_from_interaction(self, user_input: str, nano_response: NanoResponse):
        """التعلم من التفاعل الحالي"""
        
        # تحديث إحصائيات الأداء
        self.performance_stats["total_interactions"] += 1
        
        if nano_response.confidence > 0.6:
            self.performance_stats["successful_responses"] += 1
            feedback_score = nano_response.confidence
        else:
            self.performance_stats["failed_responses"] += 1
            feedback_score = nano_response.confidence
        
        # حساب متوسط الثقة
        total_responses = (self.performance_stats["successful_responses"] + 
                          self.performance_stats["failed_responses"])
        self.performance_stats["average_confidence"] = (
            (self.performance_stats["average_confidence"] * (total_responses - 1) + 
             nano_response.confidence) / total_responses
        )
        
        # تمرير التعلم للنظم الفرعية
        self.response_engine.learn_from_feedback(
            user_input, nano_response.text, 
            nano_response.method_used, feedback_score
        )
        
        self.emotion_engine.learn_from_interaction(
            user_input, nano_response.emotion_detected,
            nano_response.method_used, feedback_score
        )

    def get_system_status(self) -> Dict:
        """الحصول على حالة النظام"""
        
        return {
            "personality": {
                "current_mood": self.personality.current_mood.value,
                "stubbornness_level": self.personality.stubbornness_level,
                "energy_level": self.personality.energy_level,
                "patience_level": self.personality.patience_level
            },
            "learning": {
                "emotion_accuracy": self.emotion_engine.learning_stats.get("emotion_accuracy", 0),
                "total_patterns": len(self.response_engine.response_patterns),
                "learning_progress": self.response_engine.calculate_learning_progress()
            },
            "user_profile": self.user_profile.copy(),
            "performance": self.performance_stats.copy(),
            "conversation": {
                "messages_count": len(self.conversation_memory),
                "topics_discussed": list(set(msg.get("emotion", "عام") 
                                           for msg in self.conversation_memory[-10:]))
            }
        }

    def reset_conversation(self):
        """إعادة تعيين المحادثة"""
        self.conversation_memory.clear()
        self.personality.patience_level = 0.6
        self.personality.current_mood = PersonalityMood.FRIENDLY

    def save_brain_state(self):
        """حفظ حالة العقل"""
        brain_state = {
            "user_profile": self.user_profile,
            "behavior_settings": self.behavior_settings,
            "performance_stats": self.performance_stats,
            "conversation_memory": [
                {**msg, "timestamp": msg["timestamp"].isoformat()} 
                for msg in self.conversation_memory[-10:]  # آخر 10 فقط
            ]
        }
        
        # إنشاء مجلد البيانات
        self.data_path.mkdir(exist_ok=True)
        
        # حفظ حالة العقل
        with open(self.data_path / "brain_state.json", "w", encoding="utf-8") as f:
            json.dump(brain_state, f, ensure_ascii=False, indent=2, default=str)
        
        # حفظ النظم الفرعية
        self.emotion_engine.save_learning_data()
        self.response_engine.save_learned_data()

    def load_brain_state(self):
        """تحميل حالة العقل"""
        brain_state_path = self.data_path / "brain_state.json"
        
        if brain_state_path.exists():
            try:
                with open(brain_state_path, "r", encoding="utf-8") as f:
                    brain_state = json.load(f)
                
                self.user_profile.update(brain_state.get("user_profile", {}))
                self.behavior_settings.update(brain_state.get("behavior_settings", {}))
                self.performance_stats.update(brain_state.get("performance_stats", {}))
                
                # استعادة الذاكرة
                memory_data = brain_state.get("conversation_memory", [])
                for msg in memory_data:
                    if "timestamp" in msg and isinstance(msg["timestamp"], str):
                        msg["timestamp"] = datetime.fromisoformat(msg["timestamp"])
                    self.conversation_memory.append(msg)
                
            except Exception as e:
                print(f"خطأ في تحميل حالة العقل: {e}")

    def get_debug_info(self, user_input: str) -> Dict:
        """معلومات التشخيص للمطورين"""
        
        # تشغيل التفكير
        thought = self.think(user_input)
        
        debug_info = {
            "input_analysis": {
                "word_count": len(user_input.split()),
                "character_count": len(user_input),
                "detected_keywords": self.response_engine.extract_keywords(user_input)
            },
            "thought_process": {
                "content": thought.content,
                "confidence": thought.confidence,
                "reasoning": thought.reasoning,
                "emotion_state": thought.emotion_state
            },
            "system_state": self.get_system_status(),
            "conversation_context": {
                "recent_messages": len(self.conversation_memory),
                "relationship_level": self.user_profile["relationship_level"],
                "user_personality": self.user_profile["personality_type"]
            }
        }
        
        return debug_info