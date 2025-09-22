# nano_advanced_system.py - النظام المتكامل المتقدم لنانو
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import sys
import os

# إضافة المسار الحالي لاستيراد الوحدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد جميع الأنظمة المتطورة
try:
    from continuous_learning import ContinuousLearningSystem
    from context_memory import AdvancedContextMemory
    from emotional_intelligence import AdvancedEmotionalIntelligence
except ImportError as e:
    print(f"⚠️ خطأ في الاستيراد: {e}")
    print("تأكد من وجود جميع الملفات في نفس المجلد")

class NanoAdvancedSystem:
    """النظام المتكامل المتقدم لنانو - الجيل الجديد من الذكاء الاصطناعي السعودي"""
    
    def __init__(self, verbose: bool = True):
        self.version = "2.0 Advanced"
        self.initialization_time = datetime.now()
        self.verbose = verbose
        
        if self.verbose:
            print("🚀 تهيئة النظام المتكامل المتقدم لنانو...")
            print("=" * 60)
        
        # تهيئة الأنظمة الفرعية مع إعدادات السرعة
        self.learning_system = ContinuousLearningSystem(verbose=self.verbose)
        self.memory_system = AdvancedContextMemory()
        self.emotional_system = AdvancedEmotionalIntelligence()
        
        # إعدادات النظام
        self.system_stats = {
            "total_conversations": 0,
            "successful_responses": 0,
            "learning_sessions": 0,
            "emotional_responses": 0,
            "memory_interactions": 0
        }
        
        self.personality_config = {
            "name": "نانو",
            "personality": "مساعد ذكي سعودي أصيل",
            "traits": ["متعاطف", "ودود", "مفيد", "ثقافي", "ذكي"],
            "language_style": "اللهجة السعودية الأصيلة",
            "response_style": "دافئ ومتفهم"
        }
        
        if self.verbose:
            print("✅ تم تهيئة النظام بنجاح!")
            print(f"📅 وقت التهيئة: {self.initialization_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
    
    def process_user_message(self, user_message: str, user_context: Dict = None) -> Dict[str, Any]:
        """معالجة رسالة المستخدم بشكل متكامل"""
        if self.verbose:
            print(f"\n🔄 معالجة الرسالة: {user_message[:50]}...")
        
        # 1. تحليل الحالة العاطفية
        emotional_state = self.emotional_system.analyze_emotional_state(user_message)
        if self.verbose:
            print(f"💭 المشاعر المكتشفة: {emotional_state.primary_emotion} (شدة: {emotional_state.intensity:.2f})")
        
        # 2. استرجاع السياق من الذاكرة
        memory_hints = self.memory_system.generate_contextual_response_hints(user_message)
        if self.verbose:
            print(f"🧠 تم استرجاع السياق من الذاكرة")
        
        # 3. توليد الاستجابة العاطفية
        emotional_response = self.emotional_system.generate_empathetic_response(emotional_state, user_message)
        if self.verbose:
            print(f"💝 تم توليد الاستجابة العاطفية")
        
        # 4. دمج الاستجابة مع السياق
        enhanced_response = self.enhance_response_with_context(
            emotional_response, memory_hints, user_message
        )
        
        # 5. حفظ التفاعل في الذاكرة
        context = self.memory_system.add_conversation_context(user_message, enhanced_response["final_response"])
        if self.verbose:
            print(f"💾 تم حفظ التفاعل في الذاكرة")
        
        # 6. تحديث الإحصائيات
        self.update_system_stats(emotional_state, enhanced_response)
        
        return {
            "response": enhanced_response["final_response"],
            "emotional_analysis": {
                "primary_emotion": emotional_state.primary_emotion,
                "intensity": emotional_state.intensity,
                "cultural_context": emotional_state.cultural_context
            },
            "memory_context": {
                "relevant_history": len(memory_hints.get("relevant_history", [])),
                "conversation_patterns": memory_hints.get("conversation_patterns", {}),
                "memory_importance": context.memory_importance
            },
            "response_quality": {
                "empathy_level": enhanced_response["empathy_level"],
                "response_quality": enhanced_response["response_quality"],
                "emotional_resonance": enhanced_response["emotional_resonance"],
                "cultural_adaptation": enhanced_response["cultural_adaptation"]
            },
            "system_info": {
                "processing_time": enhanced_response["processing_time"],
                "confidence_level": enhanced_response["confidence_level"],
                "system_version": self.version
            }
        }
    
    def enhance_response_with_context(self, emotional_response: Dict, memory_hints: Dict, user_message: str) -> Dict[str, Any]:
        """تحسين الاستجابة باستخدام السياق والذاكرة"""
        start_time = time.time()
        
        base_response = emotional_response["response"]
        
        # إضافة عناصر من الذاكرة إذا كانت ذات صلة
        context_additions = []
        
        # فحص الأنماط السابقة
        conversation_patterns = memory_hints.get("conversation_patterns", {})
        if not conversation_patterns.get("insufficient_data", False):
            mood = conversation_patterns.get("conversation_mood", "balanced")
            if mood == "negative" and emotional_response["emotion_detected"] in ["sadness", "fear", "anger"]:
                context_additions.append("أشوف إن الأمور صعبة عليك هالفترة،")
            elif mood == "positive" and emotional_response["emotion_detected"] == "joy":
                context_additions.append("أحس إنك في فترة حلوة،")
        
        # إضافة مراجع للمحادثات السابقة المهمة
        relevant_history = memory_hints.get("relevant_history", [])
        if relevant_history and len(relevant_history) > 0:
            recent_topic = relevant_history[0].get("topic", "")
            if recent_topic and recent_topic in user_message.lower():
                context_additions.append("زي ما اتكلمنا قبل كذا،")
        
        # بناء الاستجابة المحسنة
        final_parts = []
        if context_additions:
            final_parts.extend(context_additions)
        final_parts.append(base_response)
        
        final_response = " ".join(final_parts)
        
        # تحسين الجودة والثقة
        processing_time = time.time() - start_time
        confidence_level = self.calculate_response_confidence(emotional_response, memory_hints)
        
        return {
            "final_response": final_response,
            "empathy_level": emotional_response["empathy_level"],
            "response_quality": emotional_response["response_quality"],
            "emotional_resonance": emotional_response["emotional_resonance"],
            "cultural_adaptation": emotional_response["cultural_adaptation"],
            "processing_time": processing_time,
            "confidence_level": confidence_level,
            "context_enhancements": len(context_additions)
        }
    
    def calculate_response_confidence(self, emotional_response: Dict, memory_hints: Dict) -> float:
        """حساب مستوى الثقة في الاستجابة"""
        confidence_factors = []
        
        # ثقة التحليل العاطفي
        confidence_factors.append(emotional_response.get("intensity", 0.5))
        
        # ثقة جودة الاستجابة
        confidence_factors.append(emotional_response.get("response_quality", 0.5))
        
        # ثقة السياق
        relevant_history = memory_hints.get("relevant_history", [])
        context_confidence = min(len(relevant_history) / 5.0, 1.0)  # كلما زاد السياق زادت الثقة
        confidence_factors.append(context_confidence)
        
        # متوسط الثقة
        return sum(confidence_factors) / len(confidence_factors)
    
    def update_system_stats(self, emotional_state, enhanced_response):
        """تحديث إحصائيات النظام"""
        self.system_stats["total_conversations"] += 1
        
        if enhanced_response["response_quality"] > 0.7:
            self.system_stats["successful_responses"] += 1
        
        if emotional_state.primary_emotion != "neutral":
            self.system_stats["emotional_responses"] += 1
        
        self.system_stats["memory_interactions"] += 1
    
    def run_learning_session(self) -> Dict[str, Any]:
        """تشغيل جلسة تعلم مستمر"""
        if self.verbose:
            print("\n📚 بدء جلسة التعلم المستمر...")
        
        added, total = self.learning_system.run_continuous_learning_cycle()
        
        self.system_stats["learning_sessions"] += 1
        
        return {
            "sentences_added": added,
            "total_sentences": total,
            "learning_session": self.system_stats["learning_sessions"],
            "timestamp": datetime.now().isoformat()
        }
    
    def get_comprehensive_analytics(self) -> Dict[str, Any]:
        """تحليلات شاملة للنظام"""
        # إحصائيات الذاكرة
        memory_stats = self.memory_system.get_memory_stats()
        
        # إحصائيات الذكاء العاطفي
        emotional_stats = self.emotional_system.get_emotional_analytics()
        
        # إحصائيات النظام الإجمالية
        uptime = datetime.now() - self.initialization_time
        
        return {
            "system_overview": {
                "version": self.version,
                "uptime_hours": uptime.total_seconds() / 3600,
                "initialization_time": self.initialization_time.isoformat(),
                "total_conversations": self.system_stats["total_conversations"],
                "success_rate": (self.system_stats["successful_responses"] / max(self.system_stats["total_conversations"], 1)) * 100
            },
            "memory_analytics": memory_stats,
            "emotional_analytics": emotional_stats,
            "performance_metrics": {
                "learning_sessions": self.system_stats["learning_sessions"],
                "emotional_responses": self.system_stats["emotional_responses"],
                "memory_interactions": self.system_stats["memory_interactions"],
                "average_response_quality": self.calculate_average_response_quality()
            }
        }
    
    def calculate_average_response_quality(self) -> float:
        """حساب متوسط جودة الاستجابة"""
        # هذا يحسب على أساس الإحصائيات المتاحة
        if self.system_stats["total_conversations"] == 0:
            return 0.0
        
        success_rate = self.system_stats["successful_responses"] / self.system_stats["total_conversations"]
        emotional_rate = self.system_stats["emotional_responses"] / self.system_stats["total_conversations"]
        
        return (success_rate + emotional_rate) / 2
    
    def interactive_chat_mode(self):
        """وضع المحادثة التفاعلية"""
        print("\n💬 وضع المحادثة التفاعلية - اكتب 'خروج' للإنهاء")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 أنت: ").strip()
                
                if user_input.lower() in ['خروج', 'exit', 'quit', 'bye']:
                    print("👋 مع السلامة! كان من دواعي سروري التحدث معك")
                    break
                
                if not user_input:
                    continue
                
                # معالجة الرسالة
                result = self.process_user_message(user_input)
                
                # عرض الاستجابة
                print(f"\n🤖 نانو: {result['response']}")
                
                # عرض معلومات إضافية (اختيارية)
                if result['emotional_analysis']['primary_emotion'] != 'neutral':
                    emotion_info = result['emotional_analysis']
                    print(f"💭 (اكتشفت مشاعر: {emotion_info['primary_emotion']} - شدة: {emotion_info['intensity']:.1f})")
                
            except KeyboardInterrupt:
                print("\n👋 تم الإنهاء. مع السلامة!")
                break
            except Exception as e:
                print(f"❌ حدث خطأ: {e}")
                continue
    
    def save_system_state(self, filepath: str = "nano_system_state.json"):
        """حفظ حالة النظام"""
        try:
            # حفظ الذاكرة
            self.memory_system.save_memory()
            
            # حفظ إحصائيات النظام
            system_state = {
                "version": self.version,
                "stats": self.system_stats,
                "personality": self.personality_config,
                "last_saved": datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(system_state, f, ensure_ascii=False, indent=2)
            
            print(f"💾 تم حفظ حالة النظام في: {filepath}")
            return True
        except Exception as e:
            print(f"❌ خطأ في حفظ النظام: {e}")
            return False

def main():
    """الدالة الرئيسية"""
    print("🇸🇦 نانو - النظام المتكامل المتقدم للذكاء الاصطناعي السعودي 🇸🇦")
    print("=" * 80)
    
    # إنشاء النظام
    nano_system = NanoAdvancedSystem()
    
    # عرض القائمة
    while True:
        print(f"\n{'قائمة النظام الرئيسية':^40}")
        print("=" * 40)
        print("1. وضع المحادثة التفاعلية")
        print("2. تشغيل جلسة تعلم مستمر")
        print("3. عرض التحليلات الشاملة") 
        print("4. حفظ حالة النظام")
        print("5. اختبار سريع للنظام")
        print("0. خروج")
        print("=" * 40)
        
        choice = input("اختر رقمًا: ").strip()
        
        if choice == "1":
            nano_system.interactive_chat_mode()
        
        elif choice == "2":
            learning_result = nano_system.run_learning_session()
            print(f"\n✅ تم إضافة {learning_result['sentences_added']} جملة جديدة")
            print(f"📊 إجمالي الجمل: {learning_result['total_sentences']}")
        
        elif choice == "3":
            analytics = nano_system.get_comprehensive_analytics()
            print(f"\n{'تحليلات النظام الشاملة':^50}")
            print("=" * 50)
            for section, data in analytics.items():
                print(f"\n📊 {section}:")
                if isinstance(data, dict):
                    for key, value in data.items():
                        print(f"   • {key}: {value}")
                else:
                    print(f"   {data}")
        
        elif choice == "4":
            nano_system.save_system_state()
        
        elif choice == "5":
            # اختبار سريع
            test_messages = [
                "السلام عليكم، كيف الحال؟",
                "والله فرحان! حصلت على قبول في الجامعة!",
                "حزين لأن صديقي سافر..."
            ]
            
            print("\n🧪 اختبار سريع للنظام:")
            for msg in test_messages:
                print(f"\n👤 اختبار: {msg}")
                result = nano_system.process_user_message(msg)
                print(f"🤖 نانو: {result['response']}")
        
        elif choice == "0":
            print("\n👋 شكرًا لاستخدام نانو! مع السلامة")
            nano_system.save_system_state()
            break
        
        else:
            print("❌ خيار غير صحيح. حاول مرة أخرى.")

if __name__ == "__main__":
    main()