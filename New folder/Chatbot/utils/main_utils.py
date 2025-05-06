from Chatbot.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

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

def prompt_template():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools if needed."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    return prompt

