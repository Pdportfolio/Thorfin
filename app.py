import streamlit as st
from chat_flow import chat_with_assistant_stream

st.set_page_config(page_title="Prakhar Dwivedi | AI Agent", page_icon="🤖")

st.title("Prakhar Dwivedi")
st.caption("Data Scientist & AI/ML Engineer — Ask me anything about his work!")

# Keep chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get new user input
user_input = st.chat_input("Ask about Prakhar's projects, skills, or experience...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get bot reply (streaming)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        final_text = ""
        for chunk in chat_with_assistant_stream(user_input, st.session_state.messages[:-1]):
            final_text = chunk
            placeholder.write(final_text)

    st.session_state.messages.append({"role": "assistant", "content": final_text})
