# app.py
# This is the main chat page. It shows the conversation and
# sends user messages to chat_flow.py to get replies.

import streamlit as st
from chat_flow import chat_with_assistant_stream

st.set_page_config(page_title="Prakhar Dwivedi | AI Agent", page_icon="🤖")

st.title("Prakhar Dwivedi")
st.caption("Data Scientist & AI/ML Engineer — Ask me anything about his work!")

# Keep chat history for this session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get new input from the user
user_input = st.chat_input("Ask about Prakhar's projects, skills, or experience...")

if user_input:
    # Save and show the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get and show the assistant's reply as it streams in
    with st.chat_message("assistant"):
        reply_box = st.empty()
        final_reply = ""
        for partial_reply in chat_with_assistant_stream(user_input, st.session_state.messages[:-1]):
            final_reply = partial_reply
            reply_box.write(final_reply)

    # Save the final reply to history
    st.session_state.messages.append({"role": "assistant", "content": final_reply})
