# app.py (v2.0 - Scheduled Background Training)
from flask import Flask, render_template, request, jsonify
from riyadh_dialect_generative_module import RiyadhDialectGenerative
import time
import schedule
import threading

# --- إعداد التطبيق والخادم ---
app = Flask(__name__)

# --- إعداد عقل نانو ---
print("="*30)
print("INITIALIZING NANO'S CORE...")
nano_mind = RiyadhDialectGenerative()

# --- الجزء الجديد: نظام التدريب المجدول ---

def training_job():
    """
    هذه هي وظيفة التدريب التي سيتم استدعاؤها بشكل دوري.
    """
    print("\n-------------------------------------------------")
    print(f"INFO: [{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting scheduled training...")
    
    # نجبر نانو على إعادة التدريب من ملف البيانات الخام
    nano_mind.train(force_retrain=True)
    
    print(f"INFO: [{time.strftime('%Y-%m-%d %H:%M:%S')}] Scheduled training completed.")
    print("-------------------------------------------------\n")

def run_scheduler():
    """
    هذه الدالة تقوم بتشغيل الجدول الزمني بشكل مستمر في الخلفية.
    """
    # جدولة وظيفة التدريب لتعمل كل 5 ساعات
    schedule.every(5).hours.do(training_job)
    
    # حلقة لا نهائية لتشغيل المهام المجدولة
    while True:
        schedule.run_pending()
        time.sleep(1) # انتظر ثانية واحدة قبل التحقق مرة أخرى

# --- نهاية الجزء الجديد ---


# --- إعداد مسارات (Routes) الخادم ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message', '')
    start_word = user_message.strip().split()[0] if user_message.strip() else None
    
    nano_reply = nano_mind.generate_sentence(start_word=start_word)
    
    if not nano_reply:
        nano_reply = nano_mind.generate_sentence()
        
    return jsonify({'reply': nano_reply})


# --- تشغيل الخادم والتدريب ---
if __name__ == '__main__':
    # 1. قم بالتدريب الأولي فورًا عند بدء التشغيل
    print("Performing initial training...")
    training_job()
    
    # 2. قم بتشغيل نظام الجدولة في خيط خلفي
    print("Starting background scheduler...")
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # هذا يجعل الخيط يتوقف عند إغلاق البرنامج الرئيسي
    scheduler_thread.start()
    
    # 3. قم بتشغيل واجهة الويب
    print("Starting Nano's Web Interface...")
    print("Nano is ready! Open this link in your browser: http://127.0.0.1:5000" )
    app.run(debug=False)
