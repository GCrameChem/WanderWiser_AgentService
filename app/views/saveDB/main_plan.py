from app.views.AgentRoute import download_main_plan_db
from app.views.saveDBRoute import saveDB_route
from flask import Flask, request, jsonify
import requests
import re
from markdown_it import MarkdownIt
import uuid


# 假设已经存在的函数
# def download_main_plan(file_url):
#     # 模拟从文件或数据库中获取MD格式内容
#     return """
#     # 北京旅游计划
#     ---
#     ## 第1天 - 北京 - 旅游 - 晴 - 2024-12-15
#     - **keyword**: 游玩
#     - **main content**: 详细的内容描述
#     - **the accommodation**: 北京大酒店
#     ---
#     ## 第2天 - 上海 - 旅游 - 阴 - 2024-12-16
#     - **keyword**: 参观
#     - **main content**: 详细的内容描述
#     - **the accommodation**: 上海宾馆
#     """


@saveDB_route.route('/main_plan', methods=['POST'])
def save_main_plan():
    # 接收请求中的user_id参数
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    file_url = f"{user_id}/main_plan.md"
    # 调用函数获取MD文件内容
    md_content = download_main_plan_db(file_url)
    # 确保md_content是字符串，如果是元组，取出第一个元素
    if isinstance(md_content, tuple):
        md_content = md_content[0]  # 假设文件内容是元组的第一个元素

    if not isinstance(md_content, str):
        return jsonify({"error": "Invalid MD file content"}), 400

    # 提取Plan Name（标题）
    title_pattern = r"^# (.+?)\n"  # 正则表达式提取第一个#后的标题
    title_match = re.match(title_pattern, md_content)
    plan_name = title_match.group(1) if title_match else "旅行计划"  # 如果没有标题，使用默认名称

    # 正则表达式提取每一天的计划
    # 改进后的正则表达式，确保能匹配到每一天的计划和住宿点
    day_pattern = r"## 第(\d+)天\s*-\s*(.*?)\s*-\s*(.*?)\s*-\s*(\d{4}/\d{1,2}/\d{1,2})\s*(-.*?)\n- \*\*关键词\*\*\s*[:：]?\s*(.*?)\n- \*\*主要内容\*\*\s*[:：]?\s*([\s\S]*?)\n- \*\*住宿点\*\*\s*[:：]?\s*(.*?)\n---"

    # 使用正则表达式提取每一天的计划
    matches = re.findall(day_pattern, md_content)

    # 打印匹配到的结果以进行调试
    # print(f"Matches: {matches}")

    # 构建days的内容
    days = []

    for match in matches:
        day_data = {
            "day_number": int(match[0]),
            "place": match[1] if match[1] else "Unknown Place",  # 检查并处理空值
            "activity": match[2] if match[2] else "Unknown Activity",
            "weather": match[3] if match[3] else "Unknown Weather",
            "date": match[4] if match[4] else "Unknown Date",
            "keyword": match[5].strip() if match[5] else "No Keywords",  # 防止为空
            "main_content": match[6].strip() if match[6] else "No Main Content",  # 防止为空
            "accommodation": match[7].strip() if match[7] else "No Accommodation"  # 防止为空
        }
        days.append(day_data)
        print(f"\nFinal days list: {days}")

    # 发送请求到 /tripManage/add 接口
    try:
        data = {
            "user_id": user_id,
            "plan_name": plan_name,
            "days": days
        }

        # 假设目标接口位于 http://localhost:3000/tripManage/add
        response = requests.post("http://localhost:3000/tripManage/add", json=data)

        if response.status_code == 200:
            # 从响应中提取返回的plan_id
            plan_id = response.json().get('data', {}).get('plan_id')

            if not plan_id:
                return jsonify({"error": "No plan_id returned from /tripManage/add"}), 500

            # 调用 /addDailyTrip 接口
            for day in days:
                daily_trip_data = {
                    "plan_id": plan_id,  # 使用从 /tripManage/add 返回的 plan_id
                    "day": day["day_number"],
                    "location": day["place"],
                    "date": day["date"],
                    "weather": day["weather"],
                    "keywords": day["keyword"],
                    "summary": day["main_content"],
                    "accomodation": day["accommodation"],
                    "abstract": "",  # 若有抽象或简要描述，可以在此处补充
                    "carry_items": ""  # 如果有携带物品，也可以填充此字段
                }

                # 调用 /addDailyTrip 接口
                daily_trip_response = requests.post("http://localhost:3000/addDailyTrip", json=daily_trip_data)

                if daily_trip_response.status_code != 200:
                    return jsonify({"error": f"Failed to add daily trip for day {day['day_number']}"}), 500

            return jsonify({
                "message": "Plan processed and added successfully, along with daily trips.",
                "plan_id": plan_id
            }), 200
        else:
            return jsonify({"error": "Failed to add trip plan"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
