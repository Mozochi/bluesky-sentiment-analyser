import gradio as gr
from gradio import themes

class GUI:
    def __init__(self, controller_instance):
        self.controller = controller_instance

        custom_css="""
        .center {
            text-align: center; 
            margin-left: auto; 
            margin-right: auto;
        }
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        """

        with gr.Blocks(css=custom_css, theme=themes.Ocean()) as self.interface:
            gr.Markdown("# Sentiment Analyser", elem_classes="center")

            self.choice_var = gr.Radio(
                ["Profile", "Keyword"],
                label="Analyse by:",
                value="Profile", # Default Value
                info="Select whether you want to analyse a profile or search by a keyword."
            )

            self.text_input_var = gr.Textbox(
                label="Please enter the Bluesky profile name:",
                placeholder="e.g. linusmediagroup.com",
                show_label=True
            )

            self.submit_button = gr.Button("Submit", variant="primary")
            self.output_textbox = gr.Textbox(label="Result:", interactive=False, lines=10)

            self.choice_var.change(
                fn=self.update_input_text_label_and_placeholder,
                inputs=self.choice_var,
                outputs=self.text_input_var
            )

            self.submit_button.click(
                fn=self.predict_sentiment_wrapper,
                inputs=[self.choice_var, self.text_input_var],
                outputs=self.output_textbox
            )

    def update_input_text_label_and_placeholder(self, current_choice):
        # Updates the label and the placeholder of the text input based on the radio choice
        if current_choice == "Profile":
            return gr.update(
                label="Please enter the BlueSky profile name:",
                placeholder="e.g. linusmediagroup.com"
            )
        else: #Keyword
            return gr.update(
                label="Please enter a keyword to search for:",
                placeholder="e.g. climate change"
            )

    def predict_sentiment_wrapper(self, selected_choice: str, user_input_text: str) -> str:
        # Call the controller's method to handle the logic
        result = self.controller.process_analysis_request(selected_choice, user_input_text)
        return result

    def launch(self):
        self.interface.launch()
