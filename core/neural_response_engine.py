# neural_response_engine.py - محرك التعلم الذاتي للردود
import json
import random
import re
import math
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, Counter, deque
from dataclasses import dataclass
from datetime import datetime
import pickle
import os

@dataclass
class ResponsePattern:
    """نمط الرد"""
    input_pattern: List[str]
    response_template: str
    success_rate: float
    context_type: str
    emotion_trigger: str
    usage_count: int
    last_used: datetime

@dataclass
class ConversationContext:
    """سياق المحادثة"""
    previous_messages: List[str]
    current_emotion: str
    user_personality_type: str
    relationship_level: float  # مستوى العلاقة من 0 إلى 1
    conversation_topic: str

class NeuralResponseEngine:
    """محرك التعلم الذاتي للردود - يتعلم من المحادثات الطبيعية"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        
        # قاعدة أنماط الردود المتعلمة
        self.response_patterns = []
        self.conversation_contexts = deque(maxlen=200)
        self.successful_interactions = deque(maxlen=500)
        
        # نماذج التعلم
        self.word_associations = defaultdict(lambda: defaultdict(float))
        self.phrase_templates = defaultdict(list)
        self.context_response_map = defaultdict(lambda: defaultdict(float))
        
        # مولد الردود التلقائي
        self.response_generators = {
            "markov_chain": self.generate_markov_response,
            "associative": self.generate_associative_response,
            "contextual": self.generate_contextual_response
        }
        
        # إحصائيات التعلم
        self.learning_metrics = {
            "total_patterns": 0,
            "success_rate": 0.0,
            "diversity_score": 0.0,
            "last_training": None
        }
        
        # تهيئة النظام
        self.initialize_base_patterns()
        self.load_learned_data()

    def initialize_base_patterns(self):
        """تهيئة أنماط الردود الأساسية للبداية"""
        
        # أنماط أساسية للتعلم منها
        base_patterns = [
            {
                "input": ["السلام عليكم", "مرحبا", "أهلا", "هاي"],
                "response_type": "greeting",
                "templates": ["وعليكم السلام حبيبي", "أهلاً وسهلاً", "مرحبا بك يا غالي"],
                "emotion": "ود"
            },
            {
                "input": ["كيف حالك", "شلونك", "إيش أخبارك"],
                "response_type": "status_check", 
                "templates": ["الحمدلله تمام", "بخير والحمدلله", "كله زين"],
                "emotion": "طيب"
            },
            {
                "input": ["شكراً", "يعطيك العافية", "تسلم"],
                "response_type": "gratitude_response",
                "templates": ["العفو حبيبي", "الله يعافيك", "ما سويت شي"],
                "emotion": "تقدير"
            }
        ]
        
        # تحويل الأنماط الأساسية لنماذج تعلم
        for pattern in base_patterns:
            for template in pattern["templates"]:
                self.add_successful_pattern(
                    input_sample=" ".join(pattern["input"][:2]),
                    response=template,
                    context_type=pattern["response_type"],
                    emotion=pattern["emotion"]
                )

    def add_successful_pattern(self, input_sample: str, response: str, 
                             context_type: str, emotion: str, success_score: float = 1.0):
        """إضافة نمط رد ناجح للتعلم"""
        
        # استخراج الكلمات المفتاحية
        input_words = self.extract_keywords(input_sample)
        response_words = response.split()
        
        # إنشاء نمط الرد
        pattern = ResponsePattern(
            input_pattern=input_words,
            response_template=response,
            success_rate=success_score,
            context_type=context_type,
            emotion_trigger=emotion,
            usage_count=1,
            last_used=datetime.now()
        )
        
        self.response_patterns.append(pattern)
        
        # تحديث خرائط التعلم
        self.update_word_associations(input_words, response_words, success_score)
        self.update_context_mappings(context_type, emotion, response, success_score)
        
        # تسجيل التفاعل الناجح
        self.successful_interactions.append({
            'input': input_sample,
            'response': response, 
            'context': context_type,
            'emotion': emotion,
            'success_score': success_score,
            'timestamp': datetime.now()
        })

    def extract_keywords(self, text: str) -> List[str]:
        """استخراج الكلمات المفتاحية المهمة"""
        
        # كلمات غير مهمة لتجاهلها
        stop_words = {
            "في", "من", "إلى", "على", "عن", "مع", "هذا", "هذه", "ذلك", "تلك",
            "التي", "التي", "اللي", "الي", "وش", "إيش", "ليش", "كيف"
        }
        
        words = re.findall(r'\w+', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords[:5]  # أهم 5 كلمات مفتاحية

    def update_word_associations(self, input_words: List[str], response_words: List[str], 
                                success_score: float):
        """تحديث ترابطات الكلمات"""
        
        for input_word in input_words:
            for response_word in response_words:
                # تقوية الترابط بناءً على النجاح
                self.word_associations[input_word][response_word] += 0.1 * success_score
                
                # تطبيع القيم لتجنب النمو المفرط
                if self.word_associations[input_word][response_word] > 1.0:
                    self.word_associations[input_word][response_word] = 1.0

    def update_context_mappings(self, context_type: str, emotion: str, 
                               response: str, success_score: float):
        """تحديث خرائط السياق والمشاعر"""
        
        context_key = f"{context_type}_{emotion}"
        
        # تحديث قوة الرد في هذا السياق
        self.context_response_map[context_key][response] += 0.1 * success_score

    def generate_smart_response(self, user_input: str, emotion: str = "محايد", 
                               context: ConversationContext = None) -> Tuple[str, float, str]:
        """توليد رد ذكي بناءً على التعلم"""
        
        # استخراج خصائص المدخل
        input_keywords = self.extract_keywords(user_input)
        
        # البحث عن أنماط مشابهة
        similar_patterns = self.find_similar_patterns(input_keywords, emotion)
        
        # توليد ردود متعددة بطرق مختلفة
        candidate_responses = []
        
        # 1. من الأنماط المتعلمة
        if similar_patterns:
            pattern_response = self.generate_from_patterns(similar_patterns, context)
            candidate_responses.append((pattern_response, "pattern_based", 0.8))
        
        # 2. من سلاسل ماركوف
        markov_response = self.generate_markov_response(input_keywords, emotion)
        candidate_responses.append((markov_response, "markov", 0.6))
        
        # 3. من الترابطات
        associative_response = self.generate_associative_response(input_keywords)
        candidate_responses.append((associative_response, "associative", 0.5))
        
        # 4. من القوالب السياقية
        if context:
            contextual_response = self.generate_contextual_response(input_keywords, context)
            candidate_responses.append((contextual_response, "contextual", 0.7))
        
        # اختيار أفضل رد
        best_response, method, confidence = self.select_best_response(candidate_responses, user_input)
        
        return best_response, confidence, method

    def find_similar_patterns(self, input_keywords: List[str], emotion: str) -> List[ResponsePattern]:
        """العثور على أنماط مشابهة"""
        
        similar_patterns = []
        
        for pattern in self.response_patterns:
            # حساب التشابه
            similarity = self.calculate_pattern_similarity(input_keywords, pattern.input_pattern)
            
            # تعديل حسب المشاعر
            if pattern.emotion_trigger == emotion:
                similarity += 0.2
            
            # إضافة الأنماط المشابهة
            if similarity > 0.3:  # حد أدنى للتشابه
                similar_patterns.append((pattern, similarity))
        
        # ترتيب حسب التشابه ومعدل النجاح
        similar_patterns.sort(key=lambda x: x[1] * x[0].success_rate, reverse=True)
        
        return [pattern for pattern, score in similar_patterns[:5]]

    def calculate_pattern_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """حساب التشابه بين مجموعتين من الكلمات المفتاحية"""
        
        if not keywords1 or not keywords2:
            return 0.0
        
        set1 = set(keywords1)
        set2 = set(keywords2)
        
        # تشابه جاكارد
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0

    def generate_from_patterns(self, patterns: List[ResponsePattern], 
                              context: ConversationContext = None) -> str:
        """توليد رد من الأنماط المتعلمة"""
        
        if not patterns:
            return self.generate_fallback_response()
        
        # اختيار نمط بناءً على النجاح والحداثة
        weights = []
        for pattern in patterns:
            # وزن يعتمد على معدل النجاح ومدى الحداثة
            recency_factor = 1.0 - ((datetime.now() - pattern.last_used).days / 30.0)
            recency_factor = max(0.1, recency_factor)
            
            weight = pattern.success_rate * recency_factor
            weights.append(weight)
        
        # اختيار عشوائي مرجح
        selected_pattern = random.choices(patterns, weights=weights)[0]
        
        # تحديث احصائيات الاستخدام
        selected_pattern.usage_count += 1
        selected_pattern.last_used = datetime.now()
        
        # إضافة تنويع للرد
        return self.add_variation_to_response(selected_pattern.response_template)

    def generate_markov_response(self, keywords: List[str], emotion: str) -> str:
        """توليد رد باستخدام سلاسل ماركوف"""
        
        # البحث عن جمل تحتوي على كلمات مشابهة
        relevant_responses = []
        
        for interaction in self.successful_interactions:
            interaction_keywords = self.extract_keywords(interaction['input'])
            
            # فحص التشابه
            if any(kw in interaction_keywords for kw in keywords):
                relevant_responses.append(interaction['response'])
        
        if not relevant_responses:
            return self.generate_fallback_response()
        
        # بناء نموذج ماركوف بسيط
        words = []
        for response in relevant_responses:
            words.extend(response.split())
        
        if len(words) < 3:
            return random.choice(relevant_responses)
        
        # توليد رد جديد
        generated_words = []
        current_word = random.choice(words)
        generated_words.append(current_word)
        
        for _ in range(random.randint(3, 8)):
            # العثور على الكلمات التي تأتي بعد الكلمة الحالية
            next_words = []
            for i, word in enumerate(words[:-1]):
                if word == current_word:
                    next_words.append(words[i + 1])
            
            if next_words:
                current_word = random.choice(next_words)
                generated_words.append(current_word)
            else:
                break
        
        return " ".join(generated_words)

    def generate_associative_response(self, keywords: List[str]) -> str:
        """توليد رد بناءً على الترابطات"""
        
        response_words = []
        
        for keyword in keywords:
            if keyword in self.word_associations:
                # الحصول على أقوى الترابطات
                associations = self.word_associations[keyword]
                if associations:
                    # اختيار أفضل 3 كلمات مرتبطة
                    top_words = sorted(associations.items(), key=lambda x: x[1], reverse=True)[:3]
                    response_words.extend([word for word, score in top_words])
        
        if not response_words:
            return self.generate_fallback_response()
        
        # بناء رد من الكلمات المرتبطة
        unique_words = list(set(response_words))[:6]
        
        # إضافة كلمات ربط بسيطة
        connectors = ["و", "لكن", "كذلك", "أيضاً", ""]
        
        # بناء جملة بسيطة
        if len(unique_words) >= 2:
            connector = random.choice(connectors)
            if connector:
                return f"{unique_words[0]} {connector} {' '.join(unique_words[1:])}"
            else:
                return " ".join(unique_words)
        else:
            return unique_words[0] if unique_words else self.generate_fallback_response()

    def generate_contextual_response(self, keywords: List[str], context: ConversationContext) -> str:
        """توليد رد سياقي متطور"""
        
        context_key = f"{context.conversation_topic}_{context.current_emotion}"
        
        if context_key in self.context_response_map:
            responses = self.context_response_map[context_key]
            if responses:
                # اختيار رد بناءً على القوة في هذا السياق
                best_response = max(responses.items(), key=lambda x: x[1])[0]
                return self.personalize_response(best_response, context)
        
        # إذا لم نجد سياقاً مناسباً، نولد رد عام
        return self.generate_general_contextual_response(context)

    def personalize_response(self, base_response: str, context: ConversationContext) -> str:
        """تخصيص الرد حسب الشخصية والعلاقة"""
        
        # تعديلات حسب مستوى العلاقة
        if context.relationship_level > 0.8:  # علاقة قوية
            # إضافة كلمات حميمة
            intimate_words = ["حبيبي", "يا غالي", "عزيزي", "يا قلبي"]
            if not any(word in base_response for word in intimate_words):
                base_response += f" {random.choice(intimate_words)}"
        
        elif context.relationship_level < 0.3:  # علاقة رسمية
            # جعل الرد أكثر رسمية
            formal_endings = ["تحياتي", "مع احترامي", "بالتوفيق"]
            base_response += f" {random.choice(formal_endings)}"
        
        # تعديلات حسب نوع الشخصية
        if context.user_personality_type == "friendly":
            base_response = self.add_friendly_tone(base_response)
        elif context.user_personality_type == "serious":
            base_response = self.add_serious_tone(base_response)
        
        return base_response

    def add_friendly_tone(self, response: str) -> str:
        """إضافة نبرة ودودة"""
        friendly_additions = ["😊", "هههه", "والله", "ما شاء الله"]
        return response + f" {random.choice(friendly_additions)}"

    def add_serious_tone(self, response: str) -> str:
        """إضافة نبرة جدية"""
        # إزالة الرموز التعبيرية والكلمات العامية
        response = re.sub(r'[😊😂🤣😍]', '', response)
        response = response.replace("هههه", "").replace("والله", "")
        return response.strip()

    def generate_general_contextual_response(self, context: ConversationContext) -> str:
        """توليد رد سياقي عام"""
        
        topic_responses = {
            "تحية": ["مرحباً بك", "أهلاً وسهلاً", "السلام عليكم"],
            "سؤال": ["سؤال مثير للاهتمام", "دعني أفكر في هذا", "هذا موضوع مهم"],
            "مشكلة": ["أفهم مشكلتك", "هذا محبط فعلاً", "لا تقلق، سنجد حلاً"],
            "فرح": ["هذا رائع!", "مبروك عليك", "أشاركك الفرحة"],
            "عام": ["فهمت", "نعم", "طبعاً", "بالتأكيد"]
        }
        
        topic = context.conversation_topic if context.conversation_topic in topic_responses else "عام"
        return random.choice(topic_responses[topic])

    def add_variation_to_response(self, base_response: str) -> str:
        """إضافة تنويع للرد لتجنب التكرار"""
        
        # إضافات بسيطة للتنويع
        variations = {
            "prefixes": ["", "يعني", "الصراحة", "طبعاً", "أكيد"],
            "suffixes": ["", "ما رأيك؟", "صحيح؟", "تمام؟", "واضح؟"],
            "intensifiers": ["جداً", "كثير", "فعلاً", "حقاً", ""]
        }
        
        # تطبيق تنويع عشوائي بسيط
        if random.random() < 0.3:  # 30% احتمال إضافة بداية
            prefix = random.choice(variations["prefixes"])
            if prefix:
                base_response = f"{prefix} {base_response}"
        
        if random.random() < 0.2:  # 20% احتمال إضافة نهاية
            suffix = random.choice(variations["suffixes"])
            if suffix:
                base_response = f"{base_response} {suffix}"
        
        return base_response

    def select_best_response(self, candidates: List[Tuple[str, str, float]], 
                           user_input: str) -> Tuple[str, str, float]:
        """اختيار أفضل رد من المرشحين"""
        
        if not candidates:
            return self.generate_fallback_response(), "fallback", 0.3
        
        # تصفية الردود الفارغة أو غير المناسبة
        valid_candidates = []
        for response, method, confidence in candidates:
            if response and len(response.strip()) > 0 and response != user_input:
                quality_score = self.evaluate_response_quality(response, user_input)
                adjusted_confidence = confidence * quality_score
                valid_candidates.append((response, method, adjusted_confidence))
        
        if not valid_candidates:
            return self.generate_fallback_response(), "fallback", 0.3
        
        # اختيار أفضل رد
        best_candidate = max(valid_candidates, key=lambda x: x[2])
        return best_candidate

    def evaluate_response_quality(self, response: str, user_input: str) -> float:
        """تقييم جودة الرد"""
        
        quality_score = 1.0
        
        # التحقق من الطول المناسب
        if len(response) < 3:
            quality_score -= 0.5
        elif len(response) > 200:
            quality_score -= 0.2
        
        # التحقق من عدم التكرار المباشر
        if response.lower() == user_input.lower():
            quality_score -= 0.8
        
        # التحقق من وجود كلمات مفيدة
        meaningful_words = len([w for w in response.split() if len(w) > 2])
        if meaningful_words < 2:
            quality_score -= 0.3
        
        # تقييم التنوع اللغوي
        unique_words = len(set(response.lower().split()))
        total_words = len(response.split())
        diversity = unique_words / total_words if total_words > 0 else 0
        quality_score += diversity * 0.2
        
        return max(0.1, quality_score)

    def generate_fallback_response(self) -> str:
        """توليد رد احتياطي عند فشل كل الطرق الأخرى"""
        
        fallbacks = [
            "فهمت كلامك",
            "أها، واضح",
            "طيب، تمام",
            "إيه نعم",
            "صحيح",
            "أكيد",
            "ما رأيك في موضوع آخر؟",
            "حلو كلامك",
            "زين"
        ]
        
        return random.choice(fallbacks)

    def learn_from_feedback(self, user_input: str, bot_response: str, 
                           feedback_type: str, success_score: float):
        """التعلم من التغذية الراجعة"""
        
        if success_score > 0.6:  # رد ناجح
            self.add_successful_pattern(
                input_sample=user_input,
                response=bot_response,
                context_type=feedback_type,
                emotion="محايد",  # سيتم تحسين هذا لاحقاً
                success_score=success_score
            )
        else:  # رد غير ناجح - تقليل الوزن
            self.reduce_pattern_weight(user_input, bot_response, success_score)

    def reduce_pattern_weight(self, user_input: str, bot_response: str, penalty_score: float):
        """تقليل وزن الأنماط غير الناجحة"""
        
        input_keywords = self.extract_keywords(user_input)
        response_words = bot_response.split()
        
        # تقليل الترابطات
        for input_word in input_keywords:
            for response_word in response_words:
                if input_word in self.word_associations and response_word in self.word_associations[input_word]:
                    self.word_associations[input_word][response_word] *= (1 - penalty_score * 0.1)
                    
                    # حذف الترابطات الضعيفة جداً
                    if self.word_associations[input_word][response_word] < 0.01:
                        del self.word_associations[input_word][response_word]

    def save_learned_data(self):
        """حفظ البيانات المتعلمة"""
        
        # إنشاء مجلد البيانات إذا لم يكن موجوداً
        os.makedirs(self.data_path, exist_ok=True)
        
        # حفظ بيانات مختلفة في ملفات منفصلة
        data_files = {
            'word_associations.pkl': dict(self.word_associations),
            'context_response_map.pkl': dict(self.context_response_map),
            'response_patterns.pkl': [
                {
                    'input_pattern': p.input_pattern,
                    'response_template': p.response_template,
                    'success_rate': p.success_rate,
                    'context_type': p.context_type,
                    'emotion_trigger': p.emotion_trigger,
                    'usage_count': p.usage_count,
                    'last_used': p.last_used
                } for p in self.response_patterns
            ],
            'learning_metrics.json': self.learning_metrics,
            'successful_interactions.pkl': list(self.successful_interactions)
        }
        
        for filename, data in data_files.items():
            filepath = os.path.join(self.data_path, filename)
            
            if filename.endswith('.json'):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            else:
                with open(filepath, 'wb') as f:
                    pickle.dump(data, f)

    def load_learned_data(self):
        """تحميل البيانات المتعلمة"""
        
        try:
            # تحميل ترابطات الكلمات
            word_assoc_path = os.path.join(self.data_path, 'word_associations.pkl')
            if os.path.exists(word_assoc_path):
                with open(word_assoc_path, 'rb') as f:
                    data = pickle.load(f)
                    self.word_associations = defaultdict(lambda: defaultdict(float), data)
            
            # تحميل خرائط السياق
            context_path = os.path.join(self.data_path, 'context_response_map.pkl')
            if os.path.exists(context_path):
                with open(context_path, 'rb') as f:
                    data = pickle.load(f)
                    self.context_response_map = defaultdict(lambda: defaultdict(float), data)
            
            # تحميل أنماط الردود
            patterns_path = os.path.join(self.data_path, 'response_patterns.pkl')
            if os.path.exists(patterns_path):
                with open(patterns_path, 'rb') as f:
                    patterns_data = pickle.load(f)
                    self.response_patterns = [
                        ResponsePattern(**pattern_data) for pattern_data in patterns_data
                    ]
            
            # تحميل المقاييس
            metrics_path = os.path.join(self.data_path, 'learning_metrics.json')
            if os.path.exists(metrics_path):
                with open(metrics_path, 'r', encoding='utf-8') as f:
                    self.learning_metrics = json.load(f)
            
            # تحميل التفاعلات الناجحة
            interactions_path = os.path.join(self.data_path, 'successful_interactions.pkl')
            if os.path.exists(interactions_path):
                with open(interactions_path, 'rb') as f:
                    interactions_data = pickle.load(f)
                    self.successful_interactions = deque(interactions_data[-500:], maxlen=500)
                    
        except Exception as e:
            print(f"خطأ في تحميل البيانات المتعلمة: {e}")
            # المتابعة بالبيانات الافتراضية

    def get_learning_statistics(self) -> Dict:
        """الحصول على إحصائيات التعلم"""
        
        stats = {
            "total_patterns": len(self.response_patterns),
            "total_interactions": len(self.successful_interactions),
            "unique_word_associations": len(self.word_associations),
            "context_mappings": len(self.context_response_map),
            "average_success_rate": 0.0,
            "most_successful_patterns": [],
            "learning_progress": self.calculate_learning_progress()
        }
        
        # حساب متوسط معدل النجاح
        if self.response_patterns:
            total_success = sum(p.success_rate for p in self.response_patterns)
            stats["average_success_rate"] = total_success / len(self.response_patterns)
        
        # أفضل الأنماط
        top_patterns = sorted(self.response_patterns, 
                            key=lambda p: p.success_rate * p.usage_count, 
                            reverse=True)[:5]
        
        stats["most_successful_patterns"] = [
            {
                "pattern": p.input_pattern[:3],  # أول 3 كلمات
                "response": p.response_template[:50],  # أول 50 حرف
                "success_rate": p.success_rate,
                "usage_count": p.usage_count
            } for p in top_patterns
        ]
        
        return stats

    def calculate_learning_progress(self) -> float:
        """حساب مدى تقدم التعلم"""
        
        if len(self.successful_interactions) < 10:
            return 0.0
        
        # مقارنة أداء أول وآخر مجموعة من التفاعلات
        interactions_list = list(self.successful_interactions)
        
        first_batch = interactions_list[:10]
        last_batch = interactions_list[-10:]
        
        first_avg = sum(i['success_score'] for i in first_batch) / 10
        last_avg = sum(i['success_score'] for i in last_batch) / 10
        
        return max(0.0, last_avg - first_avg)  # التحسن في الأداء