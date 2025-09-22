# app.py (v1.1 - Synchronous Training Fix)
from flask import Flask, render_template, request, jsonify
from enhanced_nano_module import EnhancedNano
import time

# --- إعداد التطبيق والخادم ---
app = Flask(__name__)

# --- إعداد وتدريب عقل نانو (بشكل مباشر) ---
print("="*30)
print("INITIALIZING NANO'S CORE...")
print("Please wait, Nano is currently training...")

nano_mind = EnhancedNano()
start_time = time.time()

# نقوم بالتدريب الآن بشكل مباشر وننتظر حتى ينتهي
# force_retrain=True تجبر نانو على إعادة التدريب في كل مرة
# يمكنك تغييرها إلى False بعد أول تشغيل ناجح لتسريع بدء التشغيل في المستقبل
nano_mind.train(force_retrain=True) 

end_time = time.time()
print(f"NANO'S TRAINING COMPLETED in {end_time - start_time:.2f} seconds.")
print("="*30)


# --- إعداد مسارات (Routes) الخادم ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message', '')
    
    # استخدام النموذج المحسن للرد الذكي
    nano_reply = nano_mind.generate_smart_response(user_message)
    
    if not nano_reply:
        nano_reply = "والله ما فهمت عليك، قول لي مرة ثانية"
        
    return jsonify({'reply': nano_reply})


# --- تشغيل الخادم ---
if __name__ == '__main__':
    print("Starting Nano's Web Interface...")
    print("Nano is ready! Open this link in your browser: http://127.0.0.1:5000" )
    app.run(debug=False) # تم تغيير debug إلى False لتجنب إعادة التشغيل التلقائي

