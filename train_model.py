"""
train_model.py
Run this ONCE locally to generate model.pkl and vectorizer.pkl
"""

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ── Sample training data (spam + ham) ──
# In a real project, replace with a dataset like SMS Spam Collection
EMAILS = [
    # SPAM
    ("Congratulations! You've won a $1,000 gift card. Click here to claim now!", 1),
    ("FREE entry in 2 a weekly comp to win FA Cup final tickets!", 1),
    ("URGENT: Your account has been compromised. Verify immediately at this link.", 1),
    ("You have been selected for a cash prize of $5000. Reply YES to claim.", 1),
    ("Get rich quick! Work from home and earn $500 daily. No experience needed.", 1),
    ("LIMITED OFFER: Buy 1 get 2 FREE on all products. Order now!", 1),
    ("Your loan has been approved! Click to receive your $10,000 instantly.", 1),
    ("Win an iPhone 15! You are our lucky winner. Tap to collect your prize.", 1),
    ("ATTENTION: Suspicious login detected. Verify your account NOW.", 1),
    ("Earn money fast! Join thousands making $1000/day online.", 1),
    ("FREE SMS: Call our FREE 0800 number now! Prize guaranteed.", 1),
    ("You have a secret admirer! Find out who likes you. Click here.", 1),
    ("Final notice: Your subscription is expiring. Renew immediately.", 1),
    ("Hot singles in your area! Click to meet them tonight.", 1),
    ("Your PayPal account is limited. Verify your identity to restore access.", 1),
    ("Claim your FREE vacation package worth $2,500 now!", 1),
    ("WINNER! As a valued network customer you have been selected.", 1),
    ("SIX chances to win CASH! From 100 to 20,000 pounds. Text to claim.", 1),
    ("Buy cheap meds online! No prescription needed. 80% off today!", 1),
    ("Your credit score can be boosted instantly. Click to find out how.", 1),
    # HAM
    ("Hey, are we still on for dinner tonight at 7?", 0),
    ("Please find the meeting agenda attached for tomorrow.", 0),
    ("Can you review the project report before Friday?", 0),
    ("I'll be 10 minutes late to the call, sorry!", 0),
    ("Thanks for sending over the documents. I'll review them soon.", 0),
    ("Happy birthday! Hope you have a wonderful day.", 0),
    ("The package you ordered has been shipped and will arrive Thursday.", 0),
    ("Let's catch up sometime this week. Are you free Wednesday?", 0),
    ("Reminder: your dentist appointment is tomorrow at 3pm.", 0),
    ("I just finished the assignment. Can you check my work?", 0),
    ("Our team meeting is rescheduled to 2pm on Monday.", 0),
    ("Thank you for your application. We will be in touch shortly.", 0),
    ("Can you pick up some milk on your way home?", 0),
    ("The report is ready. Please approve at your earliest convenience.", 0),
    ("I enjoyed our conversation. Looking forward to working together.", 0),
    ("Your flight booking is confirmed. Check your itinerary below.", 0),
    ("Mom called and said dinner is at 6pm this Sunday.", 0),
    ("Please submit your timesheet by end of day Friday.", 0),
    ("Good morning! Here is your daily news summary.", 0),
    ("The library books you borrowed are due back next week.", 0),
]

texts  = [e[0] for e in EMAILS]
labels = [e[1] for e in EMAILS]

# ── Build Pipeline: TF-IDF → Naive Bayes ──
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )),
    ("clf", MultinomialNB(alpha=0.1)),
])

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)
preds = pipeline.predict(X_test)

print("✅ Model trained successfully!")
print(f"   Accuracy: {accuracy_score(y_test, preds)*100:.1f}%")
print(classification_report(y_test, preds, target_names=["Ham", "Spam"]))

# ── Save model ──
with open("model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("💾 model.pkl saved!")
