import streamlit as st
import openai
import utils

# openai.api_key = st.secrets.OpenAIAPI.openai_api_key


temperature = 0.6
max_tokens = 50

sidebar = st.sidebar
name = sidebar.text_input(label="名前", value="かんな")
gender = st.sidebar.selectbox(label="性別", options=("女性", "男性"))
age = sidebar.text_input(label="年齢", value=17)

personality = st.sidebar.selectbox(label="性格", options=utils.personalitys, index=5)
intelligence_value = sidebar.slider('知性(IQ)', 80, 140, 110)
sociability_value = sidebar.slider('社交性', 0, 100, 50)

st.header(f"{personality}-ChatBot")

system_input_basis_prompt = f"""
#属性
*あなたは{age}歳の{gender}です。
*あなたの名前は{name}です。
*あなたの性格は{personality}です
"""

intelligence_text = utils.make_intelligence_text(intelligence_value)

temperature, sociability_text, txt_count = utils.make_sociability_text(sociability_value)

NG_Words = f"""*{personality}
*IQ
*User
"""

system_input_prompt = f"""
*あなたのIQは{intelligence_value}です。
{sociability_text}

#制約条件
{txt_count}
*以下の単語の使用を絶対に禁止します。
{NG_Words}
"""

system_input_basis = st.text_area("System Basis Prompt", key="system_basis_input", height=200, value=system_input_basis_prompt)
st.write(f"知性(IQ)は{intelligence_value}, 社交性は{sociability_value}です。(知性と社交性に応じて下のプロンプトが変化します)")
st.write(f"temperature={temperature}")
system_input = st.text_area("System Prompt", key="system_input", height=200, value=system_input_prompt)
st.write(f"システムには次の命令が与えられています:\n \"あなたはキャラクターになりきって会話をする人です。以下の制約条件を守りつつ、次の属性がある人になりきって会話してください。\"")
user_input = "以下の質問に答えてください\n" + st.text_input("質問", key="user_input")

button = st.button("Submit")
if button or st.session_state.get("submit"):
    responce = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはキャラクターになりきって会話をする人です。以下の制約条件を守りつつ、次の属性がある人になりきって会話してください。"},
            {"role": "user", "content": system_input_basis + system_input + user_input}
        ],
        temperature=temperature
    )
    st.write(f"{responce['choices'][0]['message']['content']}")

# st.write(system_input_basis + system_input)
# st.write(user_input)
