# smart_auto_trainer.py - نظام التدريب الذكي التلقائي لنانو
import json
import re
import requests
import time
import schedule
import logging
from datetime import datetime, timedelta
from pathlib import Path
import random
import hashlib
from typing import List, Dict, Set
# import tweepy  # ليس مطلوب في النسخة التجريبية
# from textblob import TextBlob  # ليس مطلوب حالياً 
# import nltk  # ليس مطلوب حالياً
from collections import Counter
import threading
import sqlite3

# تحميل مكتبات NLTK المطلوبة - معطل حالياً
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('stopwords', quiet=True)
# except:
#     pass

class SmartAutoTrainer:
    """نظام التدريب الذكي التلقائي - يجمع ويحلل المحتوى من مصادر متعددة"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_database()
        self.load_config()
        
        # إعداد فلاتر اللهجة السعودية
        self.saudi_indicators = {
            'كلمات_دلالية': [
                'وش', 'شلون', 'كيفك', 'هلا', 'أهلين', 'مشكور', 'يعطيك', 'العافية',
                'بروح', 'أرجع', 'تراني', 'خلاص', 'طيب', 'زين', 'كفو', 'يالله',
                'الحين', 'شوي', 'مره', 'بطل', 'عاد', 'لا بأس', 'ما علينا',
                'استغفر', 'الله', 'يرحم', 'والديك', 'ان شاء الله', 'ما شاء الله'
            ],
            'نهايات_كلمات': ['ين', 'وه', 'اك', 'كم', 'هم', 'نا'],
            'بدايات_كلمات': ['با', 'يا', 'ما', 'لا', 'كا'],
            'تعبيرات_مميزة': [
                'الله يعطيك العافية', 'ما شاء الله', 'الحمدلله', 'بسم الله',
                'يا هلا', 'أهلا وسهلا', 'كيف الصحة', 'شلونك', 'وش اخبارك'
            ]
        }
        
        # نظام تقييم المشاعر المتطور
        self.emotion_patterns = {
            'فرح': ['فرحان', 'مبسوط', 'سعيد', 'فرحة', 'بهجة', '😊', '😄', '😂', '❤️'],
            'حزن': ['زعلان', 'حزين', 'مكتئب', 'تعبان', '😢', '😭', '💔'],
            'غضب': ['زعلان', 'متضايق', 'مقهور', 'غاضب', '😠', '😡'],
            'دعاء': ['الله', 'يرحم', 'يشفي', 'يحفظ', 'ان شاء الله', 'يا رب'],
            'تحية': ['السلام', 'صباح', 'مساء', 'أهلا', 'هلا', 'مرحبا'],
            'شكر': ['شكرا', 'مشكور', 'تسلم', 'يعطيك', 'العافية', 'ما قصرت'],
            'استفهام': ['وش', 'متى', 'وين', 'كيف', 'ليش', 'شلون'],
            'تأكيد': ['ايه', 'صح', 'بالضبط', 'زين', 'تمام', 'كذا']
        }
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            filename=f'smart_training_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """إعداد قاعدة البيانات للحفظ المؤقت والتتبع"""
        self.db_path = "smart_training_cache.db"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # إنشاء الجداول
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS collected_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                content TEXT,
                emotion_score TEXT,
                quality_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                used_in_training BOOLEAN DEFAULT FALSE,
                content_hash TEXT UNIQUE
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS training_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_date DATETIME,
                sentences_added INTEGER,
                source_breakdown TEXT,
                performance_metrics TEXT
            )
        ''')
        
        self.conn.commit()
    
    def load_config(self):
        """تحميل إعدادات التدريب"""
        self.config = {
            'training_interval_hours': 2,  # كل ساعتين
            'min_quality_score': 0.3,  # عتبة أقل لاستيعاب محتوى أكثر
            'max_daily_sentences': 500,
            'sources_enabled': {
                'twitter': True,
                'web_scraping': True,
                'user_conversations': True
            }
        }
    
    def calculate_saudi_score(self, text: str) -> float:
        """حساب مدى انتماء النص للهجة السعودية"""
        text = text.lower()
        score = 0.0
        total_checks = 0
        
        # فحص الكلمات الدلالية
        for word in self.saudi_indicators['كلمات_دلالية']:
            if word in text:
                score += 0.15
            total_checks += 0.15
        
        # فحص التعبيرات المميزة
        for expr in self.saudi_indicators['تعبيرات_مميزة']:
            if expr in text:
                score += 0.25
            total_checks += 0.25
        
        # فحص النهايات والبدايات المميزة
        words = text.split()
        for word in words:
            for ending in self.saudi_indicators['نهايات_كلمات']:
                if word.endswith(ending) and len(word) > 3:
                    score += 0.05
                    break
            total_checks += 0.05
            
            for beginning in self.saudi_indicators['بدايات_كلمات']:
                if word.startswith(beginning) and len(word) > 3:
                    score += 0.05
                    break
            total_checks += 0.05
        
        return min(score / max(total_checks, 1), 1.0) if total_checks > 0 else 0.0
    
    def analyze_emotion_context(self, text: str) -> Dict[str, float]:
        """تحليل مشاعر النص بناء على السياق"""
        text = text.lower()
        emotions = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = 0.0
            for pattern in patterns:
                if pattern in text:
                    # وزن أكبر للتعبيرات الطويلة
                    weight = len(pattern.split()) * 0.3
                    score += weight
            emotions[emotion] = min(score, 1.0)
        
        return emotions
    
    def quality_check(self, text: str) -> float:
        """تقييم جودة النص للتدريب"""
        if len(text) < 5 or len(text) > 300:  # مدى أوسع
            return 0.1
        
        # فحص اللهجة السعودية
        saudi_score = self.calculate_saudi_score(text)
        
        # فحص تنوع الكلمات
        words = text.split()
        unique_words = len(set(words))
        diversity_score = min(unique_words / max(len(words), 1), 1.0) if words else 0.5
        
        # فحص وجود رموز غير مرغوبة
        spam_indicators = ['http', 'www', '@', '#hashtag', 'follow', 'like']
        has_spam = any(indicator in text.lower() for indicator in spam_indicators)
        
        # تقييم مبسط وواقعي
        if has_spam:
            final_score = 0.1  # جودة منخفضة للspam
        else:
            # جودة أساسية + مكافآت اللهجة والتنوع
            base_score = 0.4  # جودة أساسية مقبولة
            saudi_bonus = saudi_score * 0.3  # مكافأة اللهجة
            diversity_bonus = diversity_score * 0.2  # مكافأة التنوع
            final_score = base_score + saudi_bonus + diversity_bonus
        
        return max(0.1, min(final_score, 1.0))
    
    def collect_from_social_media(self) -> List[Dict]:
        """جمع المحتوى من وسائل التواصل الاجتماعي"""
        collected_data = []
        
        # محاكاة جمع البيانات من تويتر (يحتاج API keys حقيقية)
        sample_tweets = [
            "وش رايكم بالطقس اليوم؟ حار مره والله",
            "الحمدلله على كل حال، اليوم كان يوم حلو",
            "يا هلا فيك أخوي، كيف الصحة والعائلة؟",
            "الله يعطيك العافية على هذا الشرح الوافي",
            "شكرا لك يا غالي، ما قصرت والله",
            "صباح الخير جميعاً، الله يجعله يوم مبارك",
            "وش اخبار الشغل؟ ان شاء الله كله تمام",
            "يالله نروح نتغدى، انا جوعان مره",
            "الله يشفيه ويعافيه، نسأل الله له الصحة",
            "كفو عليك، شغل متقن ما شاء الله"
        ]
        
        for tweet in sample_tweets:
            quality = self.quality_check(tweet)
            if quality >= self.config['min_quality_score']:
                emotions = self.analyze_emotion_context(tweet)
                
                collected_data.append({
                    'source': 'twitter',
                    'content': tweet,
                    'quality_score': quality,
                    'emotions': emotions,
                    'timestamp': datetime.now()
                })
        
        return collected_data
    
    def collect_from_web(self) -> List[Dict]:
        """جمع المحتوى من مواقع ويب مختلفة"""
        # هنا يمكن إضافة كود لجمع المحتوى من مواقع مختلفة
        # مثل المنتديات السعودية، المواقع الإخبارية، إلخ
        
        sample_web_content = [
            "أهلا وسهلا بكم في منتدانا الكريم",
            "نرحب بجميع الأعضاء الجدد في المجتمع",
            "شكراً لكم على التفاعل الإيجابي",
            "نتطلع لمشاركاتكم القيمة والمفيدة",
            "الله يوفق الجميع في مساعيهم",
        ]
        
        collected_data = []
        for content in sample_web_content:
            quality = self.quality_check(content)
            if quality >= self.config['min_quality_score']:
                emotions = self.analyze_emotion_context(content)
                
                collected_data.append({
                    'source': 'web',
                    'content': content,
                    'quality_score': quality,
                    'emotions': emotions,
                    'timestamp': datetime.now()
                })
        
        return collected_data
    
    def store_collected_data(self, data_list: List[Dict]):
        """حفظ البيانات المجمعة في قاعدة البيانات"""
        for item in data_list:
            content_hash = hashlib.md5(item['content'].encode()).hexdigest()
            
            try:
                self.conn.execute('''
                    INSERT INTO collected_data 
                    (source, content, emotion_score, quality_score, content_hash)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    item['source'],
                    item['content'],
                    json.dumps(item['emotions'], ensure_ascii=False),
                    item['quality_score'],
                    content_hash
                ))
                self.conn.commit()
            except sqlite3.IntegrityError:
                # المحتوى موجود مسبقاً
                pass
    
    def get_training_data(self) -> List[str]:
        """استخراج البيانات للتدريب"""
        cursor = self.conn.execute('''
            SELECT content FROM collected_data 
            WHERE used_in_training = FALSE AND quality_score >= ?
            ORDER BY quality_score DESC, timestamp DESC
            LIMIT ?
        ''', (self.config['min_quality_score'], self.config['max_daily_sentences']))
        
        sentences = [row[0] for row in cursor.fetchall()]
        
        # تحديث حالة البيانات المستخدمة
        if sentences:
            placeholders = ','.join('?' * len(sentences))
            self.conn.execute(f'''
                UPDATE collected_data 
                SET used_in_training = TRUE 
                WHERE content IN ({placeholders})
            ''', sentences)
            self.conn.commit()
        
        return sentences
    
    def update_nano_corpus(self, new_sentences: List[str]):
        """تحديث قاعدة بيانات نانو بالجمل الجديدة"""
        corpus_path = "corpus.json"
        
        try:
            # قراءة الملف الحالي
            if Path(corpus_path).exists():
                with open(corpus_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"sentences": []}
            
            current_sentences = set(data.get("sentences", []))
            added_count = 0
            
            # إضافة الجمل الجديدة
            for sentence in new_sentences:
                if sentence not in current_sentences:
                    data["sentences"].append(sentence)
                    current_sentences.add(sentence)
                    added_count += 1
            
            # حفظ الملف المحدث
            with open(corpus_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"تم إضافة {added_count} جملة جديدة إلى قاعدة البيانات")
            print(f"✅ تم إضافة {added_count} جملة جديدة")
            print(f"📊 إجمالي الجمل: {len(data['sentences'])}")
            
            return added_count
            
        except Exception as e:
            self.logger.error(f"خطأ في تحديث قاعدة البيانات: {str(e)}")
            print(f"❌ خطأ: {str(e)}")
            return 0
    
    def train_nano_system(self):
        """إعادة تدريب نظام نانو بالبيانات الجديدة"""
        try:
            # هنا يتم استدعاء نظام التدريب الأساسي
            from core.nano_brain import NanoBrain
            
            nano_brain = NanoBrain()
            nano_brain.retrain_with_new_data()
            
            print("🧠 تم إعادة تدريب نانو بنجاح")
            self.logger.info("تم إعادة تدريب نانو بالبيانات الجديدة")
            
        except Exception as e:
            print(f"❌ خطأ في التدريب: {str(e)}")
            self.logger.error(f"خطأ في تدريب نانو: {str(e)}")
    
    def run_training_cycle(self):
        """تشغيل دورة تدريب كاملة"""
        start_time = datetime.now()
        print(f"\n🚀 بدء دورة التدريب التلقائي - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # مرحلة 1: جمع البيانات
            print("📥 مرحلة 1: جمع البيانات...")
            all_data = []
            
            if self.config['sources_enabled']['twitter']:
                social_data = self.collect_from_social_media()
                all_data.extend(social_data)
                print(f"   تويتر: {len(social_data)} عنصر")
            
            if self.config['sources_enabled']['web_scraping']:
                web_data = self.collect_from_web()
                all_data.extend(web_data)
                print(f"   الويب: {len(web_data)} عنصر")
            
            # مرحلة 2: حفظ البيانات
            print("💾 مرحلة 2: حفظ البيانات...")
            self.store_collected_data(all_data)
            
            # مرحلة 3: استخراج بيانات التدريب
            print("🔍 مرحلة 3: اختيار بيانات التدريب...")
            training_sentences = self.get_training_data()
            print(f"   تم اختيار {len(training_sentences)} جملة للتدريب")
            
            # مرحلة 4: تحديث قاعدة البيانات
            print("📝 مرحلة 4: تحديث قاعدة البيانات...")
            added_count = self.update_nano_corpus(training_sentences)
            
            # مرحلة 5: إعادة التدريب
            if added_count > 0:
                print("🧠 مرحلة 5: إعادة تدريب نانو...")
                self.train_nano_system()
            else:
                print("⏭️ تم تخطي التدريب - لا توجد بيانات جديدة")
            
            # حفظ معلومات الجلسة
            end_time = datetime.now()
            duration = end_time - start_time
            
            self.conn.execute('''
                INSERT INTO training_sessions 
                (session_date, sentences_added, source_breakdown, performance_metrics)
                VALUES (?, ?, ?, ?)
            ''', (
                start_time,
                added_count,
                json.dumps({src: len([d for d in all_data if d['source'] == src]) 
                          for src in ['twitter', 'web']}, ensure_ascii=False),
                json.dumps({'duration_minutes': duration.total_seconds() / 60}, ensure_ascii=False)
            ))
            self.conn.commit()
            
            print("=" * 60)
            print(f"✅ اكتملت دورة التدريب بنجاح!")
            print(f"⏱️ المدة: {duration.total_seconds():.1f} ثانية")
            print(f"📈 جمل جديدة: {added_count}")
            
            self.logger.info(f"دورة تدريب ناجحة: {added_count} جملة جديدة في {duration.total_seconds():.1f} ثانية")
            
        except Exception as e:
            error_msg = f"خطأ في دورة التدريب: {str(e)}"
            print(f"❌ {error_msg}")
            self.logger.error(error_msg)
    
    def start_continuous_training(self):
        """بدء التدريب المستمر"""
        print("🔄 بدء نظام التدريب التلقائي المستمر")
        print(f"⏰ سيتم التدريب كل {self.config['training_interval_hours']} ساعة")
        print("🛑 اضغط Ctrl+C لإيقاف النظام")
        print("-" * 50)
        
        # جدولة التدريب
        schedule.every(self.config['training_interval_hours']).hours.do(self.run_training_cycle)
        
        # تشغيل دورة فورية
        print("▶️ تشغيل دورة تدريب فورية...")
        self.run_training_cycle()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # فحص كل دقيقة
                
        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف نظام التدريب التلقائي")
            self.logger.info("تم إيقاف النظام بواسطة المستخدم")
        finally:
            self.conn.close()
    
    def get_statistics(self):
        """إحصائيات النظام"""
        cursor = self.conn.execute('''
            SELECT 
                COUNT(*) as total_collected,
                AVG(quality_score) as avg_quality,
                SUM(CASE WHEN used_in_training = TRUE THEN 1 ELSE 0 END) as used_count,
                COUNT(DISTINCT source) as unique_sources
            FROM collected_data
        ''')
        
        stats = cursor.fetchone()
        
        print("\n📊 إحصائيات نظام التدريب الذكي")
        print("=" * 40)
        print(f"🔢 إجمالي البيانات المجمعة: {stats[0]}")
        print(f"⭐ متوسط جودة البيانات: {stats[1]:.2f}")
        print(f"🎯 البيانات المستخدمة في التدريب: {stats[2]}")
        print(f"📡 عدد المصادر: {stats[3]}")

if __name__ == "__main__":
    trainer = SmartAutoTrainer()
    
    print("🤖 نظام التدريب الذكي التلقائي لنانو")
    print("=" * 50)
    print("1. بدء التدريب المستمر")
    print("2. تشغيل دورة تدريب واحدة")
    print("3. عرض الإحصائيات")
    print("4. اختبار جودة النص")
    
    choice = input("\nاختر رقم العملية: ").strip()
    
    if choice == "1":
        trainer.start_continuous_training()
    elif choice == "2":
        trainer.run_training_cycle()
    elif choice == "3":
        trainer.get_statistics()
    elif choice == "4":
        test_text = input("أدخل النص للاختبار: ")
        quality = trainer.quality_check(test_text)
        saudi_score = trainer.calculate_saudi_score(test_text)
        emotions = trainer.analyze_emotion_context(test_text)
        
        print(f"\n📝 نتائج التحليل:")
        print(f"🎯 جودة النص: {quality:.2f}")
        print(f"🇸🇦 درجة اللهجة السعودية: {saudi_score:.2f}")
        print(f"💭 المشاعر المكتشفة: {emotions}")
    else:
        print("❌ اختيار غير صحيح")