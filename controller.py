class Controller:

    def __init__(self, api_client, sentiment_analyser, model_path: str):
        self.api_client = api_client
        self.sentiment_analyser = sentiment_analyser
        self.model_path = model_path


    def process_analysis_request(self, selected_choice: str, user_input_text: str) -> tuple[str, str]:
        empty_stats_string = "Positive: 0\nNeutral: 0\nNegative:0"
        if not user_input_text:
            return "Error: Please enter some text", empty_stats_string
        
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
                return "No posted found for the keyword, or an API error as occurred.", empty_stats_string

        else:
            return "Error: Invalid choice selected.", empty_stats_string
        
        actual_texts_list = api_data['text'].tolist()
        if not actual_texts_list:
            return "No text content found in fetched posts.", empty_stats_string
        
        analysis_result, sentiment_counts = self.sentiment_analyser.run_model(self.model_path, actual_texts_list)

        if isinstance(analysis_result, str) and sentiment_counts is None:
            return analysis_result, empty_stats_string # Error from sentiment analyser


        main_output_string = ""
        if isinstance(analysis_result, list):
            if not analysis_result or (len(analysis_result) == 1 and analysis_result[0] == "No predictions were made."):
                main_output_string = "Sentiment analysis completed, but no specific predictions were generated."
            else:
                main_output_string = "\n".join(analysis_result)
        else: 
            main_output_string = "Error: Unexpected result type from sentiment analyser details."
        
        stats_output_string = ""
        if sentiment_counts:
            stats_output_string = (
                f"Positive: {sentiment_counts.get('Positive', 0)}\n"
                f"Neutral: {sentiment_counts.get('Neutral', 0)}\n"
                f"Negative: {sentiment_counts.get('Negative', 0)}"
            )
        else:
            stats_output_string = empty_stats_string
        
        return main_output_string, stats_output_string