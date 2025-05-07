class Controller:

    def __init__(self, api_client, sentiment_analyser, model_path: str):
        self.api_client = api_client
        self.sentiment_analyser = sentiment_analyser
        self.model_path = model_path
        self.actual_texts_list = []

    def get_sentiments(self, selected_choice: str, user_input_text: str) -> str:
        if not user_input_text:
            return "Error: Please enter some text"
        
        api_data = None
        if selected_choice == "Profile":
            is_valid = self.api_client.handle_validation(user_input_text)
            if not is_valid:
                return "The profile name is invalid or does not exist. Please try again."
            api_data = self.api_client.get_posts_from_handle(user_input_text)
            
        elif selected_choice == "Keyword":
            api_data = self.api_client.get_posts_from_search(user_input_text, "latest", "en")
            if api_data is None or api_data.empty:
                return "No posts found for the keyword, or an API error has occurred."
        else:
            return "Error: Invalid choice selected."
        
        self.actual_texts_list = api_data['text'].tolist()
        if not self.actual_texts_list:
            return "No text content found in fetched posts."

        return "Data fetched successfully. Ready for analysis."
    
    def process_analysis_request(self, selected_choice: str, user_input_text: str) -> str:
        if not self.actual_texts_list:
            get_result = self.get_sentiments(selected_choice, user_input_text)
            if "Error" in get_result or "invalid" in get_result.lower() or "No" in get_result:
                return get_result
        
        analysis_result = self.sentiment_analyser.run_model(self.model_path, self.actual_texts_list)

        if isinstance(analysis_result, str):
            return analysis_result
        elif isinstance(analysis_result, list):
            if not analysis_result or (len(analysis_result) == 1 and analysis_result[0] == "No predictions were made."):
                return "Sentiment analysis complete, but no predictions were generated."
            return "\n".join(analysis_result)
        else:
            return "Error: Unexpected result type from sentiment analyser."
        
