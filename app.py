# app.py (v3.0 - Self-Learning & Exploration)
from flask import Flask, render_template, request, jsonify
from riyadh_dialect_generative_module import RiyadhDialectGenerative
from explorer import explore_and_learn # <-- استيراد وظيفة الاستكشاف الجديدة
import time
import schedule
import threading

# --- إعداد التطبيق والخادم ---
app = Flask(__name__)

# --- إعداد عقل نانو ---
print("="*30)
print("INITIALIZING NANO'S CORE...")
nano_mind = RiyadhDialectGenerative()

# --- نظام التعلم المجدول والمستمر ---

def learning_cycle_job():
    """
    دورة التعلم الكاملة: استكشاف ثم تدريب.
    """
    print("\n" + "="*50)
    print(f"INFO: [{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting a new learning cycle...")
    
    # الخطوة 1: الاستكشاف لجلب بيانات جديدة
    explore_and_learn()
    
    # الخطوة 2: التدريب على كل البيانات (القديمة والجديدة)
    print(f"INFO: [{time.strftime('%Y-%m-%d %H:%M:%S')}] Retraining the mind with new knowledge...")
    nano_mind.train(force_retrain=True)
    
    print(f"INFO: [{time.strftime('%Y-%m-%d %H:%M:%S')}] Learning cycle completed.")
    print("="*50 + "\n")

def run_scheduler():
    """
    تشغيل الجدول الزمني الذي يدير دورات التعلم.
    """
    # جدولة دورة التعلم لتعمل كل 5 ساعات
    schedule.every(5).hours.do(learning_cycle_job)
    
    while True:
        schedule.run_pending()
        time.sleep(60) # التحقق كل دقيقة

# --- نهاية الجزء الجديد ---


# --- إعداد مسارات الخادم ---
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


# --- تشغيل الخادم ودورة التعلم ---
if __name__ == '__main__':
    # 1. قم بدورة تعلم أولية فورًا عند بدء التشغيل
    print("Performing initial learning cycle...")
    learning_cycle_job()
    
    # 2. قم بتشغيل نظام الجدولة في خيط خلفي
    print("Starting background self-learning scheduler...")
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # 3. قم بتشغيل واجهة الويب
    print("Starting Nano's Web Interface...")
    print("Nano is ready and will now learn on its own! Open this link: http://127.0.0.1:5000" )
    app.run(debug=False)
