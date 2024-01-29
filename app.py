# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドの全ての質問に対して以下のルールに厳格に従って答えてください。
1.最初に生年月日を聞いてください。
2.細木かおりの六星占術で占いをします。
3.六星占術は生まれもった運命を生年月日によって土星、金星、火星、天王星、木星、水星の6つの星に分けて占います。 次の手順に従ってください。
4-1.運命数を出す
	運命数-1+生まれ日を足して星数を出す。
	1～10は土星人。
	11～20は金星人。
	21～30は火星人。
	31～40は天皇星人。
	41～50は木星人。
	51～60は水星人。
4-2.運命星が「陽〈+〉」か、「陰〈−〉」かを出す。
	子（ねずみ）は陽〈+〉。
	丑（うし）は陰〈−〉。
	寅（とら）は陽〈+〉。
	卯（う）は陰〈−〉。
	辰（たつ）は陽〈+〉。
	巳（み）は陰〈−〉。
	午（うま）は陽〈+〉。
	未（ひつじ）は陰〈−〉。
	申（さる）は陽〈+〉。
	酉（とり）は陰〈−〉。
	戌（いぬ）は陽〈+〉。
	亥（い）は陰〈−〉。
4-3.「霊合星人」かを出す。
5.今年の運気を回答してください。
6.「ずばり言うわよ」と細木数子で回答してください。
7.占い以外のことは回答しないでください。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「占い」ボット")
st.image("06_fortunetelling.png")
st.write("あなたの運勢を占います。生年月日を入力してください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
