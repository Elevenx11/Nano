# advanced_auto_scheduler.py - نظام الجدولة المتطور للتدريب التلقائي
import schedule
import time
import threading
import json
from datetime import datetime, timedelta
import logging
import os
from smart_auto_trainer import SmartAutoTrainer
from social_media_collector import SocialMediaCollector
import sqlite3
from typing import Dict, List
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AdvancedAutoScheduler:
    """نظام الجدولة المتطور للتدريب التلقائي المستمر"""
    
    def __init__(self, config_file: str = "scheduler_config.json"):
        self.config_file = config_file
        self.load_configuration()
        self.setup_logging()
        self.setup_database()
        
        # إعداد المدربين
        self.smart_trainer = SmartAutoTrainer()
        self.social_collector = SocialMediaCollector()
        
        # حالة النظام
        self.is_running = False
        self.current_session = None
        self.stats = {
            'total_sessions': 0,
            'successful_sessions': 0,
            'failed_sessions': 0,
            'total_sentences_collected': 0,
            'total_sentences_trained': 0,
            'last_successful_run': None,
            'average_session_duration': 0
        }
        
        # خيط منفصل للمراقبة
        self.monitor_thread = None
        self.stop_monitoring = False
    
    def load_configuration(self):
        """تحميل إعدادات النظام"""
        default_config = {
            "training_schedule": {
                "interval_hours": 2,
                "daily_limit": 1000,
                "peak_hours": [9, 14, 20],
                "avoid_hours": [1, 2, 3, 4, 5]
            },
            "data_collection": {
                "sources": {
                    "twitter": True,
                    "reddit": True,
                    "forums": True,
                    "youtube": False,
                    "instagram": False
                },
                "quality_threshold": 0.3,  # عتبة أقل للسماح بمزيد من المحتوى
                "max_per_source": 200,
                "dedupe_threshold": 0.9
            },
            "system_monitoring": {
                "max_cpu_usage": 80,
                "max_memory_usage": 85,
                "disk_space_min_gb": 5,
                "enable_notifications": True,
                "notification_email": ""
            },
            "performance": {
                "concurrent_sources": 3,
                "request_delay": 1.0,
                "retry_attempts": 3,
                "batch_size": 100
            },
            "backup": {
                "enable_backup": True,
                "backup_interval_hours": 24,
                "keep_backups_days": 7,
                "backup_path": "backups/"
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                self.config = self.deep_update(default_config, user_config)
            else:
                self.config = default_config
                self.save_configuration()
                
        except Exception as e:
            print(f"❌ خطأ في تحميل الإعدادات: {str(e)}")
            print("📝 استخدام الإعدادات الافتراضية")
            self.config = default_config
    
    def deep_update(self, base_dict: dict, update_dict: dict) -> dict:
        """تحديث عميق للقاموس"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                base_dict[key] = self.deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
        return base_dict
    
    def save_configuration(self):
        """حفظ الإعدادات"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"فشل حفظ الإعدادات: {str(e)}")
    
    def setup_logging(self):
        """إعداد نظام السجلات"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(f'scheduler_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AdvancedScheduler')
    
    def setup_database(self):
        """إعداد قاعدة بيانات الجدولة"""
        self.db_path = "scheduler_database.db"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # إنشاء الجداول
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS scheduler_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_start DATETIME,
                session_end DATETIME,
                status TEXT,
                sentences_collected INTEGER,
                sentences_trained INTEGER,
                sources_used TEXT,
                error_message TEXT,
                system_resources TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                active_connections INTEGER
            )
        ''')
        
        self.conn.commit()
    
    def check_system_resources(self) -> Dict[str, float]:
        """فحص موارد النظام"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            resources = {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'disk_usage': disk.percent,
                'available_memory_gb': memory.available / (1024**3),
                'free_disk_gb': disk.free / (1024**3)
            }
            
            # حفظ في قاعدة البيانات
            self.conn.execute('''
                INSERT INTO system_health 
                (cpu_usage, memory_usage, disk_usage, active_connections)
                VALUES (?, ?, ?, ?)
            ''', (
                resources['cpu_usage'],
                resources['memory_usage'], 
                resources['disk_usage'],
                len(psutil.pids())
            ))
            self.conn.commit()
            
            return resources
            
        except Exception as e:
            self.logger.error(f"خطأ في فحص موارد النظام: {str(e)}")
            return {}
    
    def is_optimal_time_for_training(self) -> bool:
        """تحديد ما إذا كان الوقت مناسب للتدريب"""
        current_hour = datetime.now().hour
        
        # تجنب الساعات المحددة
        if current_hour in self.config['training_schedule']['avoid_hours']:
            return False
        
        # فحص موارد النظام
        resources = self.check_system_resources()
        if resources:
            if (resources['cpu_usage'] > self.config['system_monitoring']['max_cpu_usage'] or
                resources['memory_usage'] > self.config['system_monitoring']['max_memory_usage'] or
                resources['free_disk_gb'] < self.config['system_monitoring']['disk_space_min_gb']):
                
                self.logger.warning("تم تأجيل التدريب بسبب استهلاك موارد النظام")
                return False
        
        return True
    
    def run_intelligent_training_session(self):
        """تشغيل جلسة تدريب ذكية"""
        if not self.is_optimal_time_for_training():
            self.logger.info("تم تأجيل جلسة التدريب - الوقت غير مناسب")
            return
        
        session_start = datetime.now()
        self.current_session = {
            'start_time': session_start,
            'status': 'running',
            'sentences_collected': 0,
            'sentences_trained': 0,
            'sources_used': [],
            'error_message': None
        }
        
        self.logger.info(f"🚀 بدء جلسة تدريب ذكية - {session_start.strftime('%H:%M:%S')}")
        print(f"\n{'='*60}")
        print(f"🤖 جلسة التدريب الذكي التلقائي")
        print(f"⏰ الوقت: {session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        try:
            # مرحلة 1: جمع البيانات من مصادر متعددة
            print("\n📊 مرحلة 1: جمع البيانات الذكي...")
            collected_data = self.social_collector.collect_all_sources(
                max_per_source=self.config['data_collection']['max_per_source']
            )
            
            self.current_session['sentences_collected'] = len(collected_data)
            self.current_session['sources_used'] = list(set(item['platform'] for item in collected_data))
            
            if not collected_data:
                raise Exception("لم يتم جمع أي بيانات")
            
            # مرحلة 2: تصفية وتحسين البيانات
            print(f"🔍 مرحلة 2: تصفية البيانات... ({len(collected_data)} عنصر)")
            high_quality_data = self.filter_high_quality_data(collected_data)
            
            print(f"✨ تم اختيار {len(high_quality_data)} عنصر عالي الجودة")
            
            # مرحلة 3: دمج البيانات مع النظام الذكي
            print("🧠 مرحلة 3: تحديث نظام نانو...")
            sentences = [item['content'] for item in high_quality_data]
            
            # حفظ البيانات في النظام الذكي
            self.smart_trainer.store_collected_data([
                {
                    'source': item['platform'],
                    'content': item['content'],
                    'quality_score': self.calculate_quality_score(item),
                    'emotions': self.smart_trainer.analyze_emotion_context(item['content']),
                    'timestamp': datetime.now()
                }
                for item in high_quality_data
            ])
            
            # إضافة الجمل إلى قاعدة البيانات
            added_count = self.smart_trainer.update_nano_corpus(sentences)
            self.current_session['sentences_trained'] = added_count
            
            # مرحلة 4: إعادة تدريب النظام
            if added_count > 0:
                print("🎯 مرحلة 4: إعادة تدريب النظام...")
                self.smart_trainer.train_nano_system()
                
                # تحديث الإحصائيات
                self.stats['total_sentences_collected'] += len(collected_data)
                self.stats['total_sentences_trained'] += added_count
            
            # إنهاء الجلسة بنجاح
            session_end = datetime.now()
            duration = (session_end - session_start).total_seconds()
            
            self.current_session['status'] = 'completed'
            self.stats['successful_sessions'] += 1
            self.stats['last_successful_run'] = session_end
            
            # حفظ معلومات الجلسة
            self.save_session_info()
            
            print(f"\n{'='*60}")
            print(f"✅ اكتملت الجلسة بنجاح!")
            print(f"⏱️ المدة: {duration:.1f} ثانية")
            print(f"📥 البيانات المجمعة: {len(collected_data)}")
            print(f"🎯 الجمل المدربة: {added_count}")
            print(f"📊 المصادر: {', '.join(self.current_session['sources_used'])}")
            print(f"{'='*60}")
            
            self.logger.info(f"جلسة ناجحة: {added_count} جملة جديدة في {duration:.1f} ثانية")
            
        except Exception as e:
            # معالجة الأخطاء
            error_msg = str(e)
            self.current_session['status'] = 'failed'
            self.current_session['error_message'] = error_msg
            
            self.stats['failed_sessions'] += 1
            
            print(f"\n❌ فشلت الجلسة: {error_msg}")
            self.logger.error(f"فشل في جلسة التدريب: {error_msg}")
            
            # حفظ معلومات الجلسة حتى لو فشلت
            self.save_session_info()
            
            # إرسال تنبيه في حالة الفشل المتكرر
            if self.stats['failed_sessions'] >= 3:
                self.send_notification(f"تحذير: فشل {self.stats['failed_sessions']} جلسات متتالية")
        
        finally:
            # تحديث الإحصائيات العامة
            self.stats['total_sessions'] += 1
            self.current_session = None
    
    def filter_high_quality_data(self, data: List[Dict]) -> List[Dict]:
        """تصفية البيانات عالية الجودة"""
        threshold = self.config['data_collection']['quality_threshold']
        
        high_quality = []
        for item in data:
            quality_score = self.calculate_quality_score(item)
            if quality_score >= threshold:
                item['calculated_quality'] = quality_score
                high_quality.append(item)
        
        # ترتيب حسب الجودة
        return sorted(high_quality, key=lambda x: x['calculated_quality'], reverse=True)
    
    def calculate_quality_score(self, item: Dict) -> float:
        """حساب درجة جودة العنصر"""
        content = item['content']
        
        try:
            # استخدام نظام التقييم من SmartTrainer
            base_quality = self.smart_trainer.quality_check(content)
        except:
            # في حالة فشل التقييم، استخدم تقييم بسيط
            if len(content) >= 10 and len(content) <= 200:
                base_quality = 0.5  # جودة مقبولة
            else:
                base_quality = 0.2  # جودة ضعيفة
        
        # تعديلات إضافية حسب المصدر والتفاعل
        platform_bonus = {
            'twitter': 0.2,
            'reddit': 0.25,
            'forum': 0.3,
            'youtube': 0.15,
            'instagram': 0.15
        }
        
        engagement_bonus = min(item.get('engagement', 0) / 50, 0.2)  # مكافأة أفضل للتفاعل
        platform_score = platform_bonus.get(item.get('platform', ''), 0.1)
        
        final_score = min(base_quality + platform_score + engagement_bonus, 1.0)
        
        return final_score
    
    def save_session_info(self):
        """حفظ معلومات الجلسة"""
        if not self.current_session:
            return
        
        try:
            session_end = datetime.now()
            resources = self.check_system_resources()
            
            self.conn.execute('''
                INSERT INTO scheduler_sessions 
                (session_start, session_end, status, sentences_collected, 
                 sentences_trained, sources_used, error_message, system_resources)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.current_session['start_time'],
                session_end,
                self.current_session['status'],
                self.current_session['sentences_collected'],
                self.current_session['sentences_trained'],
                json.dumps(self.current_session['sources_used'], ensure_ascii=False),
                self.current_session['error_message'],
                json.dumps(resources, ensure_ascii=False)
            ))
            
            self.conn.commit()
            
        except Exception as e:
            self.logger.error(f"خطأ في حفظ معلومات الجلسة: {str(e)}")
    
    def send_notification(self, message: str):
        """إرسال تنبيهات"""
        if not self.config['system_monitoring']['enable_notifications']:
            return
        
        # يمكن إضافة إرسال بريد إلكتروني أو تنبيهات أخرى هنا
        self.logger.warning(f"تنبيه: {message}")
        print(f"🔔 {message}")
    
    def create_backup(self):
        """إنشاء نسخة احتياطية"""
        if not self.config['backup']['enable_backup']:
            return
        
        try:
            backup_dir = self.config['backup']['backup_path']
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f"nano_backup_{timestamp}.tar.gz")
            
            # نسخ الملفات المهمة
            import tarfile
            with tarfile.open(backup_file, 'w:gz') as tar:
                if os.path.exists('corpus.json'):
                    tar.add('corpus.json')
                if os.path.exists(self.db_path):
                    tar.add(self.db_path)
                if os.path.exists('smart_training_cache.db'):
                    tar.add('smart_training_cache.db')
            
            print(f"💾 تم إنشاء نسخة احتياطية: {backup_file}")
            self.logger.info(f"نسخة احتياطية: {backup_file}")
            
            # حذف النسخ القديمة
            self.cleanup_old_backups()
            
        except Exception as e:
            self.logger.error(f"فشل إنشاء النسخة الاحتياطية: {str(e)}")
    
    def cleanup_old_backups(self):
        """حذف النسخ الاحتياطية القديمة"""
        try:
            backup_dir = self.config['backup']['backup_path']
            keep_days = self.config['backup']['keep_backups_days']
            
            if not os.path.exists(backup_dir):
                return
            
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            
            for filename in os.listdir(backup_dir):
                if filename.startswith('nano_backup_') and filename.endswith('.tar.gz'):
                    filepath = os.path.join(backup_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    
                    if file_time < cutoff_date:
                        os.remove(filepath)
                        self.logger.info(f"حذف نسخة احتياطية قديمة: {filename}")
        
        except Exception as e:
            self.logger.error(f"خطأ في تنظيف النسخ الاحتياطية: {str(e)}")
    
    def start_monitoring(self):
        """بدء مراقبة النظام"""
        def monitor_loop():
            while not self.stop_monitoring:
                try:
                    resources = self.check_system_resources()
                    
                    # فحص حالة النظام
                    if resources:
                        if resources['cpu_usage'] > 90:
                            self.send_notification(f"استهلاك CPU عالي: {resources['cpu_usage']:.1f}%")
                        
                        if resources['memory_usage'] > 90:
                            self.send_notification(f"استهلاك ذاكرة عالي: {resources['memory_usage']:.1f}%")
                        
                        if resources['free_disk_gb'] < 1:
                            self.send_notification(f"مساحة القرص منخفضة: {resources['free_disk_gb']:.1f} GB")
                    
                    time.sleep(300)  # فحص كل 5 دقائق
                    
                except Exception as e:
                    self.logger.error(f"خطأ في مراقبة النظام: {str(e)}")
                    time.sleep(60)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("تم بدء مراقبة النظام")
    
    def start_scheduler(self):
        """بدء جدولة التدريب المتقدمة"""
        self.is_running = True
        interval_hours = self.config['training_schedule']['interval_hours']
        
        print(f"🔄 بدء نظام الجدولة المتطور")
        print(f"⏰ التدريب كل {interval_hours} ساعة")
        print(f"📊 حد الجمل اليومي: {self.config['training_schedule']['daily_limit']}")
        print(f"🛑 اضغط Ctrl+C لإيقاف النظام")
        print("-" * 60)
        
        # جدولة التدريب
        schedule.every(interval_hours).hours.do(self.run_intelligent_training_session)
        
        # جدولة النسخ الاحتياطية
        if self.config['backup']['enable_backup']:
            schedule.every(self.config['backup']['backup_interval_hours']).hours.do(self.create_backup)
        
        # بدء المراقبة
        self.start_monitoring()
        
        # تشغيل جلسة فورية
        print("▶️ تشغيل جلسة تدريب فورية...")
        self.run_intelligent_training_session()
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(30)  # فحص كل 30 ثانية
                
        except KeyboardInterrupt:
            print("\n🛑 إيقاف النظام...")
            self.stop_system()
        
        except Exception as e:
            self.logger.error(f"خطأ في الجدولة: {str(e)}")
            print(f"❌ خطأ في النظام: {str(e)}")
            self.stop_system()
    
    def stop_system(self):
        """إيقاف النظام"""
        self.is_running = False
        self.stop_monitoring = True
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        
        # إغلاق الاتصالات
        if hasattr(self.social_collector, 'close'):
            self.social_collector.close()
        
        if hasattr(self.smart_trainer, 'conn'):
            self.smart_trainer.conn.close()
        
        self.conn.close()
        
        print("✅ تم إيقاف النظام بأمان")
        self.logger.info("تم إيقاف النظام بواسطة المستخدم")
    
    def get_detailed_statistics(self):
        """إحصائيات مفصلة للنظام"""
        print(f"\n📊 إحصائيات نظام التدريب المتطور")
        print(f"{'='*50}")
        print(f"🔢 إجمالي الجلسات: {self.stats['total_sessions']}")
        print(f"✅ جلسات ناجحة: {self.stats['successful_sessions']}")
        print(f"❌ جلسات فاشلة: {self.stats['failed_sessions']}")
        print(f"📥 إجمالي الجمل المجمعة: {self.stats['total_sentences_collected']}")
        print(f"🎯 إجمالي الجمل المدربة: {self.stats['total_sentences_trained']}")
        
        if self.stats['last_successful_run']:
            print(f"⏰ آخر جلسة ناجحة: {self.stats['last_successful_run'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # إحصائيات من قاعدة البيانات
        try:
            cursor = self.conn.execute('''
                SELECT COUNT(*), AVG(sentences_trained), SUM(sentences_collected)
                FROM scheduler_sessions WHERE status = 'completed'
            ''')
            db_stats = cursor.fetchone()
            
            if db_stats and db_stats[0] > 0:
                print(f"📈 متوسط الجمل لكل جلسة: {db_stats[1]:.1f}")
        
        except Exception as e:
            self.logger.error(f"خطأ في استخراج الإحصائيات: {str(e)}")
        
        print(f"{'='*50}")

if __name__ == "__main__":
    scheduler = AdvancedAutoScheduler()
    
    print("🤖 نظام الجدولة المتطور للتدريب التلقائي")
    print("="*60)
    print("1. بدء التدريب التلقائي المستمر")
    print("2. تشغيل جلسة تدريب واحدة")
    print("3. عرض الإحصائيات المفصلة")
    print("4. إنشاء نسخة احتياطية")
    print("5. فحص موارد النظام")
    print("6. إعدادات النظام")
    
    choice = input("\nاختر رقم العملية: ").strip()
    
    try:
        if choice == "1":
            scheduler.start_scheduler()
        elif choice == "2":
            scheduler.run_intelligent_training_session()
        elif choice == "3":
            scheduler.get_detailed_statistics()
        elif choice == "4":
            scheduler.create_backup()
        elif choice == "5":
            resources = scheduler.check_system_resources()
            print("\n🖥️ موارد النظام الحالية:")
            for key, value in resources.items():
                print(f"   {key}: {value}")
        elif choice == "6":
            print(f"\n⚙️ الإعدادات الحالية:")
            print(json.dumps(scheduler.config, ensure_ascii=False, indent=2))
        else:
            print("❌ اختيار غير صحيح")
    
    finally:
        if hasattr(scheduler, 'stop_system'):
            scheduler.stop_system()