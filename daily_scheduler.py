# daily_scheduler.py - جدولة التدريب اليومي لنانو
import schedule
import time
import subprocess
import logging
from datetime import datetime
from daily_training import DailyTrainer

# إعداد نظام اللوقات
logging.basicConfig(
    filename='nano_training.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_daily_training():
    """تشغيل التدريب اليومي"""
    try:
        logging.info("بدء التدريب اليومي التلقائي")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] بدء التدريب اليومي...")
        
        trainer = DailyTrainer()
        trainer.run_daily_training()
        
        logging.info("اكتمل التدريب اليومي بنجاح")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] اكتمل التدريب اليومي!")
        
    except Exception as e:
        error_msg = f"خطأ في التدريب اليومي: {str(e)}"
        logging.error(error_msg)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {error_msg}")

def schedule_daily_training():
    """جدولة التدريب ليتم يومياً في الساعة 9 صباحاً"""
    schedule.every().day.at("09:00").do(run_daily_training)
    
    print("تم تشغيل جدولة التدريب اليومي")
    print("سيتم تشغيل التدريب كل يوم في الساعة 9:00 صباحاً")
    print("اضغط Ctrl+C لإيقاف الجدولة")
    print("-" * 50)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # فحص كل دقيقة
            
    except KeyboardInterrupt:
        print("\nتم إيقاف جدولة التدريب اليومي")
        logging.info("تم إيقاف جدولة التدريب اليومي بواسطة المستخدم")

if __name__ == "__main__":
    # تشغيل تدريب فوري ثم بدء الجدولة
    print("تشغيل تدريب فوري أولاً...")
    run_daily_training()
    
    # بدء الجدولة
    schedule_daily_training()