from Chatbot.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage

def callback_call():
    stream_handler = StreamingStdOutCallbackHandler()
    callbacks = [stream_handler]
    return callbacks
def load_google_LLM():
    llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMP,
            max_tokens =Config.MAX_TOKEN ,
            timeout = Config.TIME_OUT,
            max_retries= Config.MAX_RETRIES,
            streaming=True,
            callbacks=callback_call(),
            #handle_parsing_errors=True
            
        )
    return llm

def serialize_messages(chat_history):
    """
    Convert LangChain chat messages to a list of plain dicts for JSON response.
    """
    serialized = []
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            role = "system"
        serialized.append({"role": role, "content": msg.content})
    return serialized


