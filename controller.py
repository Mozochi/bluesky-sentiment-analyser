class Controller:
    """
    Controller class to manage sentiment analysis requests by interacting with the API client 
    and the sentiment analyser.

    Attributes:
        api_client: The API client used to fetch posts based on user input.
        sentiment_analyser: The sentiment analyser used to perform sentiment analysis on text data.
        model_path: The path to the pre-trained model for sentiment analysis.
    """

    def __init__(self, api_client, sentiment_analyser, model_path: str):
        """
        Initializes the Controller with the necessary components.

        Parameters:
            api_client: The API client instance to interact with external services.
            sentiment_analyser: The sentiment analyser instance for analyzing sentiment.
            model_path: The path where the model is stored.
        """
        self.api_client = api_client
        self.sentiment_analyser = sentiment_analyser
        self.model_path = model_path

    def process_analysis_request(self, selected_choice: str, user_input_text: str, search_type: str) -> tuple[str, str, str]:
        """
        Processes the sentiment analysis request based on the user's input and choice.

        Parameters:
            selected_choice: The choice selected by the user ("Profile" or "Keyword").
            user_input_text: The input text or profile name provided by the user.
            search_type: The type of search used in case of a keyword search (e.g., "en").

        Returns:
            A tuple containing:
                - A string with the analysis result (or error message).
                - A string with the sentiment statistics.
        """
        empty_stats_string = "Positive: 0\nNeutral: 0\nNegative:0"

        # Check if user provided input
        if not user_input_text:
            return "Error: Please enter some text", empty_stats_string

        # Fetch API data based on selected choice
        api_data = None
        if selected_choice == "Profile":
            api_data = self.api_client.handle_validation(user_input_text)

            if api_data is False:
                return "The profile name is invalid or does not exist. Please try again.", empty_stats_string
            api_data = self.api_client.get_posts_from_handle(user_input_text)

        elif selected_choice == "Keyword":
            api_data = self.api_client.get_posts_from_search(user_input_text, search_type, "en")

            if api_data.empty or api_data is None:
                return "No posts found for the keyword, or an API error occurred.", empty_stats_string

        else:
            return "Error: Invalid choice selected.", empty_stats_string

        # Process text from API response
        actual_texts_list = api_data['text'].tolist()
        if not actual_texts_list:
            return "No text content found in fetched posts.", empty_stats_string

        # Perform sentiment analysis
        analysis_result, sentiment_counts = self.sentiment_analyser.run_model(self.model_path, actual_texts_list)

        if isinstance(analysis_result, str) and sentiment_counts is None:
            return analysis_result, empty_stats_string  # Error from sentiment analyser

        # Prepare analysis output
        main_output_string = ""
        if isinstance(analysis_result, list):
            if not analysis_result or (len(analysis_result) == 1 and analysis_result[0] == "No predictions were made."):
                main_output_string = "Sentiment analysis completed, but no specific predictions were generated."
            else:
                main_output_string = "\n".join(analysis_result)
        else:
            main_output_string = "Error: Unexpected result type from sentiment analyser details."

        # Prepare sentiment statistics output
        stats_output_string = ""
        if sentiment_counts:
            stats_output_string = (
                f"Total posts analysed: {sentiment_counts.get('Total', 0)}\n"
                f"Positive: {sentiment_counts.get('Positive', 0)} "
                f"({round(sentiment_counts.get('Positive', 0) / sentiment_counts.get('Total'), 2) * 100}%)\n"
                f"Neutral: {sentiment_counts.get('Neutral', 0)} "
                f"({round(sentiment_counts.get('Neutral', 0) / sentiment_counts.get('Total'), 2) * 100}%)\n"
                f"Negative: {sentiment_counts.get('Negative', 0)} "
                f"({round(sentiment_counts.get('Negative', 0) / sentiment_counts.get('Total'), 2) * 100}%)"
            )
        else:
            stats_output_string = empty_stats_string

        return main_output_string, stats_output_string