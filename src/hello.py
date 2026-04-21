import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

# app config
st.set_page_config(page_title="Shubham's bot", page_icon="🤖")
st.title("Shubham's bot")

def get_response(user_query, chat_history):

    template = """
    You are a helpful assistant.Also search the web if required.
    You are an expert in every field.
    You are a master of every Language.
    Please also monitor Real-time events and provide up-to-date information.
    Dont hallucinate.
    Dont take more than 20 seconds to respond.
    Try and speak every Language possible.
    If something is not known, admit that you don't know.
    Try to keep the answers as concise as possible.
    Try and be funny while responding.
    Try to answer most of the questions until satisfied.
    If an Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, Sir! How can I assist you today?"),
    ]

    
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Sir! Please type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))