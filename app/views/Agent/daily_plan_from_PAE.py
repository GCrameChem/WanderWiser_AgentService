# 这个py应该被PAEAgent调用，生成


from app.views.Agent.PAEAgent import agent_executor
from utils.generate_md import generate_daily_md


def generate_daily_plan(text, day, user_id):
    """
    生成每天的行程计划并保存为Markdown文件。

    参数:
    text (str): 用户的输入文本（如旅行计划的描述）。
    user_id (str): 用户的唯一标识符，用于生成用户专属的Markdown文件。

    返回:
    str: 返回生成成功的消息。
    """
    # 获取当前日期
    # day = datetime.datetime.now().strftime('%Y-%m-%d')  # 当前日期，例如 "2024-12-12"

    try:
        # 调用PAEAgent生成行程计划结果
        result = agent_executor.invoke({
            "messages": [("user", text)],
        })

        # 输出生成的行程结果（调试用，可以根据需要调整）
        print(f"Agent result for user {user_id}: {result}")

        # 使用生成的行程计划结果和日期调用generate_daily_md函数生成Markdown文件
        generate_daily_md(user_id, day, result)

        # 返回生成成功的消息
        return f"Plan for {day} generated and saved as markdown file for user {user_id}."

    except Exception as e:
        # 错误处理，如果出现异常，返回错误信息
        return f"Error generating plan: {str(e)}"