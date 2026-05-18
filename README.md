# 🛡️ Spam Email Detector
**Machine Learning + CI/CD Deployment via GitHub + Render**

> Paste any email text and instantly find out if it's spam using a Naive Bayes + TF-IDF model.

🔗 **Live Demo:** `https://spam-email-detector.onrender.com` *(after deployment)*

---

## 🗂️ Project Structure

```
spam-detector/
├── app.py              ← Streamlit UI (main app)
├── train_model.py      ← Script to train & save model
├── model.pkl           ← Trained ML model (auto-generated)
├── requirements.txt    ← Python dependencies
├── render.yaml         ← Render deployment config
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

```
Email Text → TF-IDF Vectorizer → Naive Bayes → Spam / Ham
```

1. User pastes email text into the UI
2. Text is cleaned (lowercase, remove URLs, special chars)
3. TF-IDF converts text to numerical features
4. Naive Bayes model predicts Spam (1) or Ham (0)
5. Confidence score shown with visual bar

---

## 🚀 DEPLOYMENT GUIDE — Step by Step

### STEP 1 — Train the model locally

```bash
# Install dependencies
pip install scikit-learn streamlit numpy

# Train and save model.pkl
python train_model.py
```

You should see:
```
✅ Model trained successfully!
   Accuracy: 75.0%
💾 model.pkl saved!
```

---

### STEP 2 — Test locally

```bash
streamlit run app.py
```

Open `http://localhost:8501` and test it. ✅

---

### STEP 3 — Create GitHub Repository

1. Go to **https://github.com** → click **New repository**
2. Name it: `spam-email-detector`
3. Set to **Public**
4. Click **Create repository**

---

### STEP 4 — Push code to GitHub

Run these commands in your project folder:

```bash
git init
git add .
git commit -m "first commit: spam detector app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/spam-email-detector.git
git push -u origin main
```

> ⚠️ Replace `YOUR_USERNAME` with your actual GitHub username

---

### STEP 5 — Deploy on Render

1. Go to **https://render.com** → Sign up with GitHub
2. Click **New** → **Web Service**
3. Click **Connect** next to your `spam-email-detector` repo
4. Fill in settings:
   | Field | Value |
   |-------|-------|
   | Name | `spam-email-detector` |
   | Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |
5. Click **Create Web Service**
6. Wait 2-3 minutes for build to complete ⏳
7. Your live URL: `https://spam-email-detector.onrender.com` 🎉

---

### STEP 6 — CI/CD in Action (The Magic!)

Now every time you update code:

```bash
# Make any change to app.py
git add .
git commit -m "updated UI"
git push origin main
```

**Render automatically detects the push → rebuilds → redeploys** 🔄

This is CI/CD — Continuous Integration / Continuous Deployment!

---

## 🧪 Test Emails

**Spam examples:**
```
Congratulations! You've won a $1,000 gift card. Click here to claim now!
URGENT: Your account has been compromised. Verify immediately.
FREE entry! Win FA Cup final tickets. Text to claim your prize!
```

**Ham examples:**
```
Hey, are we still on for dinner tonight at 7?
Please find the meeting agenda attached for tomorrow.
Your flight booking is confirmed. Check your itinerary below.
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| ML Model | Naive Bayes (MultinomialNB) |
| Features | TF-IDF Vectorizer |
| Language | Python 3.11 |
| Version Control | GitHub |
| Deployment | Render (CI/CD) |

---

## 👤 Author
Built as a DevOps + ML project — Dr. T. Thimmaiah Institute of Technology
