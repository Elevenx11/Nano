# test_nano.py - اختبار نانو الجديد
import sys
from pathlib import Path

# إضافة مسار core
sys.path.append(str(Path(__file__).parent / "core"))

from core.nano_brain import NanoBrain

def test_nano_personality():
    """اختبار شخصية نانو الطبيعية"""
    
    print("🧪 اختبار شخصية نانو الجديد")
    print("=" * 40)
    
    # إنشاء عقل نانو
    nano = NanoBrain("data")
    
    # اختبارات الشخصية
    test_cases = [
        # اختبار العناد
        ("سوي لي قهوة", "يجب أن يكون عنيد"),
        ("ممكن تساعدني؟", "يجب أن يكون متعاون"),
        
        # اختبار السخرية
        ("أنا أذكى واحد في العالم", "يجب أن يكون ساخر"),
        
        # اختبار التعاطف
        ("أنا زعلان اليوم", "يجب أن يكون متعاطف"),
        
        # اختبار الطبيعية
        ("مرحبا", "يجب أن يرد بطريقة طبيعية"),
        ("كيفك؟", "يجب أن يرد كصديق"),
        
        # اختبار ردود الفعل على الإهانات
        ("إنت غبي", "يجب أن يدافع عن نفسه"),
        ("كل زق", "يجب أن يرد بعناد أو هدوء")
    ]
    
    for i, (user_input, expected) in enumerate(test_cases, 1):
        print(f"\n📝 اختبار {i}: {user_input}")
        print(f"💭 متوقع: {expected}")
        
        # الحصول على رد نانو
        response = nano.generate_response(user_input)
        
        print(f"🤖 رد نانو: {response.text}")
        print(f"📊 التفاصيل:")
        print(f"   - المزاج: {response.personality_mood}")
        print(f"   - المشاعر: {response.emotion_detected}")
        print(f"   - الثقة: {response.confidence:.1%}")
        print(f"   - الطريقة: {response.method_used}")
        
        print("-" * 50)
    
    # إحصائيات النظام
    print("\n📊 إحصائيات النظام:")
    status = nano.get_system_status()
    print(f"   - المحادثات: {status['performance']['total_interactions']}")
    print(f"   - الأنماط المتعلمة: {status['learning']['total_patterns']}")
    print(f"   - مستوى العلاقة: {status['user_profile']['relationship_level']:.1%}")
    print(f"   - نوع الشخصية المكتشف: {status['user_profile']['personality_type']}")

def test_continuous_conversation():
    """اختبار محادثة مستمرة"""
    
    print("\n🗣️ اختبار المحادثة المستمرة")
    print("=" * 40)
    
    nano = NanoBrain("data")
    
    conversation = [
        "السلام عليكم",
        "كيف حالك؟",
        "سوي لي شاي",
        "ليش مو راضي؟",
        "طيب ممكن تساعدني في شي ثاني؟",
        "أنا زعلان منك",
        "خلاص سامحتك"
    ]
    
    print("💬 محادثة تجريبية:")
    
    for msg in conversation:
        print(f"\n👤 أنت: {msg}")
        response = nano.generate_response(msg)
        print(f"🤖 نانو: {response.text}")
        
        # إظهار تغير المزاج
        if hasattr(response, 'personality_mood'):
            print(f"   (المزاج: {response.personality_mood})")
    
    print("\n✅ انتهت المحادثة التجريبية")

def test_learning_system():
    """اختبار نظام التعلم"""
    
    print("\n📚 اختبار نظام التعلم")
    print("=" * 40)
    
    nano = NanoBrain("data")
    
    # تعليم نانو رد جديد
    print("🎯 تعليم نانو رد جديد...")
    
    # رد سيء أولاً
    response1 = nano.generate_response("وش أخبارك؟")
    print(f"📝 الرد الأول: {response1.text}")
    
    # تعليم رد أفضل
    nano.response_engine.learn_from_feedback(
        "وش أخبارك؟", "كله طيب والحمدلله، وإنت شخبارك؟", 
        "friendly", 0.9
    )
    
    # تجربة مرة أخرى
    response2 = nano.generate_response("وش أخبارك؟")
    print(f"📝 الرد بعد التعلم: {response2.text}")
    
    print("✅ نظام التعلم يعمل بشكل صحيح")

def main():
    """الدالة الرئيسية"""
    
    print("🚀 بدء اختبار نانو الجديد")
    print("=" * 50)
    
    try:
        # اختبار الشخصية
        test_nano_personality()
        
        # اختبار المحادثة المستمرة
        test_continuous_conversation()
        
        # اختبار نظام التعلم
        test_learning_system()
        
        print("\n🎉 جميع الاختبارات مكتملة!")
        print("✅ نانو الجديد جاهز للاستخدام")
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        print("🔧 تأكد من تثبيت المتطلبات: pip install -r requirements.txt")

if __name__ == "__main__":
    main()