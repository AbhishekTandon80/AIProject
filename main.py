python
import streamlit as st
from at.mistral.ApiCaller import MistralCaller
from at.openai.ApiCaller import OpenAICaller
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API callers
mistral_caller = MistralCaller()
openai_caller = OpenAICaller()

# Streamlit page configuration
st.set_page_config(
    page_title="AI Bot",
    page_icon="💬",
    layout="centered"
)

# Model selection
option = st.selectbox(
    "Select the LLM Model (default - Mistral) to use.",
    ("Mistral", "OpenAI"),
)
st.write("Selected:", option)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 Smart Bot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Ask GPT...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    input_message = {"role": "user", "content": user_prompt}
    st.session_state.chat_history.append(input_message)

    # Get response from selected LLM
    if option == "Mistral":
        response = mistral_caller.response_from_mistral([input_message])
        assistant_response = response.choices[0].message.content
    else:
        response = openai_caller.get_response_from_openai([input_message])
        assistant_response = response.output_text

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)