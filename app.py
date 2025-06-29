import streamlit as st
import requests

st.set_page_config(page_title="Emotional State Checker", layout="centered")

st.title("🧠 Emotional State Prediction")

st.write("Describe how you’ve been feeling lately:")

user_input = st.text_area("Your response:", height=150)

st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117;
    color: #FAFAFA;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    border-top: 1px solid #262730;
}
</style>
<div class="footer">
    Made with ❤️ by <a href="https://github.com/BishanKD" target="_blank">Bishan Kumar Deka</a>
</div>
""", unsafe_allow_html=True)

if st.button("Predict Emotion"):
    if not user_input.strip():
        st.warning("Please enter something.")
    else:
        with st.spinner("Analyzing..."):
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"text": user_input}
            )
            if response.status_code == 200:
                score = response.json()["emotion_score"]
                st.success(f"🧭 Emotional Score: {round(score*10, 2)}/10")

                # Color-coded feedback
                if score > 0.8:
                    msg = "You're feeling ecstatic! 🎉"
                    color = "🟢"
                elif score > 0.5:
                    msg = "You're doing great. 😊"
                    color = "🟡"
                elif score > 0.3:
                    msg = "You might be feeling low. 😟"
                    color = "🟠"
                else:
                    msg = "You're deeply distressed. Reach out. ❤️"
                    color = "🔴"

                st.markdown(f"### {color} {msg}")

            else:
                st.error("Something went wrong while calling the backend.")