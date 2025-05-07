class Controller:

    def __init__(self, api_client, sentiment_analyser, model_path: str):
        self.api_client = api_client
        self.sentiment_analyser = sentiment_analyser
        self.model_path = model_path


    def process_analysis_request(self, selected_choice: str, user_input_text: str) -> str:
        if not user_input_text:
            return "Error: Please enter some text"
        
        api_data = None
        if selected_choice == "Profile":
            api_data = self.api_client.handle_validation(user_input_text)

            if api_data is False:
                return "The profile name is invalid or does not exist. Please try again."
            else:
                api_data = self.api_client.get_posts_from_handle(user_input_text)

            
        elif selected_choice == "Keyword":
            api_data = self.api_client.get_posts_from_search(user_input_text, "latest", "en")

            if api_data.empty or api_data is None:
                return "No posted found for the keyword, or an API error as occurred."

        else:
            return "Error: Invalid choice selected."
        
        actual_texts_list = api_data['text'].tolist()
        if not actual_texts_list:
            return "No text content found in fetched posts."
        
        analysis_result = self.sentiment_analyser.run_model(self.model_path, actual_texts_list)

        if isinstance(analysis_result, str):
            return analysis_result
        elif isinstance(analysis_result, list):
            if not analysis_result or (len(analysis_result) == 1 and analysis_result[0] == "No predictions were made."):
                return "Sentiment analysis complete, but no predictions were generated."
            return "\n".join(analysis_result)
        else:
            return "Error: Unexpected result type from sentiment analyser."