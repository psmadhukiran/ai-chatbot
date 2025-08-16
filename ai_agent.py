# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#Step1: Setup API Keys for Groq, OpenAI and Tavily
import os

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

#Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch 


openai_llm=ChatOpenAI(model="gpt-4.1")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile")

search_tool=TavilySearch(max_results=2)

#Step3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
system_prompt="Act as an AI chatbot who is smart and friendly"

# def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
#     if provider=="Groq":
#         llm=ChatGroq(model=llm_id)
#     elif provider=="OpenAI":
#         llm=ChatOpenAI(model=llm_id)

#     tools=[TavilySearch(max_results=2)] if allow_search else []
#     agent=create_react_agent(
#         model=llm,
#         tools=tools,
#         # state_modifier=system_prompt
#     )
#     # query = "Who is the founder of Tiger Analytics Company?"
#     state={"messages":  [
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=query)
#         ]}
#     response=agent.invoke(state)
#     messages=response.get("messages")
#     ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
#     # print(ai_messages[-1])
#     return ai_messages[-1]

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Pick provider
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # Tools
    tools = [TavilySearch(max_results=2)] if allow_search else []

    # Create agent (without state_modifier)
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Build state manually (inject system prompt + user query)
    state = {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query if isinstance(query, str) else " ".join(query))
        ]
    }

    response = agent.invoke(state)

    messages = response.get("messages", [])
    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]
    return ai_messages[-1] if ai_messages else "⚠️ No response from agent"