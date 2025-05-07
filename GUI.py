import time
import gradio as gr
from gradio import themes

from BSkyAPI import get_posts_from_search, get_posts_from_handle

from analyse import model as sentiment_model_class


sentiment_analyser_instance = sentiment_model_class()
PATH_TO_MODEL = "sentiment_analyser_model.json"




class GUI:
    def __init__(self):

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
                fn=self.predict_sentiment,
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

    def predict_sentiment(self, selected_choice, user_input_text):

        if not user_input_text:
            return "Error: Please enter some text."
        
        if selected_choice == "Profile":
            API_data = get_posts_from_handle(user_input_text)

            
            if API_data.empty:
                return "No posts from user."
            
            actual_texts_list = API_data['text'].tolist()

            if not actual_texts_list:
                return "No text content found in the fetched posts."

            list_of_sentiment_strings = sentiment_analyser_instance.run_model(PATH_TO_MODEL, actual_texts_list)

            
            if isinstance(list_of_sentiment_strings, list):
                return "\n".join(list_of_sentiment_strings)
            else:
                return list_of_sentiment_strings

        
        elif selected_choice == "Keyword":
            API_data = get_posts_from_search(user_input_text, "latest", "en")

            if API_data.empty:
                return "No posted found for the keyword."
            
            actual_texts_list = API_data['text'].tolist()

            if not actual_texts_list:
                return "No text content found in the fetched posts."
            
            list_of_sentiment_strings = sentiment_analyser_instance.run_model(PATH_TO_MODEL, actual_texts_list)

            if isinstance(list_of_sentiment_strings, list):
                return "\n".join(list_of_sentiment_strings)
            else:
                return list_of_sentiment_strings


        else:
            print("Error: Invalid choice selected.")

        

    def launch(self):
        self.interface.launch()

