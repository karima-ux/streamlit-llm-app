import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# .env を読む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def call_llm(role: str, user_text: str) -> str:
    if role == "営業コンサル":
        system_content = (
            "あなたは中小企業向けの営業・SaaS導入に詳しいコンサルタントです。"
            "専門用語はわかりやすく説明し、実行手順を具体的に提示してください。"
        )
    elif role == "クラウドエンジニア":
        system_content = (
            "あなたはAWSやPythonに詳しいクラウドエンジニアです。"
            "初心者にもわかるように、コード例とともに説明してください。"
        )
    else:
        system_content = "あなたは丁寧に説明するプロのアドバイザーです。"

    llm = ChatOpenAI(
        model="gpt-4o-mini",  # 講座に合わせて変えてOK
        temperature=0.4,
        openai_api_key=OPENAI_API_KEY,
    )

    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=user_text),
    ]

    response = llm.invoke(messages)
    return response.content


def main():
    st.set_page_config(page_title="LLMアプリ（Streamlit×LangChain）", page_icon="🤖")

    st.title("LLMアプリ（Streamlit×LangChain）")
    st.write(
        """
        このアプリは、入力したテキストをLLMに渡して回答を表示するデモです。  
        ラジオボタンで「どんな専門家として答えるか」を選んでから質問してください。  
        OpenAIのAPIキーは `.env` に記述しておき、アプリから自動で読み込む構成になっています。
        """
    )

    role = st.radio(
        "回答させる専門家を選んでください：",
        ("営業コンサル", "クラウドエンジニア"),
        horizontal=True,
    )

    user_text = st.text_area("質問や相談内容を入力してください：", height=150)

    if st.button("送信する"):
        if not user_text.strip():
            st.warning("テキストを入力してください。")
        else:
            try:
                answer = call_llm(role, user_text)
                st.subheader("回答：")
                st.write(answer)
            except Exception as e:
                st.error(f"LLM呼び出し中にエラーが発生しました: {e}")

    st.markdown("---")
    st.caption("使い方: ① 専門家を選ぶ ② テキストを書く ③ 送信 → 回答が下に出ます。")


if __name__ == "__main__":
    main()
