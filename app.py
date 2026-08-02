# app.py
import streamlit as st
from chat_flow import chat_with_assistant_stream

st.set_page_config(page_title="Prakhar Dwivedi | Portfolio Assistant", page_icon="🤖", layout="wide")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.image("avatar.png", use_container_width=True)
    st.markdown("### Prakhar Dwivedi")
    st.caption("Data Scientist & AI/ML Engineer")

    st.markdown("---")
    st.markdown("**Try asking:**")

    example_questions = [
        "What are your past work experiences?",
        "What job is he currently looking for?",
        "How can I connect with you?",
    ]

    clicked_question = None
    for question in example_questions:
        if st.button(question, use_container_width=True):
            clicked_question = question

    st.markdown("---")
    st.markdown(
        "[💻 GitHub](https://github.com/prakharpd)  \n"
        "[👔 LinkedIn](https://www.linkedin.com/in/prakhardwivedi-pd/)  \n"
        "[🌐 Portfolio](https://pd-portfolio18.netlify.app/)"
    )

# ---------------- Main chat area ----------------
st.title("Prakhar Dwivedi")
st.caption("Data Scientist & AI/ML Engineer — Ask me anything about his work!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about Prakhar's projects, skills, or experience...")

# if a sidebar example was clicked, treat it like typed input
if clicked_question:
    user_input = clicked_question

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        reply_box = st.empty()
        final_reply = ""
        for partial_reply in chat_with_assistant_stream(user_input, st.session_state.messages[:-1]):
            final_reply = partial_reply
            reply_box.write(final_reply)

    st.session_state.messages.append({"role": "assistant", "content": final_reply})
    st.rerun()
