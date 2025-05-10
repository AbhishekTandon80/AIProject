import streamlit as st


from at.mistral.ApiCaller import MistralCaller
from at.openai.CallingFunction import OpenAICaller

content = "What's the Id of person Amy?"
mistralCaller = MistralCaller()
openAiCaller = OpenAICaller()

# configuring streamlit page settings
st.set_page_config(
    page_title="AI Bot",
    page_icon="💬",
    layout="centered"
)

import streamlit as st

option = st.selectbox(
    "Select the LLM Model (default - Mistral) to use.",
    ("Mistral", "OpenAI"),
)

st.write("Selected:", option)

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🤖 Smart Bot")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("Ask GPT...")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    input_messages = [{"role": "user", "content": user_prompt}]
    st.session_state.chat_history.append(input_messages[0])

    # send user's message to GPT-4o and get a response
    if option == "Mistral":
        print("Making a call to Mistral LLM")
        response = mistralCaller.response_from_mistral(input_messages)
        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    elif option == "OpenAI":
        print("Making a call to OpenAI LLM")
        response = openAiCaller.get_response_from_openai(input_messages)
        assistant_response = response.output_text
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})


    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

