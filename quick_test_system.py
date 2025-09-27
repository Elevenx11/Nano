# quick_test_system.py - اختبار سريع للنظام
from advanced_auto_scheduler import AdvancedAutoScheduler

def test_system():
    print('🔧 إنشاء المجدول...')
    scheduler = AdvancedAutoScheduler()
    
    print(f'🎯 عتبة الجودة: {scheduler.config["data_collection"]["quality_threshold"]}')
    
    print('📥 جمع البيانات...')
    data = scheduler.social_collector.collect_all_sources(max_per_source=2)
    
    if data:
        print(f'✅ تم جمع {len(data)} عناصر')
        
        # فحص جودة كل عنصر
        print('🔍 فحص الجودة:')
        for i, item in enumerate(data):
            quality = scheduler.calculate_quality_score(item)
            passed = quality >= scheduler.config['data_collection']['quality_threshold']
            print(f'   {i+1}. {quality:.3f} - {"✅" if passed else "❌"} - {item["content"][:40]}...')
        
        # تصفية البيانات عالية الجودة
        high_quality = scheduler.filter_high_quality_data(data)
        print(f'\n✨ تم اختيار {len(high_quality)} عنصر عالي الجودة')
        
        if high_quality:
            print('📝 إضافة الجمل...')
            sentences = [item['content'] for item in high_quality]
            added = scheduler.smart_trainer.update_nano_corpus(sentences)
            print(f'🎯 تم إضافة {added} جملة جديدة!')
            
            return added
        else:
            print('❌ لا توجد جمل للإضافة')
            return 0
    
    else:
        print('❌ لم يتم جمع أي بيانات')
        return 0

if __name__ == "__main__":
    try:
        result = test_system()
        print(f'\n🎉 النتيجة النهائية: {result} جملة جديدة')
    except Exception as e:
        print(f'❌ خطأ: {e}')
        import traceback
        traceback.print_exc()