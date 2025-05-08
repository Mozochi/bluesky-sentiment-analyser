import gradio as gr
from gradio import themes


class GUI:
    def __init__(self, controller_instance):
        self.controller = controller_instance

        custom_css = """
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
            gr.Markdown("# Bluesky Sentiment Analyser", elem_classes="center")

            self.choice_var = gr.Radio(
                ["Profile", "Keyword"],
                label="Analyse by:",
                value="Profile",  # Default Value
                info="Select whether you want to analyse a profile or search by a keyword."
            )

            self.text_input_var = gr.Textbox(
                label="Please enter the Bluesky profile name:",
                placeholder="e.g. linusmediagroup.com",
                show_label=True
            )

            # Add a new radio button for search type that is initially hidden
            self.search_type_var = gr.Radio(
                ["Top", "Latest"],
                label="Search type:",
                value="Top",  # Default Value
                visible=False,
                info="Select whether to search for top posts or latest posts."
            )

            self.submit_button = gr.Button("Submit", variant="primary")
            self.output_textbox = gr.Textbox(label="Result:", interactive=False, lines=10, show_copy_button=True)
            self.output_stats_textbox = gr.Textbox(label="Stats:", interactive=False, lines=3, show_copy_button=True)

            self.choice_var.change(
                fn=self.update_input_text_label_and_placeholder,
                inputs=self.choice_var,
                outputs=[self.text_input_var, self.search_type_var]
            )

            self.submit_button.click(
                fn=self.predict_sentiment_wrapper,
                inputs=[self.choice_var, self.text_input_var, self.search_type_var],
                outputs=[self.output_textbox, self.output_stats_textbox]
            )

    def update_input_text_label_and_placeholder(self, current_choice):
        # Updates the label and the placeholder of the text input based on the radio choice
        if current_choice == "Profile":
            return gr.update(
                label="Please enter the BlueSky profile name:",
                placeholder="e.g. linusmediagroup.com"
            ), gr.update(visible=False)
        else:  # Keyword
            return gr.update(
                label="Please enter a keyword to search for:",
                placeholder="e.g. climate change"
            ), gr.update(visible=True)

    def predict_sentiment_wrapper(self, selected_choice: str, user_input_text: str, search_type: str) -> tuple[
        str, str]:
        # Call the controller's method to handle the logic
        # Now passing the search_type parameter (will be used only when Keyword is selected)
        main_result, stats_result = self.controller.process_analysis_request(selected_choice, user_input_text,
                                                                             search_type)
        return main_result, stats_result

    def launch(self):
        self.interface.launch()