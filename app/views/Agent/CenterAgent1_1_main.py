

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
Any other request is NOT allowable, give me tender warning if I do so.
and here is my idea:{messages}
and your answer should be based on this template, in the format of MARKDOWN, in the language of Chinese:
# (Title)
---
## 第(number)天 - (place, activity, restaurant, accommodation or other) - (weather forecast) - (date)
- **(keyword)**: (the content)
- **(main content)**: (detailed content)
- **(the accommadation)**: (detailed content)
---
(if a multi-day plan, the other block are the same as above.
## 第(number+1)天 - (place, activity, restaurant, accommodation or other) - (weather forecast) - (date)
......)
    """
)

# Choose the LLM that will drive the agent
llm = ChatOpenAI(model="gpt-4-turbo-preview")
agent_executor = create_react_agent(llm, tools=[], state_modifier=SystemPrompt)
SystemPrompt.pretty_print()

from langchain_core.output_parsers import StrOutputParser

# 定义一个解析器对象
parser = StrOutputParser()

chain = SystemPrompt | llm | parser


# agent_executor.invoke({
#     "messages": [("user", "我和一个朋友想要去成都旅游三天，我们喜欢人文艺术。请你给我们规划一份行程安排。")],
# })

# # 终端测试
# user_input = input("请输入你的旅行需求：")
# agent_executor.invoke({
#     "messages": [("user", user_input)],
# })




