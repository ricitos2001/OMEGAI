import time
import requests
import gradio as gr
from openai import OpenAI

MODELOS_DE_OPENROUTER = "https://openrouter.ai/api/v1/models"
URL="https://openrouter.ai/api/v1"
REQUEST_SUCESSFULL = 200

def obtener_modelos():
    respuesta = requests.get(MODELOS_DE_OPENROUTER)
    if respuesta.status_code == REQUEST_SUCESSFULL:
        return [modelo["id"] for modelo in respuesta.json().get("data", [])]
    else:
        raise Exception(respuesta.status_code)

def obtener_respuesta(modelo, api_key, prompt):
    client = OpenAI(base_url=URL, api_key=api_key)
    mensajes = [{"role": "assistant", "content": prompt}]
    respuesta = client.chat.completions.create(model=modelo, messages=mensajes)
    return respuesta.choices[0].message.content

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_message(history, message):
    for x in message["files"]:
        history.append({"role": "user", "content": {"path": x}})
    if message["text"] is not None:
        history.append({"role": "user", "content": message["text"]})
    return history, gr.MultimodalTextbox(value=None, interactive=False)

def bot(system_prompt, history, modelo, api_key):
    prompt = history[-1]["content"] if isinstance(history[-1]["content"], str) else "Archivo enviado."
    response = obtener_respuesta(modelo, api_key, (system_prompt+prompt))
    history.append({"role": "assistant", "content": ""})
    for character in response:
        history[-1]["content"] += character
        time.sleep(0.05)
        yield history

def main():
    with gr.Blocks() as demo:
        with gr.Tab("ejecución"):
            chatbot = gr.Chatbot(elem_id="chatbot", type="messages")
            chat_input = gr.MultimodalTextbox(interactive=True, file_count="multiple", placeholder="Enter message or upload file...", show_label=False)
        with gr.Tab("configuración"):
            modelo = gr.Dropdown(label="seleccionar modelo", choices=obtener_modelos())
            api_key = gr.Textbox(label="API-KEY")
            system_prompt = gr.TextArea(label="system-prompt")
        chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
        bot_msg = chat_msg.then(bot, [system_prompt, chatbot, modelo, api_key], chatbot, api_name="bot_response")
        bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])
        chatbot.like(print_like_dislike, None, None, like_user_message=True)
    demo.launch(share=False, debug=True, show_error=True)

if __name__ == "__main__":
    main()