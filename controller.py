import GUI
from BSkyAPI import get_posts_from_search, get_posts_from_handle
from analyse import model as sentiment_model_class
PATH_TO_MODEL = "sentiment_analyser_model.json"

class controler:

    def __init__(self, theGUI, thesentiment_anayiser, theAPI):
        self.GUI = theGUI
        self.sentiment_anayiser = thesentiment_anayiser
        self.API = theAPI
        self.PATH_TO_MODEL = "sentiment_analyser_model.json"

    def call_api(self):
        selected_choice = self.GUI.get_selected_choice()
        user_input_text = self.GUI.get_input_text()
        
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
            
            list_of_sentiment_strings = self.sentiment_analyser.run_model(self.PATH_TO_MODEL, actual_texts_list)

            if isinstance(list_of_sentiment_strings, list):
                return "\n".join(list_of_sentiment_strings)
            else:
                return list_of_sentiment_strings


        else:
            print("Error: Invalid choice selected.")

    def call_sentiment_anayliser(self):
        return

    def call_display_result(self):
        return
