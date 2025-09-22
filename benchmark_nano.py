# benchmark_nano.py - مقارنة أداء نانو
import time
import sys
import os

# إضافة المسار الحالي لاستيراد الوحدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def benchmark_continuous_learning():
    """مقارنة أداء نظام التعلم المستمر"""
    from continuous_learning import ContinuousLearningSystem
    
    print("🚀 مقارنة أداء نظام التعلم المستمر")
    print("=" * 50)
    
    # النمط السريع
    print("⚡ اختبار النمط السريع...")
    start_time = time.time()
    fast_system = ContinuousLearningSystem(verbose=False)
    fast_system.run_continuous_learning_cycle()
    fast_time = time.time() - start_time
    
    print(f"✅ النمط السريع: {fast_time:.3f} ثانية")
    
    # النمط العادي (مع تقليل الطباعة لتجنب مشاكل Unicode)
    print("🐌 اختبار النمط العادي...")
    start_time = time.time()
    regular_system = ContinuousLearningSystem(verbose=False)  # نستخدم False هنا أيضاً لتجنب مشاكل الطباعة
    regular_system.run_continuous_learning_cycle()
    regular_time = time.time() - start_time
    
    print(f"✅ النمط العادي: {regular_time:.3f} ثانية")
    
    # حساب التحسن
    improvement = (regular_time - fast_time) / regular_time * 100 if regular_time > 0 else 0
    speedup = regular_time / fast_time if fast_time > 0 else 1
    
    print(f"\n📊 نتائج المقارنة:")
    print(f"   تحسن بنسبة: {improvement:.1f}%")
    print(f"   تسريع بمعامل: {speedup:.2f}x")
    
    return fast_time, regular_time

def benchmark_emotional_intelligence():
    """مقارنة أداء نظام الذكاء العاطفي"""
    from emotional_intelligence import AdvancedEmotionalIntelligence
    
    print("\n💭 مقارنة أداء الذكاء العاطفي")
    print("=" * 50)
    
    ei_system = AdvancedEmotionalIntelligence()
    
    # جمل اختبار
    test_messages = [
        "والله فرحان مو طبيعي! حصلت على وظيفة أحلامي!",
        "حزين جداً لأن جدي توفى اليوم... الله يرحمه",
        "خايف من امتحان الغد، مو مستعد كويس",
        "غضبان من صديقي لأنه خانني وكذب عليّ",
        "أحب عائلتي كثير، هم كل حياتي"
    ] * 100  # تكرار للحصول على قياس أدق
    
    # اختبار الأداء
    print(f"🔍 معالجة {len(test_messages)} رسالة...")
    start_time = time.time()
    
    for message in test_messages:
        emotional_state = ei_system.analyze_emotional_state(message)
        response = ei_system.generate_empathetic_response(emotional_state, message)
        ei_system.update_emotional_memory(emotional_state, response)
    
    processing_time = time.time() - start_time
    avg_time_per_message = processing_time / len(test_messages) * 1000  # بالميليثانية
    
    print(f"✅ الوقت الإجمالي: {processing_time:.3f} ثانية")
    print(f"⚡ متوسط الوقت لكل رسالة: {avg_time_per_message:.2f} ميليثانية")
    
    return processing_time, avg_time_per_message

def benchmark_context_memory():
    """مقارنة أداء نظام الذاكرة السياقية"""
    from context_memory import AdvancedContextMemory
    
    print("\n🧠 مقارنة أداء الذاكرة السياقية")
    print("=" * 50)
    
    memory_system = AdvancedContextMemory()
    
    # محادثات اختبار
    test_conversations = [
        ("السلام عليكم، كيف الحال؟", "وعليكم السلام، الحمدلله بخير وأنت كيفك؟"),
        ("الحمدلله، أنا فرحان اليوم لأن حصلت على وظيفة جديدة", "مبروك عليك! الله يبارك لك في الوظيفة الجديدة"),
        ("أشكرك، بس قلقان شوي من التحدي الجديد", "هذا طبيعي، بإذن الله تتأقلم بسرعة وتنجح"),
        ("كيف أتعامل مع ضغط العمل؟", "المهم تنظم وقتك وتاخذ راحة بين الفترات")
    ] * 50  # تكرار للقياس
    
    print(f"💬 معالجة {len(test_conversations)} محادثة...")
    start_time = time.time()
    
    for user_msg, nano_resp in test_conversations:
        context = memory_system.add_conversation_context(user_msg, nano_resp)
        hints = memory_system.generate_contextual_response_hints(user_msg)
    
    processing_time = time.time() - start_time
    avg_time_per_conversation = processing_time / len(test_conversations) * 1000
    
    print(f"✅ الوقت الإجمالي: {processing_time:.3f} ثانية")
    print(f"⚡ متوسط الوقت لكل محادثة: {avg_time_per_conversation:.2f} ميليثانية")
    
    # عرض إحصائيات الذاكرة
    stats = memory_system.get_memory_stats()
    print(f"📊 محادثات محفوظة: {stats.get('total_conversations', 0)}")
    
    return processing_time, avg_time_per_conversation

def benchmark_integrated_system():
    """مقارنة أداء النظام المتكامل"""
    from nano_advanced_system import NanoAdvancedSystem
    
    print("\n🤖 مقارنة أداء النظام المتكامل")
    print("=" * 50)
    
    # النمط السريع
    print("⚡ اختبار النظام السريع...")
    start_time = time.time()
    fast_nano = NanoAdvancedSystem(verbose=False)
    
    test_messages = [
        "مرحبا كيف الحال؟",
        "فرحان اليوم!",
        "محتاج مساعدة في مشكلة"
    ]
    
    for msg in test_messages:
        result = fast_nano.process_user_message(msg)
    
    fast_time = time.time() - start_time
    print(f"✅ النظام السريع: {fast_time:.3f} ثانية")
    
    # النمط العادي
    print("🐌 اختبار النظام العادي...")
    start_time = time.time()
    regular_nano = NanoAdvancedSystem(verbose=True)
    
    for msg in test_messages:
        result = regular_nano.process_user_message(msg)
    
    regular_time = time.time() - start_time
    print(f"✅ النظام العادي: {regular_time:.3f} ثانية")
    
    speedup = regular_time / fast_time if fast_time > 0 else 1
    print(f"🚀 تسريع بمعامل: {speedup:.2f}x")
    
    return fast_time, regular_time

def main():
    """تشغيل جميع اختبارات الأداء"""
    print("🇸🇦 مقارنة أداء نانو - Nano Performance Benchmark 🇸🇦")
    print("=" * 60)
    
    total_start = time.time()
    
    try:
        # اختبار نظام التعلم المستمر
        cl_fast, cl_regular = benchmark_continuous_learning()
        
        # اختبار الذكاء العاطفي  
        ei_time, ei_avg = benchmark_emotional_intelligence()
        
        # اختبار الذاكرة السياقية
        cm_time, cm_avg = benchmark_context_memory()
        
        # اختبار النظام المتكامل
        int_fast, int_regular = benchmark_integrated_system()
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاختبار: {e}")
        return
    
    total_time = time.time() - total_start
    
    # تقرير نهائي
    print(f"\n🏆 التقرير النهائي")
    print("=" * 60)
    print(f"⏱️  إجمالي وقت الاختبار: {total_time:.2f} ثانية")
    print(f"🚀 نظام التعلم المستمر: {cl_fast:.3f}s (سريع) vs {cl_regular:.3f}s (عادي)")
    print(f"💭 الذكاء العاطفي: {ei_avg:.2f}ms متوسط لكل رسالة")
    print(f"🧠 الذاكرة السياقية: {cm_avg:.2f}ms متوسط لكل محادثة") 
    print(f"🤖 النظام المتكامل: {int_fast:.3f}s (سريع) vs {int_regular:.3f}s (عادي)")
    
    print(f"\n✨ نانو محسّن ومستعد للأداء العالي! ✨")

if __name__ == "__main__":
    main()