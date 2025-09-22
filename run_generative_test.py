# run_generative_test.py
from riyadh_dialect_generative_module import RiyadhDialectGenerative
import time

# 1. إنشاء نسخة من الجزيء
nano_generative_dialect = RiyadhDialectGenerative()

# 2. تدريب النموذج (سيتم مرة واحدة فقط، ثم سيقوم بتحميل النموذج تلقائيًا)
start_time = time.time()
nano_generative_dialect.train()
end_time = time.time()
print(f"INFO: استغرقت عملية التدريب/التحميل {end_time - start_time:.2f} ثانية.")

print("\n--- الجزيء التوليدي للهجة الرياض جاهز ---")
print("اكتب كلمة لتبدأ بها الجملة، أو اتركها فارغة لتوليد جملة عشوائية.")
print("اكتب 'خروج' لإنهاء الاختبار.")
print("-" * 20)

while True:
    user_input = input("أدخل كلمة بداية (أو اضغط Enter) > ")
    if user_input.lower() == 'خروج':
        break

    start_word = user_input.strip() if user_input.strip() else None

    # 3. استدعاء الجزيء لتوليد جملة
    print("نانو يفكر...")
    response = nano_generative_dialect.generate_sentence(start_word=start_word)

    print(f"نانو (توليدي): {response}\n")
