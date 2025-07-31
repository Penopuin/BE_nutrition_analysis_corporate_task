import openai
import os
from dotenv import load_dotenv

load_dotenv()

GPT_KEY = os.getenv('GPT_KEY')

openai.api_key = GPT_KEY  # 실제 사용 시 보안 관리 필요

# 강조 키워드에 따른 추천 대상 문장 생성
def get_recommendation_text(tags: list) -> str:
    keyword_map = {
    "저칼로리": "저칼로리 메뉴라 체중 조절이나 다이어트 중인 분들께 좋아요.",
    "저지방": "저지방 메뉴로 지방 섭취를 줄이고 싶은 분들께 도움이 됩니다.",
    "無지방": "지방이 거의 없어 가볍고 건강하게 즐길 수 있는 메뉴예요.",
    "저포화지방": "저포화지방 식단이라 심혈관 건강을 염두에 두시는 분들께도 좋아요.",
    "無포화지방": "포화지방이 거의 없어 심혈관 건강을 걱정하는 분들께 적합합니다.",
    "저트랜스지방": "트랜스지방이 낮아 건강한 식습관을 유지하고 싶은 분들께도 잘 맞아요.",
    "저콜레스테롤": "저콜레스테롤 식단으로 혈중 콜레스테롤이 걱정되는 분들께 권할 수 있어요.",
    "無콜레스테롤": "콜레스테롤이 거의 없어 부담 없이 섭취하실 수 있어요.",
    "無당류": "당류가 거의 없어 혈당 걱정 없이 즐길 수 있는 메뉴예요.",
    "저당류": "저당류 식단으로 당 섭취를 줄이고 싶은 분들께 알맞습니다.",
    "저나트륨": "저나트륨 식단으로 짠 음식을 피하고 싶은 분들께도 부담 없이 적합해요.",
    "無나트륨": "나트륨이 거의 없어 염분 섭취를 제한하는 분들께도 안심이 되는 메뉴예요.",
    "식이섬유 함유": "식이섬유가 함유되어 있어 장운동 촉진과 포만감에 도움을 줄 수 있어요.",
    "식이섬유 풍부": "식이섬유가 풍부해 장 건강과 포만감 유지에 효과적이에요.",
    "고단백": "고단백 식단으로 구성되어 있어 근육 유지나 운동 후 회복에 도움을 줄 수 있어요.",
    "비타민B6 함유": "비타민 B6가 함유되어 에너지 대사와 피로 회복에 도움을 줄 수 있어요.",
    "비타민B6 풍부": "비타민 B6가 풍부해 신경 기능과 활력 유지에 유익합니다.",
    "비타민B12 함유": "비타민 B12가 함유되어 신경 건강이나 혈액 생성에 도움을 줄 수 있어요.",
    "비타민B12 풍부": "비타민 B12가 풍부해 채식 위주의 식단을 보완하는 데 유익합니다.",
    "비타민C 함유": "비타민 C가 함유되어 피로 회복이나 면역력 강화에 좋습니다.",
    "비타민C 풍부": "비타민 C가 풍부해 감기 예방이나 항산화에 도움을 줄 수 있어요.",
    "비타민D 함유": "비타민 D가 함유되어 뼈 건강과 면역력 유지에 도움이 됩니다.",
    "비타민D 풍부": "비타민 D가 풍부해 햇빛 부족이 걱정되는 분들께 좋습니다.",
    "비타민E 함유": "비타민 E가 함유되어 있어 항산화 작용을 기대할 수 있어요.",
    "비타민E 풍부": "비타민 E가 풍부해 노화 방지나 세포 보호에 관심 있는 분들께 유익합니다.",
    "비타민K 함유": "비타민 K가 함유되어 뼈 대사와 혈액 응고에 도움이 될 수 있어요.",
    "비타민K 풍부": "비타민 K가 풍부해 뼈 건강을 신경 쓰는 분들께 유익합니다.",
    "칼슘 함유": "칼슘이 함유되어 있어 뼈 건강을 신경 쓰는 분들께 추천할 수 있어요.",
    "칼슘 풍부": "칼슘이 풍부해 뼈 건강이나 성장기 영양에 도움이 될 수 있어요.",
    "철분 함유": "철분이 함유되어 있어 피로 개선이나 빈혈 예방에도 유익해요.",
    "철분 풍부": "철분이 풍부해 철분 보충이 필요한 분들께 추천돼요.",
    "아연 함유": "아연이 함유되어 면역력 향상에 도움이 될 수 있어요.",
    "아연 풍부": "아연이 풍부해 피부 건강이나 면역력 관리에 유익합니다."
}
    sentences = [keyword_map[tag] for tag in tags if tag in keyword_map]
    return " ".join(sentences)

# 강조 키워드 자동 추출
def get_emphasis_tags(nutrients: dict) -> list:
    tags = []

    g = nutrients.get("제공량(g)", 0)
    ml = nutrients.get("밀리리터(ml)", 0)
    kcal = nutrients.get("에너지(kcal)", 0)
    carbs = nutrients.get("탄수화물(g)", 0)
    sugar = nutrients.get("당류(g)", 0)
    protein = nutrients.get("단백질(g)", 0)
    fat = nutrients.get("지방(g)", 0)
    sat_fat = nutrients.get("포화지방(g)", 0)
    trans_fat = nutrients.get("트랜스지방(g)", 0)
    cholesterol = nutrients.get("콜레스테롤(mg)", 0)
    sodium = nutrients.get("나트륨(mg)", 0)
    fiber = nutrients.get("식이섬유(g)", 0)
    calcium = nutrients.get("칼슘(mg)", 0)
    iron = nutrients.get("철분(mg)", 0)
    zinc = nutrients.get("아연(mg)", 0)
    vit_a = nutrients.get("비타민 A(μg)", 0)
    vit_b6 = nutrients.get("비타민 B6(mg)", 0)
    vit_b12 = nutrients.get("비타민 B12(μg)", 0)
    vit_c = nutrients.get("비타민 C(mg)", 0)
    vit_d = nutrients.get("비타민 D(μg)", 0)
    vit_e = nutrients.get("비타민 E(mg)", 0)
    vit_k = nutrients.get("비타민 K(μg)", 0)

    if (g > 0 and (kcal / g) * 100 < 40) or (ml > 0 and (kcal / ml) * 100 < 20):
        tags.append("저칼로리")

    if (g > 0 and (fat / g) * 100 < 3) or (ml > 0 and (fat / ml) * 100 < 1.5):
        tags.append("저지방")

    if (g > 0 and (fat / g) * 100 < 0.5) or (ml > 0 and (fat / ml) * 100 < 0.5):
        tags.append("無지방")

    low_sat_fat = False
    if g > 0 and (sat_fat / g) * 100 < 1.5:
        low_sat_fat = True
    if ml > 0 and (sat_fat / ml) * 100 < 0.75:
        low_sat_fat = True

    sat_fat_ratio = (sat_fat * 9 / kcal) if kcal > 0 else 0

    if low_sat_fat and sat_fat_ratio < 0.1:
        tags.append("저포화지방")

    no_sat_fat = False
    if g > 0 and (sat_fat / g) * 100 < 0.1:
        no_sat_fat = True
    if ml > 0 and (sat_fat / ml) * 100 < 0.1:
        no_sat_fat = True

    if no_sat_fat:
        tags.append("無포화지방")

    if g > 0 and (trans_fat / g) * 100 < 0.5:
        tags.append("저트랜스지방")

    is_low_cholesterol = False

    if g > 0 and (cholesterol / g) * 100 < 20:
        is_low_cholesterol = True
    if ml > 0 and (cholesterol / ml) * 100 < 10:
        is_low_cholesterol = True

    is_low_sat_fat = False
    if g > 0 and (sat_fat / g) * 100 < 1.5:
        is_low_sat_fat = True
    if ml > 0 and (sat_fat / ml) * 100 < 0.75:
        is_low_sat_fat = True

    sat_fat_ratio = (sat_fat * 9 / kcal) if kcal > 0 else 0

    if is_low_cholesterol and is_low_sat_fat and sat_fat_ratio < 0.1:
        tags.append("저콜레스테롤")

    low_chol = False
    if g > 0 and (cholesterol / g) * 100 < 5:
        low_chol = True
    if ml > 0 and (cholesterol / ml) * 100 < 5:
        low_chol = True

    sat_fat_ratio = (sat_fat * 9 / kcal) if kcal > 0 else 0

    if low_chol and sat_fat_ratio < 0.1:
        tags.append("無콜레스테롤")

    no_sugar = False
    if g > 0 and (sugar / g) * 100 < 0.5:
        no_sugar = True
    if ml > 0 and (sugar / ml) * 100 < 0.5:
        no_sugar = True

    if no_sugar:
        tags.append("無당류")

    low_sugar = False
    if g > 0 and (sugar / g) * 100 < 5:
        low_sugar = True
    if ml > 0 and (sugar / ml) * 100 < 2.5:
        low_sugar = True

    if low_sugar:
        tags.append("저당류")

    if g > 0 and (sodium / g) * 100 < 120:
        tags.append("저나트륨")

    if g > 0 and (sodium / g) * 100 < 5:
        tags.append("無나트륨")

    fiber_contained = False
    if g > 0 and (fiber / g) * 100 >= 3:
        fiber_contained = True
    if kcal > 0 and (fiber / kcal) * 100 >= 1.5:
        fiber_contained = True

    if fiber_contained:
        tags.append("식이섬유 함유")

    fiber_high = False
    if g > 0 and (fiber / g) * 100 >= 6:
        fiber_high = True
    if kcal > 0 and (fiber / kcal) * 100 >= 3:
        fiber_high = True

    if fiber_high:
        tags.append("식이섬유 풍부")

    high_protein = False
    if g > 0 and (protein / g) * 100 >= 10:
        high_protein = True
    if kcal > 0 and (protein / kcal) * 100 >= 5:
        high_protein = True

    if high_protein:
        tags.append("고단백")

    b6_high = False
    if g > 0 and (vit_b6 / g) * 100 >= 0.45:
        b6_high = True
    if ml > 0 and (vit_b6 / ml) * 100 >= 0.225:
        b6_high = True
    if kcal > 0 and (vit_b6 / kcal) * 100 >= 0.15:
        b6_high = True

    if b6_high:
        tags.append("비타민 B6 풍부")

    b6_contained = False
    if g > 0 and (vit_b6 / g) * 100 >= 0.225:
        b6_contained = True
    if ml > 0 and (vit_b6 / ml) * 100 >= 0.1125:
        b6_contained = True
    if kcal > 0 and (vit_b6 / kcal) * 100 >= 0.075:
        b6_contained = True

    if b6_contained:
        tags.append("비타민 B6 함유")


    b12_high = False
    if g > 0 and (vit_b12 / g) * 100 >= 0.72:
        b12_high = True
    if ml > 0 and (vit_b12 / ml) * 100 >= 0.36:
        b12_high = True
    if kcal > 0 and (vit_b12 / kcal) * 100 >= 0.24:
        b12_high = True

    if b12_high:
        tags.append("비타민 B12 풍부")


    b12_contained = False
    if g > 0 and (vit_b12 / g) * 100 >= 0.36:
        b12_contained = True
    if ml > 0 and (vit_b12 / ml) * 100 >= 0.18:
        b12_contained = True
    if kcal > 0 and (vit_b12 / kcal) * 100 >= 0.12:
        b12_contained = True

    if b12_contained:
        tags.append("비타민 B12 함유")

    vitc_high = False
    if g > 0 and (vit_c / g) * 100 >= 30:
        vitc_high = True
    if ml > 0 and (vit_c / ml) * 100 >= 15:
        vitc_high = True
    if kcal > 0 and (vit_c / kcal) * 100 >= 10:
        vitc_high = True

    if vitc_high:
        tags.append("비타민 C 풍부")

    vitc_contained = False
    if g > 0 and (vit_c / g) * 100 >= 15:
        vitc_contained = True
    if ml > 0 and (vit_c / ml) * 100 >= 7.5:
        vitc_contained = True
    if kcal > 0 and (vit_c / kcal) * 100 >= 5:
        vitc_contained = True

    if vitc_contained:
        tags.append("비타민 C 함유")


    vitd_high = False
    if g > 0 and (vit_d / g) * 100 >= 3.0:
        vitd_high = True
    if ml > 0 and (vit_d / ml) * 100 >= 1.5:
        vitd_high = True
    if kcal > 0 and (vit_d / kcal) * 100 >= 1.0:
        vitd_high = True

    if vitd_high:
        tags.append("비타민 D 풍부")

    vitd_contained = False
    if g > 0 and (vit_d / g) * 100 >= 1.5:
        vitd_contained = True
    if ml > 0 and (vit_d / ml) * 100 >= 0.75:
        vitd_contained = True
    if kcal > 0 and (vit_d / kcal) * 100 >= 0.5:
        vitd_contained = True

    if vitd_contained:
        tags.append("비타민 D 함유")

    vite_high = False
    if g > 0 and (vit_e / g) * 100 >= 3.3:
        vite_high = True
    if ml > 0 and (vit_e / ml) * 100 >= 1.65:
        vite_high = True
    if kcal > 0 and (vit_e / kcal) * 100 >= 1.1:
        vite_high = True

    if vite_high:
        tags.append("비타민 E 풍부")

    vite_contained = False
    if g > 0 and (vit_e / g) * 100 >= 1.65:
        vite_contained = True
    if ml > 0 and (vit_e / ml) * 100 >= 0.825:
        vite_contained = True
    if kcal > 0 and (vit_e / kcal) * 100 >= 0.55:
        vite_contained = True

    if vite_contained:
        tags.append("비타민 E 함유")

    vitk_contained = False
    if g > 0 and (vit_k / g) * 100 >= 10.5:
        vitk_contained = True
    if ml > 0 and (vit_k / ml) * 100 >= 5.25:
        vitk_contained = True
    if kcal > 0 and (vit_k / kcal) * 100 >= 3.5:
        vitk_contained = True

    if vitk_contained:
        tags.append("비타민 K 함유")

    vitk_high = False
    if g > 0 and (vit_k / g) * 100 >= 21.0:
        vitk_high = True
    if ml > 0 and (vit_k / ml) * 100 >= 10.5:
        vitk_high = True
    if kcal > 0 and (vit_k / kcal) * 100 >= 7.0:
        vitk_high = True

    if vitk_high:
        tags.append("비타민 K 풍부")

    calcium_contained = False
    if g > 0 and (calcium / g) * 100 >= 105:
        calcium_contained = True
    if ml > 0 and (calcium / ml) * 100 >= 52.5:
        calcium_contained = True
    if kcal > 0 and (calcium / kcal) * 100 >= 35:
        calcium_contained = True

    if calcium_contained:
        tags.append("칼슘 함유")

    calcium_high = False
    if g > 0 and (calcium / g) * 100 >= 210:
        calcium_high = True
    if ml > 0 and (calcium / ml) * 100 >= 105:
        calcium_high = True
    if kcal > 0 and (calcium / kcal) * 100 >= 70:
        calcium_high = True

    if calcium_high:
        tags.append("칼슘 풍부")


    iron_contained = False
    if g > 0 and (iron / g) * 100 >= 1.8:
        iron_contained = True
    if ml > 0 and (iron / ml) * 100 >= 0.9:
        iron_contained = True
    if kcal > 0 and (iron / kcal) * 100 >= 0.6:
        iron_contained = True

    if iron_contained:
        tags.append("철분 함유")

    iron_high = False
    if g > 0 and (iron / g) * 100 >= 3.6:
        iron_high = True
    if ml > 0 and (iron / ml) * 100 >= 1.8:
        iron_high = True
    if kcal > 0 and (iron / kcal) * 100 >= 1.2:
        iron_high = True

    if iron_high:
        tags.append("철분 풍부")


    zinc_contained = False
    if g > 0 and (zinc / g) * 100 >= 1.275:
        zinc_contained = True
    if ml > 0 and (zinc / ml) * 100 >= 0.6375:
        zinc_contained = True
    if kcal > 0 and (zinc / kcal) * 100 >= 0.425:
        zinc_contained = True

    if zinc_contained:
        tags.append("아연 함유")

    zinc_high = False
    if g > 0 and (zinc / g) * 100 >= 2.55:
        zinc_high = True
    if ml > 0 and (zinc / ml) * 100 >= 1.275:
        zinc_high = True
    if kcal > 0 and (zinc / kcal) * 100 >= 0.85:
        zinc_high = True

    if zinc_high:
        tags.append("아연 풍부")

    return deduplicate_tags(tags)

def deduplicate_tags(tags: list) -> list:
    # 중복 제거 우선순위 그룹 정의
    priority_groups = [
        ["지방無", "저지방"],
        ["無포화지방", "저포화지방"],
        ["無콜레스테롤", "저콜레스테롤"],
        ["無당류", "저당류"],
        ["無나트륨", "저나트륨"],
        ["식이섬유 풍부", "식이섬유 함유"],
        ["비타민 B6 풍부", "비타민 B6 함유"],
        ["비타민 B12 풍부", "비타민 B12 함유"],
        ["비타민 C 풍부", "비타민 C 함유"],
        ["비타민 D 풍부", "비타민 D 함유"],
        ["비타민 E 풍부", "비타민 E 함유"],
        ["비타민 K 풍부", "비타민 K 함유"],
        ["칼슘 풍부", "칼슘 함유"],
        ["철분 풍부", "철분 함유"],
        ["아연 풍부", "아연 함유"]
    ]

    final_tags = tags.copy()
    for group in priority_groups:
        for tag in group:
            if tag in final_tags:
                # 그룹 내에서 우선순위 높은 첫 번째 항목만 남기고 나머지 제거
                final_tags = [t for t in final_tags if t not in group or t == tag]
                break
    return final_tags

def build_prompt(menu_name: str, ingredients: list, nutrients: dict, emphasis_tags: list) -> str:
    ingredient_text = ", ".join(ingredients)
    nutrient_text = "\n".join([f"- {k}: {v}" for k, v in nutrients.items()])
    emphasis_text = ", ".join(emphasis_tags) if emphasis_tags else "균형 잡힌 영양 구성"

    prompt = f"""
[메뉴 정보]
- 메뉴명: {menu_name}
- 주요 원재료: {ingredient_text}
- 주요 영양성분:
{nutrient_text}

[영양적 특성]
- 강조 키워드: {emphasis_text}

[작성 요청]
위 정보를 바탕으로 소비자에게 신뢰감을 줄 수 있는 **건강 코멘트**를 작성해주세요.

[작성 조건]
1. 공백 포함 **250자 이상, 300자 이내**로 작성해주세요.
2. 문장은 **1~2문장 이내**로 구성하되, 각 문장은 자연스럽게 연결되도록 작성해주세요.
3. **원재료 각각의 대표 효능이나 기능을 중심으로 설명**해주세요.
   예: 귀리는 콜레스테롤 개선, 브로콜리는 항산화 효과, 닭가슴살은 고단백 식품 등
4. **영양성분 수치 자체에 집중하지 말고**, 일반 소비자가 알기 어려운 **기능 중심**으로 작성해주세요.
5. 사용할 수 있는 강조 키워드는 다음과 같습니다:
   {emphasis_text}
6. 강조 키워드들은 **문장 속에 자연스럽게 포함만 시켜주세요. 절대 별도로 한 문장에 몰아서 나열하지 마세요.**
   - 강조 키워드: {', '.join(emphasis_tags)}
7. {emphasis_text} 목록에 없는 유사 키워드나 의미가 비슷한 표현도 모두 사용 금지입니다.
8. **광고 문구는 절대 사용하지 마세요. 설명 중심의 신뢰감 있는 문장**으로 작성해주세요.

[작성 예시]
예시1) 닭가슴살은 단백질이 풍부하여 운동 후 회복에 도움이 됩니다. 또한 무지방 식단으로 지방 섭취를 줄이고 싶은 분들께도 적합해요.

예시2) 브로콜리와 방울토마토는 항산화 성분이 풍부해 면역력 강화에 도움이 됩니다. 이 샐러드는 고단백, 무나트륨 식단으로 건강한 식사를 원하시는 분들께 추천드려요.
""".strip()

    return prompt



# GPT API 호출
def generate_comment(menu_name, ingredients, nutrients):
    emphasis_tags = get_emphasis_tags(nutrients)
    prompt = build_prompt(menu_name, ingredients, nutrients, emphasis_tags)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    return response["choices"][0]["message"]["content"].strip()

# 문장 단위 줄바꿈 포맷팅 함수 (이미 있음)
def format_comment_by_sentence(comment: str) -> str:
    sentences = comment.strip().split('. ')
    formatted = '.\n'.join(s.strip() for s in sentences if s)
    if not formatted.endswith('.'):
        formatted += '.'
    return formatted

