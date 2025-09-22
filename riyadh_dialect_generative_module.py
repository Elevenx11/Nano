# riyadh_dialect_generative_module.py (v5.0 - JSON Reader)
import random
import json
import os

class RiyadhDialectGenerative:
    """
    جزيء لغوي توليدي للهجة الرياض.
    النسخة: 5.0 (قارئ JSON)

    التحسينات:
    - تم فصل البيانات بشكل كامل، الآن يقرأ الجمل من ملف `corpus.json`.
    - الكود أصبح أكثر نظافة واحترافية.
    """
    def __init__(self, model_path="riyadh_model.json"):
        self.model_path = model_path
        self.model = {}
        self._start_token = "_START_"
        self._end_token = "_END_"

    def train(self, corpus_path="corpus.json", force_retrain=False):
        """
        تدريب النموذج على ملف البيانات JSON.
        """
        print("INFO: بدء عملية التدريب...")

        if not force_retrain and os.path.exists(self.model_path):
            print(f"INFO: تم العثور على نموذج مدرب. جاري التحميل من '{self.model_path}'...")
            self.load_model()
            return

        print(f"INFO: جاري قراءة البيانات من '{corpus_path}'...")
        try:
            with open(corpus_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lines = data.get("sentences", [])
        except FileNotFoundError:
            print(f"ERROR: ملف البيانات '{corpus_path}' غير موجود. لا يمكن التدريب.")
            return
        except json.JSONDecodeError:
            print(f"ERROR: خطأ في قراءة ملف '{corpus_path}'. تأكد من أنه بصيغة JSON صحيحة.")
            return

        if not lines:
            print("WARNING: ملف البيانات فارغ أو لا يحتوي على مفتاح 'sentences'.")
            return

        print(f"INFO: تم العثور على {len(lines)} جملة. جاري بناء النموذج الإحصائي...")
        for line in lines:
            words = [self._start_token] + line.strip().split() + [self._end_token]
            for i in range(len(words) - 1):
                current_word = words[i]
                next_word = words[i+1]

                if current_word not in self.model:
                    self.model[current_word] = {}

                if next_word not in self.model[current_word]:
                    self.model[current_word][next_word] = 0

                self.model[current_word][next_word] += 1

        print("INFO: اكتمل بناء النموذج. جاري حفظه...")
        self.save_model()

    def save_model(self):
        with open(self.model_path, 'w', encoding='utf-8') as f:
            json.dump(self.model, f, ensure_ascii=False, indent=2)
        print(f"INFO: تم حفظ النموذج في '{self.model_path}'.")

    def load_model(self):
        with open(self.model_path, 'r', encoding='utf-8') as f:
            self.model = json.load(f)
        print(f"INFO: تم تحميل النموذج بنجاح.")

    def _choose_next_word(self, current_word):
        if current_word not in self.model or not self.model[current_word]:
            return self._end_token

        next_words_pool = self.model[current_word]
        words = list(next_words_pool.keys())
        weights = list(next_words_pool.values())

        return random.choices(words, weights=weights, k=1)[0]

    def generate_sentence(self, start_word=None, max_length=15):
        if not self.model:
            return "لم يتم تدريب النموذج بعد. يرجى تشغيل دالة train() أولاً."

        if start_word and start_word in self.model:
            current_word = start_word
        else:
            current_word = self._start_token

        sentence = []
        if current_word != self._start_token:
            sentence.append(current_word)

        # منع الحلقات المفرغة البسيطة
        last_word = ""
        while len(sentence) < max_length:
            next_word = self._choose_next_word(current_word)
            if next_word == self._end_token or next_word == last_word:
                break

            sentence.append(next_word)
            last_word = current_word
            current_word = next_word

        return " ".join(sentence)

