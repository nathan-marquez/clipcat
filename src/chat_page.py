# visualization_page.py
import streamlit as st
import plotly.graph_objs as go
import json
from openai import OpenAI
from utils.rag_query import rag_query


openai_api_key = "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"


def show_chat():
    st.title("💬 Clip Chat")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        rag_prompt = rag_query(prompt)
        st.chat_message("user").write(prompt)

        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=st.session_state.messages
            + [{"role": "user", "content": rag_prompt}],
        )
        st.session_state.messages.append({"role": "user", "content": prompt})
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
