import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_astradb import AstraDBVectorStore
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from astrapy.info import CollectionVectorServiceOptions
import base64

# Streaming call back handler for responses
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text + "▌")

# Cache prompt for future runs
@st.cache_data()
def load_prompt():
    template = """You’re a helpful AI assistant tasked with helping users find the perfect bicycle based on their preferences and needs. You're friendly and provide extensive answers. Use bullet points to summarize your suggestions. Here's how you can assist:

After gathering the user's preferences, provide at least two bicycle products that match their criteria.
Use bullet points to summarize each suggestion, including key features, benefits, and price.
Example:
"Mountain Bike: Trailblazer 300
Durable frame with advanced suspension system
Excellent traction for rugged terrain
Price: $1500"
"Road Bike: Speedster 200
Lightweight aerodynamic design
High-performance tires for speed
Price: $800"

Encourage Further Questions and Offer Additional Assistance:

"Feel free to ask any more questions or provide additional details if needed. I'm here to help you find the best bicycle for your needs!"

CONTEXT:
{context}

QUESTION:
{question}

YOUR ANSWER:"""
    return ChatPromptTemplate.from_messages([("system", template)])
prompt = load_prompt()

# Cache OpenAI Chat Model for future runs
@st.cache_resource()
def load_chat_model():
    return ChatOpenAI(
        temperature=0.3,
        model='gpt-3.5-turbo',
        streaming=True,
        verbose=True
    )
chat_model = load_chat_model()

nvidia_vectorize_options = CollectionVectorServiceOptions(
    provider="nvidia",
    model_name="NV-Embed-QA",
)

# Cache the Astra DB Vector Store for future runs
@st.cache_resource(show_spinner='Connecting to Astra')
def load_vector_store():
    # Connect to the Vector Store
    vector_store = AstraDBVectorStore(
        collection_name="bicycle_catalog",
        api_endpoint=st.secrets['ASTRA_API_ENDPOINT'],
        token=st.secrets['ASTRA_TOKEN'],
        collection_vector_service_options=nvidia_vectorize_options,
    )
    return vector_store

vector_store = load_vector_store()

# Cache the Retriever for future runs
@st.cache_resource(show_spinner='Getting retriever')
def load_retriever():
    # Get the retriever for the Chat Model
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.5, "k": 3},
    )
    return retriever
retriever = load_retriever()

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

    # UI placeholder to start filling with agent response
    with st.chat_message('assistant'):
        response_placeholder = st.empty()

    # Generate the answer by calling OpenAI's Chat Model
    inputs = RunnableMap({
        'context': lambda x: retriever.invoke(x['question']),
        'question': lambda x: x['question']
    })
    chain = inputs | prompt | chat_model
    response = chain.invoke({'question': question}, config={'callbacks': [StreamHandler(response_placeholder)]})
    answer = response.content

    # Store the bot's answer in a session object for redrawing next time
    st.session_state.messages.append({"role": "ai", "content": answer})

    # Write the final answer without the cursor
    response_placeholder.markdown(answer)