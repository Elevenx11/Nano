# explorer.py (v1.0 - The Explorer Module)
import requests
from bs4 import BeautifulSoup
import json
import time
import random

# --- إعدادات المستكشف ---
CORPUS_PATH = "corpus.json"
# هذا رابط لصفحة ويب تحتوي على أمثلة جمل باللهجة السعودية (كمثال أولي)
# في المستقبل، يمكننا إضافة روابط لمنتديات أو صفحات تويتر
SOURCES = [
    "https://www.almrsal.com/post/475941" 
]

def get_existing_sentences( ):
    """قراءة الجمل الموجودة حاليًا في الذاكرة لمنع التكرار."""
    try:
        with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # نستخدم set للبحث السريع
            return set(data.get("sentences", []))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_new_sentences(sentences_to_add):
    """حفظ الجمل الجديدة في ملف الذاكرة."""
    try:
        with open(CORPUS_PATH, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            # إضافة الجمل الجديدة إلى القائمة الموجودة
            data["sentences"].extend(sentences_to_add)
            # العودة إلى بداية الملف للكتابة فوقه
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            # حذف أي بيانات قديمة متبقية بعد الكتابة
            f.truncate()
    except (FileNotFoundError, json.JSONDecodeError):
        # إذا كان الملف غير موجود أو تالف، أنشئ ملفًا جديدًا
        with open(CORPUS_PATH, 'w', encoding='utf-8') as f:
            json.dump({"sentences": sentences_to_add}, f, ensure_ascii=False, indent=2)

def clean_sentence(text):
    """تنقية الجملة من الشوائب."""
    text = text.strip()
    # إزالة الكلمات أو الرموز غير المرغوب فيها (يمكن توسيع هذه القائمة)
    if "@" in text or "http" in text or "#" in text:
        return None
    # التأكد من أن الجملة ذات طول معقول
    if 3 < len(text.split( )) < 20:
        return text
    return None

def explore_and_learn():
    """
    الوظيفة الرئيسية للاستكشاف والتعلم.
    تبحث في المصادر، تنقي الجمل، وتضيفها إلى الذاكرة.
    """
    print(f"\nINFO: [{time.strftime('%Y-%m-%d %H:%M:%S')}] Nano is starting an exploration mission...")
    
    existing_sentences = get_existing_sentences()
    newly_found_sentences = []
    
    # اختيار مصدر عشوائي في كل مرة
    url = random.choice(SOURCES)
    print(f"INFO: Exploring source: {url}")

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # هذا الجزء يعتمد على هيكل الموقع المستهدف
        # هنا، نحن نبحث عن كل الفقرات <p> والنقاط <li>
        potential_sentences = soup.find_all(['p', 'li'])
        
        for sentence_tag in potential_sentences:
            text = sentence_tag.get_text()
            cleaned = clean_sentence(text)
            
            if cleaned and cleaned not in existing_sentences and cleaned not in newly_found_sentences:
                newly_found_sentences.append(cleaned)

    except Exception as e:
        print(f"ERROR: Failed to explore source {url}. Reason: {e}")
        return

    if newly_found_sentences:
        print(f"SUCCESS: Found {len(newly_found_sentences)} new sentences. Adding to memory...")
        save_new_sentences(newly_found_sentences)
    else:
        print("INFO: Did not find any new valid sentences in this mission.")
        
    print(f"INFO: [{time.strftime('%Y-%m-%d %H:%M:%S')}] Exploration mission completed.")

