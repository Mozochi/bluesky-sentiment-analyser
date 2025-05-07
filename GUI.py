import time
import gradio as gr
import analyse

MODEL_FILEPATH = "sentiment_analyser_model.json"

class GUI:
    def __init__(self):
        with gr.Blocks(css=".center {text-align: center; margin-left: auto; margin-right: auto;}") as self.interface:
            gr.Markdown("# Facebook sentiment tantaliser", elem_classes="center")

            self.choice = gr.Radio(
                ["Profile", "Key word"],
                label="Choose one:",
                value="Profile"
            )

            self.input_label = gr.Textbox(
                value=self.get_input_text(),
                interactive=False,
                label="",
                elem_classes="invisible-box"
            )

            self.text_input = gr.Textbox(label="Input")
            self.submit = gr.Button("Submit")
            self.output = gr.Textbox(label="Result:")

            self.choice.change(
                fn=self.update_input_text_label,
                inputs=self.choice,
                outputs=self.input_label
            )

            self.submit.click(
                fn=self.predict,
                inputs=[self.choice, self.text_input],
                outputs=self.output
            )

    def get_input_text(self):
        if self.choice.value == "Profile":
            return "Please enter the Facebook profile."
        else:
            return "Please enter a keyword."

    def update_input_text_label(self, choice):
        self.choice.value = choice
        return self.get_input_text()

    def predict(self, choice, text_input):
        model = analyse.model()
        result = model.run_model(MODEL_FILEPATH, [text_input])
        return result

    def launch(self):
        self.interface.launch()

