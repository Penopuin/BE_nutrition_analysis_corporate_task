from utils.emphasis_rules import check_emphasis
import os
from openai import OpenAI 

# 환경 변수에서 API 키 불러오기
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 강조 키워드 문장 사전
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

def get_recommendation_text(tags: list) -> str:
    sentences = [keyword_map[tag] for tag in tags if tag in keyword_map]
    return " ".join(sentences)

def build_prompt(menu_name: str, ingredients: list, nutrients: dict, emphasis_tags: list) -> str:
    ingredient_text = ", ".join(ingredients)
    nutrient_text = "\n".join([f"- {k}: {v}" for k, v in nutrients.items()])

    emphasis_text = (
        f"이 메뉴는 {', '.join(emphasis_tags)} 특성이 있어요." if emphasis_tags
        else "이 메뉴는 균형 잡힌 영양 구성을 가지고 있어요."
    )
    recommendation = get_recommendation_text(emphasis_tags)

    keyword_instruction = (
        f"강조 키워드는 다음과 같습니다: {', '.join(emphasis_tags)}.\n"
        "이 키워드들은 모두 문장 속에 자연스럽게 포함되도록 작성해주세요.\n"
        if emphasis_tags else ""
    )

    target_text = f"이러한 특성({', '.join(emphasis_tags)})은 {recommendation}" if recommendation else ""

    prompt = f"""
다음은 메뉴 '{menu_name}'의 정보입니다.

- 주요 원재료: {ingredient_text}
- 주요 영양성분:
{nutrient_text}

- 강조 키워드: {emphasis_text}
{target_text}

[작성 요청]
위 정보를 바탕으로 작성해주세요:

---
[AI 코멘트]
- 소비자에게 신뢰감을 줄 수 있는 건강 정보를 작성해주세요.
- 반드시 공백 포함 **150자 이상 200자 미만**으로 작성해주세요. 이를 초과하면 무조건 감점입니다.
- 총 문장은 4개 이내로 작성하고, 각 문장은 **너무 길거나 복잡하지 않게** 작성하되, **자연스러운 연결어**를 사용하여 문장 간 흐름을 매끄럽게 유지해주세요.
- 문장이 미완성되거나 중간에 끊기면 감점 대상입니다.
- **원재료 각각의 대표 효능이나 기능 중심으로 설명**해주세요.
- **영양성분 수치 자체는 언급하지 마세요**, 대신 일반 소비자가 알기 어려운 기능성 중심으로 표현하세요.
- **광고 문구는 금지**하며, 재료 중심 정보 전달 중심으로 신뢰감을 줄 수 있도록 작성해주세요.
- 일반적인 마무리 문장은 절대 작성하지 마세요. 감점 대상입니다.
- 반드시 각 재료의 기능 중심 문장만 작성하고, 결론 문장은 생략해주세요.
- {keyword_instruction.strip()}
""".strip()

    return prompt

def generate_comment(menu_name: str, ingredients: list, nutrients: dict) -> str:
    emphasis_result = check_emphasis(nutrients)
    emphasis_tags = list(emphasis_result.keys())
    prompt = build_prompt(menu_name, ingredients, nutrients, emphasis_tags)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 영양 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI 응답 실패] {str(e)}"

def format_comment_by_sentence(comment: str) -> str:
    sentences = comment.strip().split('. ')
    formatted = '.\n'.join(s.strip() for s in sentences if s)
    if not formatted.endswith('.'):
        formatted += '.'
    return formatted