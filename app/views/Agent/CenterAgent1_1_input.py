

import getpass
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults



tools = [TavilySearchResults(max_results=3)]

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain import OpenAI,PromptTemplate,LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.llms import OpenAI
from langchain import LLMMathChain

from langgraph.prebuilt import create_react_agent

# Get the prompt to use - you can modify this!
# prompt = hub.pull("ih/ih-react-agent-executor")
SystemPrompt = PromptTemplate(
    input_variables=["messages"],
    template="""you are an expert at planning a multi-day journey. Now I will tell you some of my idea which include but not just the destination,
my interest and requirement. You should use tools and the template that I will give you later to help me generate a feasible and custom-made plan.
Here is my idea:{messages};
Notice, you may encounter those situations:
1. Greeting or other everyday conversation: You should respond politely and briefly, steer the conversation to travel plans, and ask me about their specific needs.
2. My demand description is not clear: Before you generate the plan, you should first ask the user's trip date and days, if I do not tell you, you should try to ask first rather than directly generate the plan. But if I am not clear, you can just generate suggestions.
3. Be asked for planning suggestions: Once you have enough information, you can go straight to the tools and templates.

if you encounter Situation3, The FIRST line of your OUTPUT must annotate "situation 3" and then respond in the language of Chinese, 
your planning suggestions should be only based on this template(no more conversation),in the language of Chinese:
"Situation3
# (Title)
---
## 第(number)天 - (place, activity, restaurant, accommodation or other) - (weather forecast) - (date)
- **关键词**: (the keyword)
- **主要内容**: (detailed content)
- **住宿点**: (the accommodation)
(这里需要空一行)
---
(if a multi-day plan, the other block are the same as above.
## 第(number+1)天 - (place, activity, restaurant, accommodation or other) - (weather forecast) - (date)
......)
"
But if you encounter situation 1 or 2, do not add any FIRST line, just like this: 
"(your response in the language of CHINESE)" 
And any other request is NOT allowable, give me tender warning if I do so.
    """
)

# Choose the LLM that will drive the agent
from langgraph.checkpoint.memory import MemorySaver
llm = ChatOpenAI(model="gpt-4-turbo")
memory = MemorySaver()
agent_executor = create_react_agent(llm, tools, state_modifier=SystemPrompt,checkpointer=memory)
# SystemPrompt.pretty_print()


# add memory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

def generate_travel_plan(user_id, user_input):
    config = {"configurable": {"thread_id": user_id}}
    print("agent successfully created ")
    try:
        # 调用 agent_executor，并传入用户输入的需求

        result = agent_executor.invoke(
            {"messages": [ ("user", user_input)]},config,
        )["messages"][-1].content

        print(result)
        # result = agent_executor.invoke({
        #     "messages": [("user", user_input)],  # 传递用户输入
        # })
        return result
        # return result["messages"][-1].content  # 返回生成的结果
    except Exception as e:
        # 处理异常并返回错误信息
        print(user_input)
        return {"error": str(e)}

#
# agent_executor.invoke({
#     "messages": [("user", "我和一个朋友想要去成都旅游三天，我们喜欢人文艺术。请你给我们规划一份行程安排。")],
# })


