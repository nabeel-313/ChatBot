from Chatbot.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from Chatbot.exception import ChatException
from Chatbot.logger import logging

import sys
from dotenv import load_dotenv, find_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
f
load_dotenv(find_dotenv(), override=True)

def generate_response(user_message):
    """
Processes the user input and returns the LLM response.

:param user_input: str
    The query provided by the user.
:return: str
    The response generated by the LLM for the given query.
:raises Exception:
    If the function encounters an error during execution.
:description:
    This function takes user input, processes it, and returns the output
    generated by the LLM for the query. In case of failure, it raises an exception.
"""
    try:
        logging.info(f"Answering the User message {user_message}")
        load_dotenv(find_dotenv(), override=True)
        llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMP
        )
        memory = ConversationSummaryBufferMemory(
            llm = llm,
            max_token_limit=Config.MAX_TOKEN
        )
        conversation = ConversationChain(
            llm = llm,
            memory = memory
        )
        response = conversation.run(input=user_message)
        #print(response)
        return response
    except Exception as e:
        raise ChatException(e,sys)
