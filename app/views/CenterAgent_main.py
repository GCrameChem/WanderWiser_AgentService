# Agent模块逻辑


# %%capture --no-stderr
# %pip install --quiet -U langgraph langchain-community langchain-openai tavily-python

import getpass
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

# 加载.env文件的环境变量
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
agent_executor = create_react_agent(llm, tools, state_modifier=SystemPrompt)
SystemPrompt.pretty_print()

uence([SystemPrompt, llm])
# SystemPrompt.pretty_print()

agent_executor.invoke({
    "messages": [("user", "我和一个朋友想要去成都旅游三天，我们喜欢人文艺术。请你给我们规划一份行程安排。")],
})

import operator
from typing import Annotated, List, Tuple
from typing_extensions import TypedDict


class PlanExecute(TypedDict):
    input: str
    plan: List[str] # 计划轨迹
    past_steps: Annotated[List[Tuple], operator.add]
    response: str # 响应结果

from pydantic import BaseModel, Field


class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

from langchain_core.prompts import ChatPromptTemplate

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.""",
        ),
        ("placeholder", "{messages}"),
    ]
)
planner = planner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Plan)

planner.invoke(
    {
        "messages": [
            ("user", "我和一个朋友想要去成都旅游三天，我们喜欢人文艺术。请你给我们规划一份行程安排。")
        ]
    }
)

from typing import Union


class Response(BaseModel):
    """Response to user."""

    response: str


class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )


replanner_prompt = ChatPromptTemplate.from_template(
    """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

Your objective was this:
{input}

Your original plan was this:
{plan}

You have currently done the follow steps:
{past_steps}

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan."""
)


replanner = replanner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Act)

from typing import Literal
from langgraph.graph import END


async def execute_step(state: PlanExecute):
    plan = state["plan"]
    plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
    task = plan[0]
    task_formatted = f"""For the following plan:
{plan_str}\n\nYou are tasked with executing step {1}, {task}."""
    agent_response = await agent_executor.ainvoke(
        {"messages": [("user", task_formatted)]}
    )
    return {
        "past_steps": [(task, agent_response["messages"][-1].content)],
    }


async def plan_step(state: PlanExecute):
    plan = await planner.ainvoke({"messages": [("user", state["input"])]})
    return {"plan": plan.steps}


async def replan_step(state: PlanExecute):
    output = await replanner.ainvoke(state)
    if isinstance(output.action, Response):
        return {"response": output.action.response}
    else:
        return {"plan": output.action.steps}


def should_end(state: PlanExecute):
    if "response" in state and state["response"]:
        return END
    else:
        return "agent"

from langgraph.graph import StateGraph, START

workflow = StateGraph(PlanExecute)

# Add the plan node
workflow.add_node("planner", plan_step)

# Add the execution step
workflow.add_node("agent", execute_step)

# Add a replan node
workflow.add_node("replan", replan_step)

workflow.add_edge(START, "planner")

# From plan we go to agent
workflow.add_edge("planner", "agent")

# From agent, we replan
workflow.add_edge("agent", "replan")

workflow.add_conditional_edges(
    "replan",
    # Next, we pass in the function that will determine which node is called next.
    should_end,
    ["agent", END],
)

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()


# from IPython.display import Image, display
#
# display(Image(app.get_graph(xray=True).draw_mermaid_png()))

config = {"recursion_limit": 50}
inputs = {"input": "我和一个朋友想要去成都旅游三天，我们喜欢人文艺术。请你给我们规划一份行程安排。"}
async for event in app.astream(inputs, config=config):
    for k, v in event.items():
        if k != "__end__":
            print(v)

# async def run():
#     config = {"recursion_limit": 20}
#     inputs = {
#         "input": "我和一个朋友想要去成都旅游三天，我们喜欢人文艺术。请你给我们规划一份行程安排。"}
#     async for event in app.astream(inputs, config=config):
#         for k, v in event.items():
#             if k != "__end__":
#                 print(v)

# asyncio.run(run())



