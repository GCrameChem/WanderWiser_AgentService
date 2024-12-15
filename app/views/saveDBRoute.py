from flask import Flask, Blueprint, jsonify, request,send_file
import os
import requests
import re
from markdown_it import MarkdownIt
import uuid
from dotenv import load_dotenv

# 加载环境变量 (如果你使用 .env 文件来设置环境变量)
load_dotenv()


# 定义Agent路由根目录
saveDB_route = Blueprint('saveDB', __name__)

@saveDB_route.route('/test', methods=['POST'])
def test_save_DB():
    print(request.data)
    return jsonify({'notice': 'connected'})


# 实际从前端引入
from app.views.AgentRoute import download_main_plan_db


@saveDB_route.route('/main_plan', methods=['POST'])
def save_main_plan():
    # 接收请求中的user_id参数
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    file_url = f"{user_id}/main_plan.md"
    # 调用函数获取MD文件内容，返回的是一个JSON响应
    response = download_main_plan_db(file_url)

    # 提取返回的JSON中的file_content字段
    if response.status_code != 200:
        return jsonify({"error": "File not found or error in fetching the file"}), 404

    md_content = response.json.get("file_content")  # 获取文件内容

    if not md_content:
        return jsonify({"error": "MD file content is empty"}), 400

    print(md_content)
    # 假设md_content是已经获取到的文件内容
    # 提取计划标题
    title_pattern = r"^# (.+?)\n"
    title_match = re.match(title_pattern, md_content)
    plan_name = title_match.group(1) if title_match else "旅行计划"
    print(f"Plan Name: {plan_name}")

    # 修改day_pattern以更宽松地匹配换行符、空格等格式差异
    day_pattern = r"## 第(\d+)天\s*-\s*(.*?)\s*-\s*(.*?)\s*-\s*(\d{4}/\d{2}/\d{2})\n(.*?)\n---"
    matches = re.findall(day_pattern, md_content, re.MULTILINE | re.DOTALL)

    print(f"Matches found: {matches}")

    days = []
    max_day_number = 0

    for match in matches:
        day_number = int(match[0])
        place = match[1]
        weather = match[2]
        date = match[3]
        details = match[4]

        # print(f"Day {day_number} details:\n{details}")
        # 提取每条详细信息中的字段：**关键词**, **主要内容**, **住宿点**
        field_pattern = r"- \*\*(.*?)\*\*\s*[:：]?\s*(.*?)\n"
        field_matches = re.findall(field_pattern, details)

        print(f"Field matches: {field_matches}")
        # 获取关键词、主要内容和住宿点字段
        keyword = field_matches[0][1] if len(field_matches) > 0 else ""
        abstract = field_matches[1][1] if len(field_matches) > 1 else ""
        # 调整住宿点提取的正则表达式，确保正确匹配
        accommodation_pattern = r"- \*\*住宿点\*\*\s*[:：]?\s*(.*?)\n"
        accommodation_match = re.search(accommodation_pattern, details)
        accommodation = accommodation_match.group(1) if accommodation_match else ""
        print(f"Keyword: {keyword}")
        print(f"Abstract: {abstract}")
        print(f"Accommodation: {accommodation}")

        day_data = {
            "day_number": day_number,
            "place": place,
            "weather": weather,
            "date": date,
            "keyword": keyword,
            "abstract": abstract,
            "accommodation": accommodation
        }
        days.append(day_data)

        if day_number > max_day_number:
            max_day_number = day_number

    # 打印days和max_day_number的值以进行调试
    # print(f"Constructed days: {days}")
    # print(f"Max day number: {max_day_number}")
    # 发送请求到 /tripManage/add 接口
    try:
        data = {
            "user_id": user_id,
            "plan_name": plan_name,
            "days": max_day_number,
        }

        # 假设目标接口位于 http://localhost:3000/tripManage/add
        response = requests.post("http://localhost:3000/tripManage/add", json=data)

        if response.status_code == 200:
            # 从响应中提取返回的plan_id
            plan_id = response.json().get('data', {}).get('plan_id')
            # 输出 plan_id 以调试
            print(f"Successfully created trip plan with plan_id: {plan_id}")

            if not plan_id:
                return jsonify({"error": "No plan_id returned from /tripManage/add"}), 500

            # 调用 /addDailyTrip 接口
            print(f"days {days}")
            for day in days:
                daily_trip_data = {
                    "plan_id": plan_id,  # 使用从 /tripManage/add 返回的 plan_id
                    "day": day["day_number"],
                    "location": day["place"],
                    "date": day["date"],
                    "weather": day["weather"],
                    "keywords": day["keyword"],
                    "abstract": day["abstract"],
                    "accomodation": day["accommodation"],
                    "summary": "",  # 若有抽象或简要描述，可以在此处补充
                    "carry_items": ""  # 如果有携带物品，也可以填充此字段
                }

                # 调用 /addDailyTrip 接口
                daily_trip_response = requests.post("http://localhost:3000/tripManage/dailytrips/add", json=daily_trip_data)

                if daily_trip_response.status_code != 200:
                    print(
                        f"Failed to add daily trip for day {day['day_number']}: {daily_trip_response.status_code} - {daily_trip_response.text}")
                    return jsonify({"error": f"Failed to add daily trip for day {day['day_number']}"}), 500

            return jsonify({
                "message": "Plan processed and added successfully, along with daily trips.",
                "plan_id": plan_id
            }), 200
        else:
            return jsonify({"error": "Failed to add trip plan"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
