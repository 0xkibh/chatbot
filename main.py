import os
import openai
import gradio as gr

from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.environ.get(
    "APIKEY"
)  # setup your key as APIKEY = "your-key" in .env file

# or you can simply give the apikey as string as
# openai.api_key = "your-key"

start_sequence = "AI:"
restart_sequence = "Human: "


def resetchat():
    """Function to reset the chat history and prompt

    Returns:
        tuple: chatbot, state and message
    """
    with open("prompts.txt", "w") as f:
        f.write(
            "The following is a conversation with an AI assistant.The assistant is helpful, creative, clever, and very friendly.\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"
        )
    return [], [], ""


def chatkbt(txt, history):
    """Function to take the state and message and return state with additional chat

    Args:
        txt (str): The text in the input box
        history (list): The list of tuples containing the chat history of AI and Human

    Returns:
        tuple: chatbot, state and message
    """
    prompt = ""
    with open("prompts.txt", "r") as f:
        prompt = f.read()
    history = history or []
    prompt_ = "\nHuman: {} \nAI: ".format(txt)

    prompt += prompt_

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
    )

    prompt_ += response.choices[0].text.strip()

    history.append((txt, response.choices[0].text.strip()))

    with open("prompts.txt", "a") as f:
        f.write(prompt_)
    return history, history, ""


block = gr.Blocks()


with block:
    gr.Markdown(
        """<h1><center>CHAT KBT</center></h1>
    """
    )
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="", value="")
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatkbt, inputs=[message, state], outputs=[chatbot, state, message])
    submit = gr.Button("RESET CHAT")
    submit.click(resetchat, outputs=[chatbot, state, message])

block.launch(debug=True)
