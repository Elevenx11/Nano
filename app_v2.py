# app_v2.py - التطبيق الجديد مع نظام نانو المتكامل
from flask import Flask, render_template, request, jsonify
from nano_core import NanoCore
import time

# --- إعداد التطبيق والخادم ---
app = Flask(__name__)

# --- إعداد وتدريب نانو الجديد ---
print("="*50)
print("🤖 INITIALIZING NANO'S ADVANCED CORE...")
print("Loading modules, emotions, and personality...")

nano_mind = NanoCore()

print("✅ NANO'S ADVANCED SYSTEM READY!")
print("📊 Modules loaded:", len(nano_mind.modules))
print("🧠 Emotion engine: Active")
print("👤 Personality: Loaded")
print("="*50)

# --- مسارات الخادم ---

@app.route('/')
def home():
    return render_template('advanced_index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message', '')
    
    # استخدام النظام الجديد للرد الذكي مع المشاعر
    nano_reply = nano_mind.process_input(user_message)
    
    # الحصول على حالة المشاعر
    emotion_status = nano_mind.get_emotion_status()
    
    if not nano_reply:
        nano_reply = "والله ما فهمت عليك، قول لي مرة ثانية 🤔"
        
    return jsonify({
        'reply': nano_reply,
        'emotion': emotion_status['current_emotion'],
        'emotion_intensity': emotion_status['intensity'],
        'modules_active': len([m for m in nano_mind.modules if m.is_active])
    })

@app.route('/status', methods=['GET'])
def get_status():
    """الحصول على حالة نانو"""
    emotion_status = nano_mind.get_emotion_status()
    
    modules_info = []
    for module in nano_mind.modules:
        modules_info.append({
            'name': module.name,
            'type': module.module_type.value,
            'active': module.is_active
        })
    
    return jsonify({
        'emotion': emotion_status,
        'modules': modules_info,
        'conversation_history': len(nano_mind.conversation_history)
    })

@app.route('/reset_emotions', methods=['POST'])
def reset_emotions():
    """إعادة تعيين المشاعر"""
    nano_mind.emotion_engine.current_emotions = []
    return jsonify({'status': 'تم إعادة تعيين المشاعر'})

# --- تشغيل الخادم ---
if __name__ == '__main__':
    print("🚀 Starting Nano's Advanced Web Interface...")
    print("🌐 Nano is ready! Open: http://127.0.0.1:5000")
    print("💡 Features: Emotions, Modules, Personality")
    app.run(debug=False, port=5000)