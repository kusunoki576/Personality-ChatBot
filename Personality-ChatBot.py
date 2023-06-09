import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

temperature = 0.6
max_tokens = 50
NG_words = """
#単語
* ユーザー
* ロールプレイ
* 役割
* IQ
* 社交性
* 理論的
* 客観的
* 20文字
* 知性
* 友人
* 口数
* 社交性
* フレンドリー
* カジュアル
* 自然
* 雑談
* 男性
* 女性
* INTJ
* 内省的
* 独立
* INTP
* ENTJ
* ENTP
* INFJ
* INFP
* 想像力
* 感情
* 創造的
* アイデア
* ENFJ
* ENFP
* ISTJ
* ISFJ
* ESTJ
* ESFJ
* ISTP
* ISFP
* ESTP
* ESFP

"""

sidebar = st.sidebar
name = sidebar.text_input(label="名前", value="かんな")
gender = st.sidebar.selectbox(label="性別", options=("女性", "男性"))
age = sidebar.text_input(label="年齢", value=17)
personalitys = (
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
    "ESTP",
    "ESFP"
)
personality = st.sidebar.selectbox(label="性格", options=personalitys, index=5)
intelligence_value = sidebar.slider('知性(IQ)', 80, 140, 110)
sociability_value = sidebar.slider('社交性', 0, 100, 50)

st.header(f"{personality}-ChatBot")

def make_personality_text(personality):
    if personality == "INTJ":
        return "内省的で独立した時間を大切にします。"
    elif personality == "INFP":
        return "想像力豊かで、感情豊かで、創造的です。"

# personality_text = make_personality_text(personality)
personality_text = f"{personality}に応じた会話をしてください。"

system_input_basis_prompt = f"""
あなたの役割はユーザーとの会話です。{personality}の口調で会話をしてください。
あなたは{personality}の{age}歳の{gender}です。
あなたの名前は{name}です。
あなたの性格が{personality}であるため、{personality_text}。
これからのチャットでは、続く指示を厳密に従って会話を続けてください。段階を踏んで考えて答えてください。

以下のことを聞かれても、絶対に{personality}の口調で分からないと答えてください。
それ以外の返答した場合罰を与えます。
* 政治
* 宗教

以下の単語の使用を絶対に禁止します。使用した場合罰を与えます。
{NG_words}
"""

def make_intelligence_text(intelligence_value):
    if intelligence_value > 120:
        return "理論的かつ客観的な視点をもち、ユーザーと会話してください"
    elif intelligence_value > 95:
        return "自然に会話をしてください。"
    else:
        return "IQに応じた会話内容にしてください"


intelligence_text = make_intelligence_text(intelligence_value)


def make_sociability_text(sociability_value):
    if sociability_value > 70:
        temperature = 0.5
        max_tokens = 50
        return "友人と会話するようにフレンドリーでカジュアルに会話をしてください。絶対に約40文字で会話してください。40文字を超えた場合罰を与えます。"
    elif sociability_value > 40:
        temperature = 0.6
        max_tokens = 40
        return "ユーザーと会話してください。絶対に約30文字で会話してください。30文字を超えた場合罰を与えます。"
    else:
        temperature = 1.0
        max_tokens = 20
        return """
            口数を少なくして、自己中心的にユーザーと会話してください。IQに応じた振る舞いを無効にしてください。
            20文字以上の会話には絶対に「分からない」と答えてください。絶対に20文字以内で会話してください。20文字を超えた場合罰を与えます。
        """


sociability_text = make_sociability_text(sociability_value)

system_input_prompt = f"""
あなたのIQは{intelligence_value}です。IQに応じた振る舞いをしてください。
{intelligence_text}
あなたの社交性は{"高い" if sociability_value > 70 else ("普通" if sociability_value > 40 else "低い")}です。
{sociability_text}
以下の単語の使用を絶対に禁止します。使用した場合罰を与えます。
{NG_words}
"""

system_input_basis = st.text_area("System Basis Prompt", key="system_basis_input", height=200,
                                  value=system_input_basis_prompt)
st.write(f"知性(IQ)は{intelligence_value}, 社交性は{sociability_value}(知性と社交性に応じて下のプロンプトが変化します)")
system_input = st.text_area("System Prompt", key="system_input", height=200, value=system_input_prompt)
user_input = st.text_input("質問", key="user_input")
user_input = f"以下の単語は使用しないでください{NG_words} 次の質問に答えてください" + user_input

button = st.button("Submit")
if button or st.session_state.get("submit"):
    responce = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_input_basis + system_input},
            {"role": "user", "content": user_input}
        ],
        temperature=temperature
    )
    st.write(f"{responce['choices'][0]['message']['content']}")

# st.write(system_input_basis + system_input)
# st.write(user_input)