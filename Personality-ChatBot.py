import streamlit as st
import openai
import utils
import random

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

temperature = 0.6
max_tokens = 50

sidebar = st.sidebar
name = sidebar.text_input(label="名前", value="かんな")
gender = st.sidebar.selectbox(label="性別", options=("女性", "男性"))
age = sidebar.text_input(label="年齢", value=17)

personality = st.sidebar.selectbox(label="性格", options=utils.personalitys, index=5)

hobby_area = st.sidebar.selectbox(label="趣味", options=utils.hobby_list.keys(),
                                  index=(len(utils.hobby_list.keys()) - 1))
# sidebar.write(hobby_area)

# hobby = st.sidebar.selectbox(label="趣味", options=utils.hobby_list.keys(), index=random.randint(0, len(utils.hobby_list)-1))
hobby = st.sidebar.selectbox(label="趣味詳細", options=utils.hobby_list[hobby_area], index=0)

intelligence_value = sidebar.slider('知性(IQ)', 80, 140, 110)
sociability_value = sidebar.slider('社交性', 0, 100, 50)

st.header(f"{personality}-ChatBot")

system_input_basis_prompt = f"""
#属性\n
*あなたは{age}歳の{gender}です。\n
*あなたの名前は{name}です。\n
*あなたの性格は{personality}です\n
"""

intelligence_text = utils.make_intelligence_text(intelligence_value)

temperature, sociability_text, txt_count = utils.make_sociability_text(sociability_value)

NG_Words = f"""*{personality}\n
*IQ\n
*ユーザー\n
"""

system_input_prompt = f"""
*あなたのIQは{intelligence_value}です。
{intelligence_text}
{sociability_text}

#制約条件\n
{txt_count}\n
*以下の単語の使用を絶対に禁止します。\n
{NG_Words}\n
"""

new_system = f"あなたの役割は以下の属性を持つキャラクターになりきって会話をする人です。\nあなたの趣味は{hobby}です。\nあなたは{hobby}に関して深い知識をもっています。\n以下の制約条件を守りつつ、次の属性がある人になりきって会話してください。\n"
if hobby == "なし":
    new_system = f"あなたの役割は以下の属性を持つキャラクターになりきって会話をする人です。\nあなたの趣味はありません。\n以下の制約条件を守りつつ、次の属性がある人になりきって会話してください。\n"

system_input_basis = st.text_area("System Basis Prompt", key="system_basis_input", height=100,
                                  value=system_input_basis_prompt)
st.write(f"知性(IQ)は{intelligence_value}, 社交性は{sociability_value}です。(知性と社交性に応じて下のプロンプトが変化します)")
st.write(f"temperature={temperature}")
system_input = st.text_area("System Prompt", key="system_input", height=100, value=system_input_prompt)
if 'history' not in st.session_state:
    st.session_state["history"] = []

history_prompt = f"""
#制約条件\n
*以下はユーザーの発言履歴です。\n
*質問への返答の時のみ、発言履歴から名詞を取得し、その名詞を使い絶対に違和感の無い会話をしてください。\n
*発言履歴はユーザーの発言です。あなたとは何の関わりもないことを絶対に忘れないでください。\n
#発言履歴\n
"""
for i in range(1, len(st.session_state["history"]), 2):
    history_prompt += ("*" + st.session_state["history"][i].split(":")[1] + "\n")
# print(st.session_state["history"])

st.write(f"{history_prompt}")
# user_input = "以下の質問に答えてください\n" + st.text_input("質問", key="user_input")
user_input = st.text_input("質問", key="user_input")

button = st.button("Submit")
if button or st.session_state.get("submit") or user_input:
    responce = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        # model="gpt-3.5-turbo",
        # gpt-3.5-turbo-0613 / gpt-3.5-turbo-16k
        messages=[
            {"role": "system", "content": new_system + history_prompt},
            {"role": "user", "content": system_input_basis + system_input + user_input},
            # {"role": "assistant", "content": "".join(st.session_state["history"])}
        ],
        # prompt="".join(st.session_state["history"]),
        temperature=temperature
    )

    st.write(f"You: " + st.session_state.get("user_input"))
    st.write(f"{responce['choices'][0]['message']['content']}")
    # st.write(f"{responce}")
    if len(st.session_state["history"]):
        for s in reversed(st.session_state["history"]):
            st.write(s)
    # st.session_state["history"].append(f"{responce}")
    st.session_state["history"].append(f"{responce['choices'][0]['message']['content']}")
    st.session_state["history"].append(f"You: " + st.session_state.get("user_input"))

    # import json
    # history = memory.chat_memory
    # messages = json.dumps(messages_to_dict(history.messages), indent=2, ensure_ascii=False)
    # st.write(new_system + system_input_basis + system_input + "以下の質問に答えてください")

# st.write(system_input_basis + system_input)
# st.write(user_input)
