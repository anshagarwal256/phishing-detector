# app.py
import streamlit as st
import joblib
import re

# -----------------------------
# Load model and vectorizer
# -----------------------------
vectorizer = joblib.load("model/vectorizer.pkl")
model = joblib.load("model/model.pkl")

# -----------------------------
# Text cleaning function
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " link ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Phishing Detector", page_icon="📧")

st.title("📧 Phishing Email Detection System")
st.write("Paste an email (subject + body) to check if it is **Safe** or **Phishing**.")

email_text = st.text_area("Email Content", height=250)

if st.button("Check Email"):
    if email_text.strip() == "":
        st.warning("⚠️ Please paste an email first.")
    else:
        cleaned = clean_text(email_text)
        vectorized = vectorizer.transform([cleaned])

        prediction = model.predict(vectorized)[0]
        probability = model.predict_proba(vectorized)[0][1]

        if prediction == 1:
            st.error(f"⚠️ PHISHING DETECTED\n\nConfidence: {probability*100:.2f}%")
        else:
            st.success(f"✅ SAFE EMAIL\n\nConfidence: {(1-probability)*100:.2f}%")

st.markdown("---")
st.caption("Software-only phishing detection using Machine Learning")
