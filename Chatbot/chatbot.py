import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt', quiet=True)

class AdmissionChatBot:
    def __init__(self):
        self.ps = PorterStemmer()
        self.load_knowledge_base("knowledge_base.json")
        self.context = {}

    def load_knowledge_base(self, filepath):
        with open(filepath, encoding='utf-8') as f:
            self.knowledge = json.load(f)

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return [self.ps.stem(t) for t in tokens if t.isalnum()]

    def match_intents(self, query):
        tokens = self.preprocess(query)
        detected_intents = []
        intent_keywords = {
            "greeting": ["hi", "hello", "hey", "namaste"],
            "farewell": ["bye", "goodbye", "see you", "later"],
            "smalltalk": ["you", "your", "name", "doing", "bot"],
            "deadlines": ["deadlin", "last", "date", "close", "due"],
            "eligibility": ["eligib", "qualif", "criteria", "require", "admiss", "apply", "percent", "graduat", "bachelor", "score"],
            "fees": ["fee", "tuit", "cost", "price", "charg", "amount", "₹", "rs"],
            "contact": ["contact", "email", "phone", "reach", "helpdesk"],
            "programs": ["program", "course", "mca", "special", "subject", "field"],
            "installments": ["install", "payment", "emi", "split", "part", "plan"],
            "hostel": ["hostel", "stay", "room", "accomm", "warden", "residenc"],
            "placement": ["placement", "job", "assist", "career", "recruit", "internship"],
            "canteen": ["canteen", "food", "mess", "dining", "cafeteria"],
            "library": ["library", "book", "study", "read", "reference"],
            "scholarship": ["scholarship", "aid", "merit", "waiver"],
            "wifi": ["wifi", "internet", "network", "connect", "access"]
        }
        for intent, keywords in intent_keywords.items():
            if any(word in tokens for word in keywords):
                detected_intents.append(intent)
        return detected_intents or ["unknown"]

    def generate_response(self, intents):
        responses = []

        for intent in intents:
            if intent == "greeting":
                return "Hello! How can I assist you with MCA admissions today?"
            elif intent == "farewell":
                return "Goodbye! Feel free to reach out again anytime."
            elif intent == "smalltalk":
                return "I'm just a helpful bot here to assist with MCA admissions. Ask me about deadlines, fees, eligibility, etc."
            elif intent == "unknown":
                return (
                    "I'm not sure I understand. You can ask about MCA fees, eligibility, deadlines, hostel, placements, canteen, and more."
                )
            elif intent in self.knowledge:
                responses.append(self.knowledge[intent])

        return "\n\n".join(responses)

    def handle_query(self, query):
        intents = self.match_intents(query)
        print(f"Detected intents: {intents}")
        response = self.generate_response(intents)
        self.log_conversation(query, response, intents)
        return response

    def log_conversation(self, query, response, intents):
        with open("conversation_log.txt", "a", encoding='utf-8') as f:
            f.write(f"User: {query}\nIntent(s): {', '.join(intents)}\nBot: {response}\n\n")

knowledge_base = {
    "deadlines": "MCA admissions close on September 30, 2025. Late applications are accepted until October 15 with a late fee.",
    "eligibility": "Eligibility: Bachelor's degree with at least 50% marks and a valid entrance exam score.",
    "fees": "The total tuition fee is ₹1,20,000 per year. Scholarships are offered to the top 10% scorers.",
    "contact": "Email: mcaadmissions@xyz.ac.in | Phone: +91-3134545071",
    "programs": "We offer MCA programs with specializations in Artificial Intelligence, Cybersecurity, and Data Science.",
    "installments": "You will be given 2 installments to pay the yearly fee.",
    "hostel": "Our hostel facilities include spacious rooms, 24/7 security, Wi-Fi, and both veg/non-veg mess services. Rooms are available on a first-come basis.",
    "placement": "We offer 100% placement assistance with top companies visiting for recruitment. Career guidance and mock interviews are provided.",
    "canteen": "The campus canteen serves a variety of hygienic and affordable meals, snacks, and beverages throughout the day.",
    "library": "Our central library has over 25,000 books, online journal access, and quiet study spaces available for students.",
    "scholarship": "Merit-based scholarships and need-based financial aid are available. You can apply during the admission process.",
    "wifi": "High-speed campus-wide Wi-Fi is available to all registered students and staff."
}

if __name__ == "__main__":
    with open("knowledge_base.json", "w", encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=4)

    bot = AdmissionChatBot()
    print("Admission Bot: Hi! Ask me about MCA admissions (type 'quit' to exit)\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ['quit', 'exit']:
            print("Bot: Thank you! Feel free to reach out for more help.")
            break
        print("Bot:", bot.handle_query(user_input))
