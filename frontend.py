import streamlit as st
import requests

st.set_page_config(page_title="Infinite Pay Interface", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #4F8BF9;'>Infinite Pay Interface 🤖</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

env = st.sidebar.selectbox(
    "Select API environment",
    options=["Local", "Render (Prod)"],
    format_func=lambda x: x
)

base_url = "http://localhost:8000" if env == "Local" else "https://infinitepayinterface.onrender.com"

with st.form("agent_form"):
    message = st.text_area("Your Message:", placeholder="Ex: I want to know my current balance.")
    user_id = st.text_input("User ID:", placeholder="Ex: user_123")
    tone = st.selectbox("Response tone:", ["professional", "casual", "pragmatic", "humorous", "sad"])
    submitted = st.form_submit_button("Send")

if submitted:
    if not message or not user_id:
        st.warning("⚠️ Please fill out all fields before submitting.")
    else:
        try:
            response = requests.post(
                f"{base_url}/ask",
                json={"message": message, "user_id": user_id, "tone": tone},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()

                st.markdown(f"""
                    <div style='
                        background-color: #f1f3f8;
                        padding: 20px;
                        border-radius: 10px;
                        border-left: 6px solid #4F8BF9;
                        font-size: 18px;
                        color: #333;
                    '>
                        {data['response']}
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("---")
                with st.expander("Original response (no personality):"):
                    st.code(data["source_agent_response"])

                with st.expander("Agent Workflow:"):
                    st.json(data["agent_workflow"])

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Failed Connecting to API: {e}")

