# اختبار سريع لنانو الجديد
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "core"))

from core.nano_brain import NanoBrain

def quick_test():
    nano = NanoBrain("data")
    
    test_cases = [
        "سوي لي قهوة",      # يجب أن يرفض
        "أنا أذكى واحد",      # يجب أن يسخر
        "أنا زعلان",         # يجب أن يتعاطف  
        "ممكن تساعدني؟",      # يجب أن يساعد
        "إنت غبي",           # يجب أن يدافع
        "كل زق"              # يجب أن يرد بقوة
    ]
    
    print("🧪 اختبار سريع لشخصية نانو")
    print("=" * 40)
    
    for i, test in enumerate(test_cases, 1):
        response = nano.generate_response(test)
        print(f"\n{i}. 👤: {test}")
        print(f"   🤖: {response.text}")
        print(f"   📊: {response.personality_mood} | {response.method_used}")

if __name__ == "__main__":
    quick_test()