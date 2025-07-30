from flask import Blueprint, request, jsonify
from sqlalchemy import func
from db_model.food_nutrition_db import FoodNutritionDB
from db_model.raw_food_nutrition import RawFoodNutrition
from db_model.standard_nutrition import StandardNutrition
from utils import serialize_model

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/all', methods=['GET'])
def search_all_sources():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Query parameter "name" is required'}), 400

    limit = 15
    name_lower = name.lower()

    # ✅ 1. food_nutrition_db
    food_results = FoodNutritionDB.query.filter(
        func.lower(FoodNutritionDB.food_name).like(f'%{name_lower}%')
    ).limit(limit).all()

    remaining = limit - len(food_results)

    # ✅ 2. raw_food_nutrition
    raw_results = []
    if remaining > 0:
        raw_results = RawFoodNutrition.query.filter(
            func.lower(RawFoodNutrition.food_name).like(f'%{name_lower}%')
        ).limit(remaining).all()
        remaining -= len(raw_results)

    # ✅ 3. standard_nutrition
    standard_results = []
    if remaining > 0:
        standard_results = StandardNutrition.query.filter(
            func.lower(StandardNutrition.food_name).like(f'%{name_lower}%')
        ).limit(remaining).all()

    # 결과 합치기
    combined = food_results + raw_results + standard_results

    # 직렬화
    serialized = [serialize_model(item) for item in combined]

    return jsonify({
        'items': serialized,
        'count': len(serialized),
        'query': name
    })
