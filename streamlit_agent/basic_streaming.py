from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
import streamlit as st


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)
st.sidebar.image(url ="https://drive.google.com/file/d/1EcM_cJtGYrxErqLsYLqGBl6dzNKSsxF6/view?usp=sharing")
st.title(" :rainbow[Bienvenue sur le site des Chatbots de [Gpts-Index.com](https://gpts-index.com)]")
st.sidebar.title(" :green[differents modeles, differentes plateformes, des outils et des agents! :blue[Selectionnez vos préférence pour chaque attributs.]]")
with st.sidebar:
    openai_api_key = st.text_input(" :rainbow[inserrez votre cle API de OpenAI ou sinon [cliquez ici](https://platform.openai.com/api-keys) pour en obtenir une. Il es possible de choisir un autre modèle a partir d'autre plateforme.]", type="password")
    TOGETHER_API_KEY = st.text_input(" :rainbow[Inserrez votre cle API de Together.ai ou obtenez la gratuitement et avoir acces a plus de 100 modeles !! [Obtenir une cle API together.ai ici](https://api.together.xyz/settings/api-keys)]", type="password")
if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="Salut! Comment puis-je vous aider?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="utilisateur", content=prompt))
    st.chat_message("utilisateur").write(prompt)

    if not openai_api_key:
        st.info("Veuillez Inserrer votre clé API pour utiliser le Gpts-Index Chatbot")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
        response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
