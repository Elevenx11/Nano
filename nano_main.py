# nano_main.py - التطبيق الرئيسي الجديد لنانو
import sys
import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
import json

# إضافة مجلد core للمسار
sys.path.append(str(Path(__file__).parent / "core"))

# استيراد عقل نانو
from core.nano_brain import NanoBrain, NanoResponse

class NanoApp:
    """التطبيق الرئيسي لنانو"""
    
    def __init__(self):
        self.brain = NanoBrain("data")
        self.app = Flask(__name__)
        self.setup_routes()
        
        print("🤖 نانو يستيقظ...")
        print(f"📊 حالة النظام: {self.get_startup_status()}")
        
    def setup_routes(self):
        """إعداد مسارات Flask"""
        
        @self.app.route('/')
        def index():
            return render_template('nano_interface.html')
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            try:
                data = request.json
                user_input = data.get('message', '').strip()
                
                if not user_input:
                    return jsonify({'error': 'رسالة فارغة'}), 400
                
                # توليد الرد من العقل
                nano_response = self.brain.generate_response(user_input)
                
                return jsonify({
                    'response': nano_response.text,
                    'confidence': nano_response.confidence,
                    'method': nano_response.method_used,
                    'mood': nano_response.personality_mood,
                    'emotion': nano_response.emotion_detected,
                    'reasoning': nano_response.reasoning,
                    'debug': nano_response.thought_process if self.is_debug_mode() else None
                })
                
            except Exception as e:
                return jsonify({'error': f'خطأ: {str(e)}'}), 500
        
        @self.app.route('/status')
        def status():
            return jsonify(self.brain.get_system_status())
        
        @self.app.route('/reset', methods=['POST'])
        def reset():
            self.brain.reset_conversation()
            return jsonify({'message': 'تم إعادة تعيين المحادثة'})
        
        @self.app.route('/debug/<user_input>')
        def debug(user_input):
            debug_info = self.brain.get_debug_info(user_input)
            return jsonify(debug_info)
        
        @self.app.route('/save', methods=['POST'])
        def save_state():
            try:
                self.brain.save_brain_state()
                return jsonify({'message': 'تم حفظ حالة العقل بنجاح'})
            except Exception as e:
                return jsonify({'error': f'فشل الحفظ: {str(e)}'}), 500

    def get_startup_status(self):
        """حالة النظام عند البدء"""
        status = self.brain.get_system_status()
        return f"المزاج: {status['personality']['current_mood']}, المحادثات: {status['performance']['total_interactions']}"
    
    def is_debug_mode(self):
        """فحص وضع التشخيص"""
        return os.getenv('NANO_DEBUG', 'false').lower() == 'true'
    
    def run_console_mode(self):
        """تشغيل نانو في وضع سطر الأوامر"""
        print("💬 وضع المحادثة المباشرة - اكتب 'خروج' للإنهاء")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 أنت: ").strip()
                
                if user_input.lower() in ['خروج', 'exit', 'quit']:
                    print("👋 نانو: مع السلامة!")
                    break
                
                if user_input.lower() == 'حالة':
                    status = self.brain.get_system_status()
                    print(f"📊 الحالة: {json.dumps(status, ensure_ascii=False, indent=2)}")
                    continue
                
                if user_input.lower() == 'حفظ':
                    self.brain.save_brain_state()
                    print("💾 تم حفظ حالة العقل")
                    continue
                
                if user_input.lower() == 'إعادة':
                    self.brain.reset_conversation()
                    print("🔄 تم إعادة تعيين المحادثة")
                    continue
                
                if not user_input:
                    continue
                
                # توليد الرد
                response = self.brain.generate_response(user_input)
                
                # طباعة الرد
                print(f"🤖 نانو: {response.text}")
                
                # معلومات إضافية في وضع التشخيص
                if self.is_debug_mode():
                    print(f"   📈 الثقة: {response.confidence:.2f}")
                    print(f"   🎭 المزاج: {response.personality_mood}")
                    print(f"   💭 المشاعر: {response.emotion_detected}")
                    print(f"   ⚙️  الطريقة: {response.method_used}")
                
            except KeyboardInterrupt:
                print("\n👋 نانو: مع السلامة!")
                break
            except Exception as e:
                print(f"❌ خطأ: {e}")
        
        # حفظ الحالة عند الخروج
        self.brain.save_brain_state()
        print("💾 تم حفظ حالة العقل تلقائياً")

    def run_web_mode(self, host='127.0.0.1', port=5000):
        """تشغيل نانو في وضع الويب"""
        print(f"🌐 تشغيل نانو على http://{host}:{port}")
        self.app.run(host=host, port=port, debug=self.is_debug_mode())

def main():
    """الدالة الرئيسية"""
    
    # التحقق من وجود مجلد templates
    templates_dir = Path(__file__).parent / "templates"
    if not templates_dir.exists():
        templates_dir.mkdir()
        
        # إنشاء قالب HTML بسيط
        html_template = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نانو - المساعد الذكي</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #667eea;
            margin: 0;
            font-size: 2.5em;
        }
        .status-bar {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 0.9em;
            color: #666;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            background: #fafafa;
        }
        .message {
            margin: 15px 0;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 70%;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-right: auto;
            text-align: right;
        }
        .nano-message {
            background: white;
            border: 2px solid #667eea;
            margin-left: auto;
            text-align: left;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        .input-container input {
            flex: 1;
            padding: 15px;
            border: 2px solid #667eea;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
        }
        .input-container button {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        .input-container button:hover {
            background: #5a67d8;
        }
        .debug-info {
            background: #f1f5f9;
            padding: 10px;
            margin-top: 5px;
            border-radius: 8px;
            font-size: 0.8em;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 نانو</h1>
            <p>المساعد الذكي باللهجة السعودية</p>
        </div>
        
        <div class="status-bar">
            <span>📊 المزاج: <span id="mood">يتم التحميل...</span></span> |
            <span>💭 المحادثات: <span id="conversations">0</span></span> |
            <span>⚡ الحالة: <span id="status">متصل</span></span>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message nano-message">
                السلام عليكم! أنا نانو، مساعدك الذكي 😊<br>
                كيف يمكنني مساعدتك اليوم؟
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="اكتب رسالتك هنا..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // إضافة رسالة المستخدم
            addMessage(message, 'user');
            input.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addMessage('خطأ: ' + data.error, 'nano');
                } else {
                    addMessage(data.response, 'nano', {
                        confidence: data.confidence,
                        mood: data.mood,
                        method: data.method,
                        emotion: data.emotion
                    });
                }
            } catch (error) {
                addMessage('خطأ في الاتصال: ' + error.message, 'nano');
            }
            
            updateStatus();
        }
        
        function addMessage(text, sender, debug = null) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            let content = text;
            if (debug) {
                content += `<div class="debug-info">
                    الثقة: ${(debug.confidence * 100).toFixed(1)}% | 
                    المزاج: ${debug.mood} | 
                    الطريقة: ${debug.method}
                </div>`;
            }
            
            messageDiv.innerHTML = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        async function updateStatus() {
            try {
                const response = await fetch('/status');
                const status = await response.json();
                
                document.getElementById('mood').textContent = status.personality.current_mood;
                document.getElementById('conversations').textContent = status.performance.total_interactions;
                document.getElementById('status').textContent = 'متصل';
            } catch (error) {
                document.getElementById('status').textContent = 'خطأ في الاتصال';
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // تحديث الحالة كل 30 ثانية
        setInterval(updateStatus, 30000);
        
        // تحديث الحالة عند التحميل
        updateStatus();
    </script>
</body>
</html>'''
        
        with open(templates_dir / "nano_interface.html", "w", encoding="utf-8") as f:
            f.write(html_template)

    # إنشاء التطبيق
    app = NanoApp()
    
    # تحديد وضع التشغيل
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "console":
            app.run_console_mode()
        elif mode == "web":
            host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
            app.run_web_mode(host, port)
        else:
            print("وضع غير معروف. استخدم: console أو web")
    else:
        # وضع تفاعلي لاختيار النوع
        print("🤖 أهلاً بك في نانو!")
        print("اختر وضع التشغيل:")
        print("1. وضع سطر الأوامر (console)")
        print("2. وضع الويب (web)")
        
        choice = input("اختيارك (1-2): ").strip()
        
        if choice == "1":
            app.run_console_mode()
        elif choice == "2":
            app.run_web_mode()
        else:
            print("اختيار غير صحيح!")

if __name__ == "__main__":
    main()