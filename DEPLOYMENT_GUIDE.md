# 🚀 Spam Email Detector — Full Deployment Guide
## GitHub + Render CI/CD Pipeline

---

## 📁 Project Structure

```
spam-detector/
├── app.py              ← Main Streamlit app
├── train_model.py      ← Run once to generate model.pkl
├── model.pkl           ← Trained ML model (auto-generated)
├── requirements.txt    ← Python dependencies
├── runtime.txt         ← Python version for Render
└── .gitignore          ← Files to exclude from Git
```

---

## STEP 1 — Set Up Locally

### 1.1 Install dependencies
```bash
pip install streamlit scikit-learn numpy
```

### 1.2 Train the model (run once)
```bash
python train_model.py
```
This creates `model.pkl` in your project folder.

### 1.3 Run the app locally
```bash
streamlit run app.py
```
Open http://localhost:8501 — you should see the app! ✅

---

## STEP 2 — Push to GitHub

### 2.1 Create a GitHub account
Go to https://github.com and sign up (free).

### 2.2 Create a new repository
1. Click the **+** button → **New repository**
2. Name it: `spam-email-detector`
3. Set to **Public**
4. Click **Create repository**

### 2.3 Push your code
Open terminal in your project folder and run:

```bash
# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Spam Email Detector"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/spam-email-detector.git

# Push to GitHub
git branch -M main
git push -u origin main
```

✅ Your code is now on GitHub!

---

## STEP 3 — Deploy on Render

### 3.1 Create a Render account
Go to https://render.com and sign up with your GitHub account (free).

### 3.2 Create a new Web Service
1. Click **New +** → **Web Service**
2. Click **Connect a repository**
3. Select your `spam-email-detector` repo
4. Click **Connect**

### 3.3 Configure the service

| Field             | Value                        |
|-------------------|------------------------------|
| **Name**          | spam-email-detector          |
| **Region**        | Singapore (closest to India) |
| **Branch**        | main                         |
| **Runtime**       | Python 3                     |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

### 3.4 Deploy!
Click **Create Web Service**.

Render will:
1. Clone your GitHub repo
2. Install all requirements
3. Start your Streamlit app
4. Give you a live URL like: `https://spam-email-detector.onrender.com`

⏳ First deploy takes 3-5 minutes. Watch the logs!

---

## STEP 4 — CI/CD in Action (The Magic Part!)

This is what makes it DevOps — every time you push code to GitHub,
Render automatically redeploys. No manual work needed!

### Try it:
```bash
# Make any small change to app.py (e.g. change a text)
# Then:

git add .
git commit -m "Updated app title"
git push origin main
```

Watch Render automatically rebuild and redeploy! ✅

---

## STEP 5 — Verify Everything Works

| Check | How |
|-------|-----|
| App loads | Visit your Render URL |
| Spam detected | Paste a spam email, click Analyse |
| Ham detected | Paste a normal email, click Analyse |
| Sample buttons | Click 🚨 Spam Sample / ✅ Ham Sample |
| History works | Make 3+ detections, check history table |
| Auto-deploy | Push a small code change, watch Render redeploy |

---

## 🧠 How the ML Works

```
Email Text
    ↓
TF-IDF Vectorizer          ← Converts text to numbers
    ↓                         (Term Frequency-Inverse Document Frequency)
Naive Bayes Classifier     ← Predicts spam/ham probability
    ↓
Confidence Score + Label
```

**Why Naive Bayes for spam?**
- Fast and lightweight
- Works great with text data
- Industry standard for email filtering (used by Gmail!)
- Trained on TF-IDF features (word importance scores)

---

## 🔧 Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| `model.pkl not found` | Run `python train_model.py` first |
| Build fails on Render | Check `requirements.txt` versions |
| App not loading | Check Render logs for errors |
| Port error | Make sure start command includes `--server.port $PORT` |
| Slow first load | Render free tier sleeps after 15min — wait 30 seconds |

---

## 🚀 Future Improvements (for report)

1. Use the full **UCI SMS Spam Dataset** (5,574 emails) for better accuracy
2. Add **Docker** containerization
3. Add **GitHub Actions** for automated testing before deploy
4. Add a **database** to store detection history permanently
5. Build a **REST API** with FastAPI alongside the Streamlit UI

---

## 📝 For Your Report

- **GitHub Repo:** https://github.com/YOUR_USERNAME/spam-email-detector
- **Live App:** https://spam-email-detector.onrender.com
- **ML Model:** Naive Bayes with TF-IDF vectorization
- **CI/CD:** GitHub webhook → Render auto-deploy
- **Framework:** Streamlit (Python)
