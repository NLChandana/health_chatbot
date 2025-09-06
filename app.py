import streamlit as st
from google import genai

# Load API key from Render env var (or st.secrets)
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = (
    "You are a health information assistant. Provide general health info only. "
    "Do NOT diagnose or prescribe. Always add: "
    "'I am not a doctor. Informational only. Consult a licensed healthcare professional.'"
)

st.set_page_config(page_title="Health Chatbot", page_icon="💬")
st.title("💬 Health Chatbot")
st.caption("⚠️ Informational only, not medical advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a health question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Gemini directly
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
    )
    reply = response.text + "\n\n---\n*I am not a doctor. Informational only.*"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
