import streamlit as st
import requests
import os
import json

# ---------- 🎯 Page Config ----------
st.set_page_config(page_title="Insurance Q&A - HackRx", page_icon="📄")

# ---------- 🎯 Header ----------
st.title("🛡️ Insurance Policy Q&A Assistant")
st.markdown("**Ask questions about your uploaded policy PDFs. Get clause-based answers — fast.**")
st.markdown("---")

# ---------- 📤 Upload Section ----------
st.subheader("📤 Upload Policy PDF")
pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if pdf_file:
    st.success(f"✅ Uploaded: `{pdf_file.name}`")

# ---------- ❓ Questions Section ----------
st.subheader("❓ Enter Your Questions")
questions_input = st.text_area(
    "Write one question per line (e.g. Is maternity covered?)",
    placeholder="e.g.\nIs maternity covered?\nWhat is the waiting period?\nDoes it cover knee surgery?",
    height=150
)

# ---------- 🚀 Button ----------
if st.button("Get Answers 🚀"):
    if not pdf_file or not questions_input.strip():
        st.warning("⚠️ Please upload a PDF and enter at least one question.")
    else:
        with st.spinner("🧠 Thinking... Getting answers from the policy..."):
            # Prepare multipart request
            files = {"pdf": pdf_file.getvalue()}
            questions = [q.strip() for q in questions_input.strip().split("\n") if q.strip()]
            data = {"questions": json.dumps(questions)}

            try:
                # ✅ Replace this with your actual backend URL
                res = requests.post(
                    "https://ayush018-hackrx-fastapi.hf.space/api/v1/hackrx/run",
                    files=files,
                    data=data
                )

                if res.status_code == 200:
                    results = res.json()["answers"]
                    st.success("✅ Answers retrieved!")

                    for item in results:
                        st.markdown("### 📄 " + item["document"])
                        st.markdown(f"**❓ Question:** {item['question']}")
                        if item['answer'].startswith("❌"):
                            st.error(f"🟥 {item['answer']}")
                        else:
                            st.info(f"🧠 {item['answer']}")
                        st.markdown("---")
                else:
                    st.error(f"❌ Backend error: {res.status_code}\n{res.text}")

            except Exception as e:
                st.error(f"❌ Failed to contact backend: `{e}`")
