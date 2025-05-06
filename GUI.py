import tkinter as tk
import time
from tkinter import ttk
import gradio as gr

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
        return f"You selected '{choice}' and typed '{text_input}'."

    def launch(self):
        self.interface.launch()

class GUI2:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x600")

        self.top_label = tk.Label(self.window, text='Facebook Sentiment Analyzer')
        self.button_text = 'Please enter a keyword'
        self.button_label = tk.Label(self.window, text=self.button_text)
        self.submit_button = tk.Button(
            self.window, text='Submit', width=25, command=self.submit
        )

        self.radio_var = tk.IntVar()
        self.radio_button1 = tk.Radiobutton(
            self.window, text='Keyword Input', variable=self.radio_var, value=0,
            command=self.change_button_text
        )
        self.radio_button2 = tk.Radiobutton(
            self.window, text='Profile Input', variable=self.radio_var, value=1,
            command=self.change_button_text
        )

        self.progress_bar = ttk.Progressbar(
            self.window, orient="horizontal", length=300, mode="determinate"
        )

        self.enter_var = tk.StringVar()
        self.entry_field = tk.Entry(self.window, textvariable=self.enter_var)

        self.invalid_input_label = tk.Label(self.window, text='Sorry, invalid input')

        self.display_widgets()
    def display_widgets(self):
        self.top_label.grid(row=0, column=0)
        self.button_label.grid(row=2, column=0)
        self.entry_field.grid(row=2, column=1)
        self.submit_button.grid(row=3, column=0)
        self.progress_bar.grid(row=4, column=0)
        self.radio_button1.grid(row=1, column=0)
        self.radio_button2.grid(row=1, column=1)

    def show_invalid_input_label(self):
        self.invalid_input_label.grid(row=5, column=0)

    def hide_invalid_input_label(self):
        self.invalid_input_label.grid_forget()

    def change_button_text(self):
        if self.radio_var.get() == 0:
            self.button_text = 'Please enter a keyword'

        else:
            self.button_text = 'Please enter a profile name'

        self.button_label.config(text=self.button_text)

    def start_progress(self):
        # place holder from geeks for geeks
        self.progress_bar.start()

        for i in range(101):
            time.sleep(0.05)
            self.progress_bar['value'] = i
            self.window.update_idletasks()

        self.progress_bar.stop()

    def get_data(self):
        # call controller
        return

    def submit(self):
        user_input = self.enter_var.get().strip()

        if not user_input:
            self.show_invalid_input_label()

        else:
            if (self.radio_var.get() == 0):
                pass

            else:
                pass

            self.start_progress()
            self.get_data()

        self.enter_var.set("")

    def main_loop(self):
        self.window.mainloop()
