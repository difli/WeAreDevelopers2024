import streamlit as st
import requests
import json
import base64


# Function to get the response from the API
def get_ai_response(question):
    # URL and headers
    url = "http://54.75.128.187:7860/api/v1/run/02d23378-38c0-4a95-98e4-fda5bdad068a?stream=false"
    headers = {
        'Content-Type': 'application/json'
    }

    # Payload
    data = {
        "input_value": question,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatInput-zIXrB": {},
            "AstraDB-Yr0Bn": {},
            "AstraVectorize-WYGLa": {},
            "Prompt-4Qm7P": {},
            "ParseData-ygMFu": {},
            "OpenAIModel-QCEVx": {},
            "ChatOutput-rfvLT": {}
        }
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        response_data = response.json()
        # Extract the 'text' field from the response
        text_message = response_data['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        return text_message
    else:
        return f"Failed to get response. Status code: {response.status_code}"


# Start with empty messages, stored in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to add background image
# Function to add background image from a local file
# Function to add background image with transparency
def add_bg_from_local(image_file, opacity=0.5):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use the function to set the background with the desired transparency level
add_bg_from_local('assets/bike.png', opacity=0.8)

# Draw a title and some markdown
st.title("Bicycle Recommendation Service")
st.markdown("""Welcome to our bicycle recommendation service! Let's find the perfect bike based on your preferences. Please provide as much detail as possible so I can suggest the best options for you.""")
# Adding "powered by Langflow" text
st.markdown("""
    <div style='text-align: right; color: grey;'>
        <small>Powered by <a href='https://www.langflow.org/' target='_blank'>Langflow</a></small>
    </div>
""", unsafe_allow_html=True)

# Draw all messages, both user and bot so far (every time the app reruns)
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# Draw the chat input box
if question := st.chat_input("What's up?"):
    # Store the user's question in a session object for redrawing next time
    st.session_state.messages.append({"role": "human", "content": question})

    # Draw the user's question
    with st.chat_message('human'):
        st.markdown(question)

    # Get the AI response
    answer = get_ai_response(question)

    # Store the bot's answer in a session object for redrawing next time
    st.session_state.messages.append({"role": "ai", "content": answer})

    # Draw the bot's answer
    with st.chat_message('assistant'):
        st.markdown(answer)
