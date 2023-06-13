import json

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

NG_words = """
#制約条件
*以下の単語の使用を禁止します
*ユーザー
*ロールプレイ
*役割
*IQ
*社交性
*理論的
*客観的
*20文字
*知性
*友人
*口数
*社交性
*フレンドリー
*カジュアル
*自然
*雑談
*男性
*女性
*INTJ
*内省的
*独立
*性格
*INTP
*ENTJ
*ENTP
*INFJ
*INFP
*想像力
*感情
*創造的
*アイデア
*ENFJ
*ENFP
*ISTJ
*ISFJ
*ESTJ
*ESFJ
*ISTP
*ISFP
*ESTP
*ESFP
"""


def make_intelligence_text(intelligence_value):
    if intelligence_value > 120:
        return "*あなたは上手に会話をします。"
    elif intelligence_value > 95:
        return "*自然に会話をしてください。"
    else:
        return "*あなたの返答は要領の悪い返答です。\n*あなたは小学3年生程度の単語のみを使用します。"
        # return "あなたは小学3年生程度の単語のみを使用します。"


def make_sociability_text(sociability_value):
    if sociability_value > 70:
        temperature = 0.5
        sociability = "*あなたはユーザーに友好的です。\n"
        txt_count = "*会話内容は60文字以内です。"
        return temperature, sociability, txt_count
    elif sociability_value > 35:
        temperature = 0.6
        sociability = "*ユーザーと特別な関係はありません。\n"
        txt_count = "*会話内容は40文字以内です。"
        return temperature, sociability, txt_count
    else:
        temperature = 0.2
        sociability = "*あなたは口数が少ないです。\n*あなたは自己中心的です。\n*あなたは会話が嫌いです。\n"
        txt_count = "*会話内容は絶対に20文字以内です。"
        return temperature, sociability, txt_count


tf = open("hobbies.json", "r")
hobby_list = json.load(tf)
