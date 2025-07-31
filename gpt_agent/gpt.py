import openai
import os
from dotenv import load_dotenv

load_dotenv()

GPT_KEY = os.getenv('GPT_KEY')
openai.api_key = GPT_KEY  # 실제 사용 시 보안 관리 필요

from flask import Blueprint, request, jsonify
from gpt_agent.ai_comment import generate_comment, format_comment_by_sentence

gpt_bp = Blueprint('gpt', __name__)

@gpt_bp.route("/generate-comment", methods=["POST"])
def generate():
    data = request.get_json()
    menu_name = data.get("menu_name")
    ingredients = data.get("ingredients")
    nutrients = data.get("nutrients")

    if not menu_name or not ingredients or not nutrients:
        return jsonify({"error": "필수 값 누락"}), 400

    try:
        comment = generate_comment(menu_name, ingredients, nutrients)
        formatted = format_comment_by_sentence(comment)
        return jsonify({
            "menu_name": menu_name,
            "comment": formatted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
