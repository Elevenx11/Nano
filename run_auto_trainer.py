# run_auto_trainer.py - تشغيل نظام التدريب التلقائي الذكي لنانو
import os
import sys
import json
from datetime import datetime
import subprocess

def install_requirements():
    """تثبيت المتطلبات المطلوبة"""
    required_packages = [
        'schedule',
        'psutil', 
        'requests',
        'beautifulsoup4',
        'selenium'
        # 'nltk',  # ليس مطلوب حالياً
        # 'textblob'  # ليس مطلوب حالياً
    ]
    
    print("🔧 فحص وتثبيت المتطلبات...")
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"📦 تثبيت {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    print("✅ تم التأكد من جميع المتطلبات")

def check_system_setup():
    """فحص إعداد النظام"""
    print("🔍 فحص إعداد النظام...")
    
    # فحص الملفات المطلوبة
    required_files = [
        'smart_auto_trainer.py',
        'social_media_collector.py', 
        'advanced_auto_scheduler.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {', '.join(missing_files)}")
        return False
    
    # إنشاء مجلدات مطلوبة
    dirs_to_create = ['backups', 'logs']
    for dir_name in dirs_to_create:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 تم إنشاء مجلد: {dir_name}")
    
    # إنشاء corpus.json إذا لم يكن موجود
    if not os.path.exists('corpus.json'):
        initial_corpus = {
            "sentences": [
                "السلام عليكم ورحمة الله وبركاته",
                "وعليكم السلام ورحمة الله وبركاته", 
                "أهلا وسهلا بك",
                "شلونك؟ كيف الصحة؟",
                "الحمدلله، كله تمام",
                "الله يعطيك العافية",
                "تسلم يا غالي",
                "ما شاء الله عليك",
                "بارك الله فيك",
                "في أمان الله"
            ]
        }
        
        with open('corpus.json', 'w', encoding='utf-8') as f:
            json.dump(initial_corpus, f, ensure_ascii=False, indent=2)
        
        print("📝 تم إنشاء corpus.json الأساسي")
    
    print("✅ النظام جاهز للتشغيل")
    return True

def show_main_menu():
    """عرض القائمة الرئيسية"""
    print(f"\n{'='*60}")
    print("🤖 نظام التدريب الذكي التلقائي لنانو")
    print(f"{'='*60}")
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 مجلد العمل: {os.getcwd()}")
    print("-" * 60)
    print("1️⃣  بدء التدريب التلقائي المستمر (موصى به)")
    print("2️⃣  تشغيل جلسة تدريب واحدة فقط")
    print("3️⃣  اختبار جمع البيانات من وسائل التواصل")
    print("4️⃣  عرض الإحصائيات والتقارير")
    print("5️⃣  إنشاء نسخة احتياطية")
    print("6️⃣  إعدادات النظام")
    print("7️⃣  اختبار جودة النص")
    print("8️⃣  فحص موارد النظام")
    print("9️⃣  تشغيل النظام القديم (للمقارنة)")
    print("0️⃣  خروج")
    print("-" * 60)

def run_continuous_training():
    """تشغيل التدريب المستمر"""
    print("🚀 بدء النظام الذكي للتدريب التلقائي المستمر...")
    print("⚠️  هذا الوضع سيعمل تلقائياً كل فترة زمنية")
    print("🛑 يمكنك إيقافه بـ Ctrl+C")
    
    confirm = input("\nهل تريد المتابعة؟ (y/n): ").strip().lower()
    if confirm in ['y', 'yes', 'نعم', '1']:
        try:
            from advanced_auto_scheduler import AdvancedAutoScheduler
            scheduler = AdvancedAutoScheduler()
            scheduler.start_scheduler()
        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف النظام بواسطة المستخدم")
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
    else:
        print("❌ تم إلغاء العملية")

def run_single_session():
    """تشغيل جلسة واحدة"""
    print("🎯 تشغيل جلسة تدريب واحدة...")
    
    try:
        from advanced_auto_scheduler import AdvancedAutoScheduler
        scheduler = AdvancedAutoScheduler()
        scheduler.run_intelligent_training_session()
        
        # عرض النتائج
        print("\n📊 إحصائيات الجلسة:")
        if scheduler.current_session:
            session = scheduler.current_session
            print(f"   📥 جمل مجمعة: {session.get('sentences_collected', 0)}")
            print(f"   🎯 جمل مدربة: {session.get('sentences_trained', 0)}")
            print(f"   📡 مصادر: {', '.join(session.get('sources_used', []))}")
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

def test_data_collection():
    """اختبار جمع البيانات"""
    print("📊 اختبار جمع البيانات من وسائل التواصل...")
    
    try:
        from social_media_collector import SocialMediaCollector
        collector = SocialMediaCollector()
        
        # جمع بيانات تجريبية
        data = collector.collect_all_sources(max_per_source=10)
        
        print(f"✅ تم جمع {len(data)} عنصر")
        
        if data:
            print("\n📄 عينة من البيانات المجمعة:")
            for i, item in enumerate(data[:3]):
                print(f"   {i+1}. [{item['platform']}] {item['content'][:50]}...")
        
        collector.close()
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

def show_statistics():
    """عرض الإحصائيات"""
    print("📊 جاري تحميل الإحصائيات...")
    
    try:
        from advanced_auto_scheduler import AdvancedAutoScheduler
        scheduler = AdvancedAutoScheduler()
        scheduler.get_detailed_statistics()
        
        # إحصائيات إضافية
        if os.path.exists('corpus.json'):
            with open('corpus.json', 'r', encoding='utf-8') as f:
                corpus = json.load(f)
            print(f"\n📚 حجم قاعدة البيانات: {len(corpus.get('sentences', []))} جملة")
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

def create_backup():
    """إنشاء نسخة احتياطية"""
    print("💾 إنشاء نسخة احتياطية...")
    
    try:
        from advanced_auto_scheduler import AdvancedAutoScheduler
        scheduler = AdvancedAutoScheduler()
        scheduler.create_backup()
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

def show_settings():
    """عرض الإعدادات"""
    config_file = "scheduler_config.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print("\n⚙️ الإعدادات الحالية:")
            print(json.dumps(config, ensure_ascii=False, indent=2))
            
        except Exception as e:
            print(f"❌ خطأ في قراءة الإعدادات: {str(e)}")
    else:
        print("📝 لا توجد إعدادات مخصصة، سيتم استخدام الإعدادات الافتراضية")

def test_text_quality():
    """اختبار جودة النص"""
    print("🔍 اختبار جودة النص...")
    
    text = input("أدخل النص للاختبار: ").strip()
    if not text:
        print("❌ لم يتم إدخال نص")
        return
    
    try:
        from smart_auto_trainer import SmartAutoTrainer
        trainer = SmartAutoTrainer()
        
        quality = trainer.quality_check(text)
        saudi_score = trainer.calculate_saudi_score(text)
        emotions = trainer.analyze_emotion_context(text)
        
        print(f"\n📝 نتائج التحليل:")
        print(f"🎯 درجة الجودة: {quality:.2f}/1.0")
        print(f"🇸🇦 درجة اللهجة السعودية: {saudi_score:.2f}/1.0")
        print(f"💭 المشاعر المكتشفة:")
        
        for emotion, score in emotions.items():
            if score > 0:
                print(f"   {emotion}: {score:.2f}")
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

def check_system_resources():
    """فحص موارد النظام"""
    print("🖥️ فحص موارد النظام...")
    
    try:
        from advanced_auto_scheduler import AdvancedAutoScheduler
        scheduler = AdvancedAutoScheduler()
        
        resources = scheduler.check_system_resources()
        
        if resources:
            print(f"\n💻 حالة النظام:")
            print(f"   🔥 استهلاك المعالج: {resources['cpu_usage']:.1f}%")
            print(f"   🧠 استهلاك الذاكرة: {resources['memory_usage']:.1f}%")
            print(f"   💾 استهلاك القرص: {resources['disk_usage']:.1f}%")
            print(f"   📦 الذاكرة المتاحة: {resources['available_memory_gb']:.1f} GB")
            print(f"   🗄️ مساحة القرص المتاحة: {resources['free_disk_gb']:.1f} GB")
            
            # تحذيرات
            if resources['cpu_usage'] > 80:
                print("⚠️ تحذير: استهلاك معالج عالي")
            if resources['memory_usage'] > 80:
                print("⚠️ تحذير: استهلاك ذاكرة عالي")
            if resources['free_disk_gb'] < 5:
                print("⚠️ تحذير: مساحة قرص منخفضة")
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

def run_legacy_system():
    """تشغيل النظام القديم"""
    print("🔄 تشغيل نظام التدريب القديم للمقارنة...")
    
    if os.path.exists('daily_training.py'):
        try:
            subprocess.run([sys.executable, 'daily_training.py'])
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
    else:
        print("❌ لا يوجد نظام قديم")

def main():
    """الدالة الرئيسية"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("🚀 بدء تشغيل نظام التدريب الذكي لنانو...")
    
    # فحص وتثبيت المتطلبات
    try:
        install_requirements()
    except Exception as e:
        print(f"⚠️ تحذير في تثبيت المتطلبات: {str(e)}")
    
    # فحص إعداد النظام
    if not check_system_setup():
        print("❌ فشل في إعداد النظام")
        input("اضغط أي مفتاح للخروج...")
        return
    
    # الحلقة الرئيسية
    while True:
        try:
            show_main_menu()
            choice = input("اختر رقم العملية: ").strip()
            
            if choice == '1':
                run_continuous_training()
            elif choice == '2':
                run_single_session()
            elif choice == '3':
                test_data_collection()
            elif choice == '4':
                show_statistics()
            elif choice == '5':
                create_backup()
            elif choice == '6':
                show_settings()
            elif choice == '7':
                test_text_quality()
            elif choice == '8':
                check_system_resources()
            elif choice == '9':
                run_legacy_system()
            elif choice == '0':
                print("👋 إلى اللقاء!")
                break
            else:
                print("❌ اختيار غير صحيح، حاول مرة أخرى")
            
            input("\nاضغط أي مفتاح للمتابعة...")
            
        except KeyboardInterrupt:
            print("\n👋 تم إنهاء البرنامج")
            break
        except Exception as e:
            print(f"❌ خطأ غير متوقع: {str(e)}")
            input("اضغط أي مفتاح للمتابعة...")

if __name__ == "__main__":
    main()