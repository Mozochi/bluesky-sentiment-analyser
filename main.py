from GUI import GUI
from controller import Controller
from analyse import SentimentAnalyser
from BSkyAPI import *


class SimpleBSkyAPIClient:
    def __init__(self, search_func, handle_func, validate_handle_func):
        self.get_posts_from_search = search_func
        self.get_posts_from_handle = handle_func
        self.handle_validation = validate_handle_func  


if __name__ == '__main__':
    PATH_TO_MODEL_FILE = "sentiment_analyser_model.json"

    ### Instantiate Components
    # 1. API Client
    api_instance = BlueskyAPI()

    api_client = SimpleBSkyAPIClient(
        search_func=api_instance.get_posts_from_search,
        handle_func=api_instance.get_posts_from_handle,
        validate_handle_func=api_instance.handle_validation
    )

    # 2. Sentiment Analyser
    the_sentiment_analyser_instance = SentimentAnalyser()

    # 3. Controller
    the_app_controller = Controller(
        api_client=api_client,
        sentiment_analyser=the_sentiment_analyser_instance,
        model_path=PATH_TO_MODEL_FILE
    )

    # 4. GUI
    the_app_gui = GUI(controller_instance=the_app_controller)
    the_app_gui.launch()
