from Chatbot.config import Config
from Chatbot.exception import ChatException
from Chatbot.logger import logging
from Chatbot.utils.main_utils import load_google_LLM, callback_call, serialize_messages
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables import RunnableConfig
from Chatbot.tools.tools import *
import sys
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv, find_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain import hub
load_dotenv(find_dotenv(), override=True)

#list of tools
tools = [google_search_tool,create_weather_tool(),convert_c_to_f,live_cricket_score]
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human", "{input}"),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),
# ])
prompt = hub.pull("hwchase17/react")
def create_tool_agent():
    agent = create_react_agent(
        llm = load_google_LLM(),
        tools = tools,
        prompt=prompt,
        #verbose = True
    )
    return agent
    
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
        print("answering user qustion")
        logging.info(f"Answering the User message {user_message}")
        load_dotenv(find_dotenv(), override=True)
        #llm = load_google_LLM()
        print("loading llm done")
        

        memory = ConversationBufferMemory(
            memory_key="chat_history",  
            return_messages=True
        )
        print("memory done")
        print("Agnt Executor started")

        agent_executor = AgentExecutor(
                            agent=create_tool_agent(),
                            tools=tools,
                            memory=memory,
                            verbose = True,
                            return_intermediate_steps = True,
                            handle_parsing_errors = True
        )
        print("Agnt Executor done ------>>>>>>", agent_executor)
        config = RunnableConfig(callbacks=callback_call())
        print("user_mesage is --->>", user_message)
        print("Registered Tools:", agent_executor.tools)
        response = agent_executor.invoke(
                            {"input": user_message },
                             config=config
                            )
        
        print('Inside generate function --->>>>',response)
        chat_history = memory.chat_memory.messages  # Includes HumanMessage and AIMessage
        serialized_history = serialize_messages(chat_history)
        print(" response output --->>>", response["output"])

        return {
            "input": user_message,
            "output": response["output"],
            "chat_history": serialized_history
        }
    
    except Exception as e:
        raise ChatException(e,sys)
