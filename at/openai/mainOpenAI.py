import streamlit as st

from at.openai.ApiCaller import OpenAICaller
from dotenv import load_dotenv

content = "What's the Id of person Amy?"
load_dotenv()
apiCaller = OpenAICaller()

# configuring streamlit page settings
st.set_page_config(
    page_title="AI Bot",
    page_icon="💬",
    layout="centered"
)

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🤖 Smart Bot powered by OpenAI")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("Ask OpenAI GPT...")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    input_messages = [{"role": "user", "content": user_prompt}]
    st.session_state.chat_history.append(input_messages[0])

    # send user's message to GPT-4o and get a response
    response = apiCaller.get_response_from_openai(input_messages)
    assistant_response = response.output_text
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)