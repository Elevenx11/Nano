# social_media_collector.py - جمع البيانات من وسائل التواصل الاجتماعي
import requests
import json
import re
import time
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import hashlib
from urllib.parse import quote_plus
import random

class SocialMediaCollector:
    """جامع البيانات من مواقع التواصل الاجتماعي"""
    
    def __init__(self):
        self.setup_logging()
        
        # قائمة الكلمات المفتاحية للبحث عن المحتوى السعودي
        self.saudi_keywords = [
            "السعودية", "الرياض", "جدة", "الدمام", "مكة", "المدينة",
            "وش رايكم", "كيفكم", "شلونكم", "الله يعطيكم العافية",
            "صباح الخير", "مساء الخير", "كل عام وانتم بخير",
            "الله يوفقك", "ان شاء الله", "ما شاء الله", "بسم الله",
            "يالله", "طيب", "زين", "كفو", "مشكور", "تسلم",
            "الحين", "شوي", "مره", "بطل", "عاد", "خلاص"
        ]
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            filename=f'social_collector_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)
    
    def collect_from_twitter_api(self, keywords: List[str], max_results: int = 100) -> List[Dict]:
        """جمع البيانات من تويتر باستخدام API"""
        collected_data = []
        
        # بيانات تجريبية من تويتر
        sample_tweets = [
            {
                'text': "وش رايكم بالطقس اليوم؟ حار مره والله ☀️",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user1', 'location': 'الرياض'},
                'public_metrics': {'like_count': 15, 'retweet_count': 3}
            },
            {
                'text': "الحمدلله على كل حال، اليوم كان يوم حلو 😊",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user2', 'location': 'جدة'},
                'public_metrics': {'like_count': 22, 'retweet_count': 8}
            },
            {
                'text': "يا هلا فيك أخوي، كيف الصحة والعائلة؟",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user3', 'location': 'الدمام'},
                'public_metrics': {'like_count': 31, 'retweet_count': 5}
            },
            {
                'text': "الله يعطيك العافية على هذا الشرح الوافي 👍",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user4', 'location': 'مكة'},
                'public_metrics': {'like_count': 45, 'retweet_count': 12}
            },
            {
                'text': "شكرا لك يا غالي، ما قصرت والله",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user5', 'location': 'المدينة'},
                'public_metrics': {'like_count': 18, 'retweet_count': 4}
            },
            {
                'text': "صباح الخير عليكم، كيف نومكم؟",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user6', 'location': 'الرياض'},
                'public_metrics': {'like_count': 12, 'retweet_count': 2}
            },
            {
                'text': "والله انا من جد استفدت من هالمعلومات",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user7', 'location': 'جدة'},
                'public_metrics': {'like_count': 28, 'retweet_count': 7}
            },
            {
                'text': "الله يسعدك ويوفقك في كل خطوة تخطيها",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user8', 'location': 'الطائف'},
                'public_metrics': {'like_count': 41, 'retweet_count': 11}
            },
            {
                'text': "وش برامجكم للعطلة هالأيام؟ ابغى اروح مع العيال",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user9', 'location': 'الرياض'},
                'public_metrics': {'like_count': 23, 'retweet_count': 6}
            },
            {
                'text': "انشالله الجو يعتدل قريباً، مااقدر على هالحر",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user10', 'location': 'جدة'},
                'public_metrics': {'like_count': 19, 'retweet_count': 4}
            },
            {
                'text': "يااااه الحمدلله خلصنا من الامتحانات بالسلامة",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user11', 'location': 'الدمام'},
                'public_metrics': {'like_count': 33, 'retweet_count': 9}
            },
            {
                'text': "اليوم جربت مطعم جديد في الحي، والله اكله لذيذ",
                'created_at': datetime.now().isoformat(),
                'user': {'username': 'user12', 'location': 'الرياض'},
                'public_metrics': {'like_count': 27, 'retweet_count': 5}
            }
        ]
        
        for tweet_data in sample_tweets[:max_results]:
            collected_data.append({
                'platform': 'twitter',
                'content': tweet_data['text'],
                'timestamp': tweet_data['created_at'],
                'engagement': tweet_data['public_metrics']['like_count'] + tweet_data['public_metrics']['retweet_count'],
                'location': tweet_data['user'].get('location', ''),
                'source_url': f"https://twitter.com/{tweet_data['user']['username']}"
            })
        
        self.logger.info(f"تم جمع {len(collected_data)} تغريدة من Twitter")
        return collected_data
    
    def collect_from_reddit(self, subreddits: List[str] = ['saudiarabia', 'riyadh'], max_posts: int = 50) -> List[Dict]:
        """جمع البيانات من Reddit"""
        collected_data = []
        
        # بيانات تجريبية من Reddit
        sample_posts = [
            {
                'title': "أفضل مطاعم في الرياض - شاركوا تجاربكم",
                'selftext': "وش أفضل مطعم رحتوا له في الرياض؟ ابغى أجرب أماكن جديدة",
                'created_utc': time.time(),
                'score': 25,
                'num_comments': 15,
                'subreddit': 'riyadh'
            },
            {
                'title': "نصائح للطقس الحار",
                'selftext': "الجو حار مره هالأيام، وش أفضل الطرق للتعامل معه؟",
                'created_utc': time.time(),
                'score': 42,
                'num_comments': 23,
                'subreddit': 'saudiarabia'
            },
            {
                'title': "تجربتي مع الشغل في الرياض",
                'selftext': "حبيت أشارككم تجربتي الجديدة في العمل، والله صار لي شهر وأنا مبسوط",
                'created_utc': time.time(),
                'score': 67,
                'num_comments': 31,
                'subreddit': 'riyadh'
            },
            {
                'title': "استفسار عن جامعات المملكة",
                'selftext': "ابغى اعرف ايش أفضل جامعة لتخصص الهندسة؟ ياليت تساعدوني",
                'created_utc': time.time(),
                'score': 34,
                'num_comments': 19,
                'subreddit': 'saudiarabia'
            },
            {
                'title': "كيف الوضع مع توصيل الطلبات",
                'selftext': "صار لي فترة استخدم تطبيقات التوصيل، بس احس الأسعار غالية شوي",
                'created_utc': time.time(),
                'score': 18,
                'num_comments': 8,
                'subreddit': 'riyadh'
            },
            {
                'title': "وش أفضل ماركات في الرياض",
                'selftext': "ابغى اشتري هدايا للعائلة، وش تنصحوني من الماركات؟",
                'created_utc': time.time(),
                'score': 29,
                'num_comments': 16,
                'subreddit': 'riyadh'
            },
            {
                'title': "تجربتي مع طلب الوظائف",
                'selftext': "خلصت قبل كم شهر وابغى اشتغل، وش نصائحكم للتقديم؟",
                'created_utc': time.time(),
                'score': 45,
                'num_comments': 22,
                'subreddit': 'saudiarabia'
            }
        ]
        
        for post in sample_posts[:max_posts]:
            if post['selftext']:  # فقط المنشورات التي تحتوي على نص
                collected_data.append({
                    'platform': 'reddit',
                    'content': f"{post['title']} - {post['selftext']}",
                    'timestamp': datetime.fromtimestamp(post['created_utc']).isoformat(),
                    'engagement': post['score'] + post['num_comments'],
                    'location': 'Saudi Arabia',
                    'source_url': f"https://reddit.com/r/{post['subreddit']}"
                })
        
        self.logger.info(f"تم جمع {len(collected_data)} منشور من Reddit")
        return collected_data
    
    def collect_from_forums(self) -> List[Dict]:
        """جمع البيانات من المنتديات العربية والسعودية"""
        collected_data = []
        
        # بيانات تجريبية من المنتديات
        sample_forum_posts = [
            {
                'content': "السلام عليكم ورحمة الله وبركاته، كيفكم يا شباب؟",
                'forum': 'hawamer',
                'timestamp': datetime.now().isoformat(),
                'replies': 12
            },
            {
                'content': "جربت المطعم الجديد في الرياض، والله كان أكله زين مره",
                'forum': 'saudieng',
                'timestamp': datetime.now().isoformat(),
                'replies': 8
            },
            {
                'content': "وش رايكم في الأجواء الحلوة هالأيام؟ الحمدلله انكسر الحر شوي",
                'forum': 'almrsal',
                'timestamp': datetime.now().isoformat(),
                'replies': 15
            },
            {
                'content': "ابغى اسافر خارج المملكة، وش تنصحوني من الدول؟",
                'forum': 'travel_ksa',
                'timestamp': datetime.now().isoformat(),
                'replies': 23
            },
            {
                'content': "الحمدلله خلصت الجامعة اخيراً، ادعولي اشتغل شغل زين",
                'forum': 'graduates',
                'timestamp': datetime.now().isoformat(),
                'replies': 7
            }
        ]
        
        for post in sample_forum_posts:
            collected_data.append({
                'platform': 'forum',
                'content': post['content'],
                'timestamp': post['timestamp'],
                'engagement': post['replies'],
                'location': 'Saudi Arabia',
                'source_url': f"https://www.{post['forum']}.com"
            })
        
        self.logger.info(f"تم جمع {len(collected_data)} منشور من المنتديات")
        return collected_data
    
    def collect_all_sources(self, max_per_source: int = 100) -> List[Dict]:
        """جمع البيانات من جميع المصادر"""
        all_data = []
        
        print("🔄 بدء جمع البيانات من جميع المصادر...")
        
        try:
            # جمع من تويتر
            print("📱 جمع من Twitter...")
            twitter_data = self.collect_from_twitter_api(
                keywords=self.saudi_keywords[:5], 
                max_results=min(max_per_source, 8)  # حد أقصى للبيانات التجريبية
            )
            all_data.extend(twitter_data)
            
            # جمع من Reddit
            print("🔴 جمع من Reddit...")
            reddit_data = self.collect_from_reddit(max_posts=min(max_per_source, 5))
            all_data.extend(reddit_data)
            
            # جمع من المنتديات
            print("💬 جمع من المنتديات...")
            forum_data = self.collect_from_forums()
            all_data.extend(forum_data)
            
            # تطبيق التصفية
            filtered_data = []
            for item in all_data:
                if self.filter_saudi_content(item['content']):
                    item['content_hash'] = hashlib.md5(
                        item['content'].encode('utf-8')
                    ).hexdigest()
                    filtered_data.append(item)
            
            print(f"✅ تم جمع {len(all_data)} عنصر، وتمت تصفية {len(filtered_data)} عنصر مناسب")
            self.logger.info(f"جمع البيانات: {len(all_data)} الكل، {len(filtered_data)} مصفى")
            
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"خطأ في جمع البيانات: {str(e)}")
            print(f"❌ خطأ في جمع البيانات: {str(e)}")
            return []
    
    def filter_saudi_content(self, content: str) -> bool:
        """تصفية المحتوى للتأكد من أنه باللهجة السعودية"""
        content_lower = content.lower()
        
        # فحص الكلمات المفتاحية السعودية
        saudi_word_count = sum(1 for keyword in self.saudi_keywords 
                              if keyword.lower() in content_lower)
        
        # إذا وجد كلمة واحدة أو أكثر من الكلمات السعودية
        return saudi_word_count >= 1
    
    def close(self):
        """إغلاق الاتصالات"""
        # لا توجد اتصالات للإغلاق في النسخة المبسطة
        self.logger.info("تم إغلاق جامع البيانات")

if __name__ == "__main__":
    collector = SocialMediaCollector()
    
    try:
        # اختبار جمع البيانات
        collected_data = collector.collect_all_sources(max_per_source=10)
        
        # عرض النتائج
        print(f"\n📊 تم جمع {len(collected_data)} عنصر إجمالياً")
        
        if collected_data:
            print("\n📄 عينة من البيانات المجمعة:")
            for i, item in enumerate(collected_data[:5]):
                print(f"   {i+1}. [{item['platform']}] {item['content'][:60]}...")
                
        # حفظ البيانات (اختياري)
        with open(f"collected_sample_{datetime.now().strftime('%Y%m%d_%H%M')}.json", 'w', encoding='utf-8') as f:
            json.dump(collected_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 تم حفظ البيانات في ملف JSON")
        
    finally:
        collector.close()