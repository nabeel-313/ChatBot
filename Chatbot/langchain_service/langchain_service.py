from Chatbot.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from Chatbot.exception import ChatException
from Chatbot.logger import logging
import sys
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

def generate_response(user_message):
    """
    Generate a response using LangChain with VertexAI.
    """
    try:
        logging.info(f"Answering the User message {user_message}")
        load_dotenv(find_dotenv(), override=True)
        llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMP
        )
        #print(llm)
        response = llm.invoke(user_message)
        #print(user_message)
        #print(response)
        return response
    except Exception as e:
        raise ChatException(e,sys)
