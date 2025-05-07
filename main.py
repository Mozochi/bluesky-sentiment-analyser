from GUI import GUI
from controller import Controller
from analyse import SentimentAnalyser
from BSkyAPI import *

if __name__ == '__main__':

    class SimpleBSkyAPIClient:
        def __init__(self, search_func, handle_func, validate_handle_func):
            self.get_posts_from_search = search_func
            self.get_posts_from_handle = handle_func
            self.handle_validation = validate_handle_func

    PATH_TO_MODEL_FILE = "sentiment_analyser_model.json"

    ### Instantiate Components
    # 1. API Client
    api_client = SimpleBSkyAPIClient(
        search_func=bluesky_api.get_posts_from_search,
        handle_func=bluesky_api.get_posts_from_handle,
        validate_handle_func=bluesky_api.handle_validation
    )

    # 2. Sentiment Analyser
    sentiment_analyser_instance = SentimentAnalyser()

    # 3. Controller
    app_controller = Controller(
        api_client=api_client,
        sentiment_analyser=sentiment_analyser_instance,
        model_path=PATH_TO_MODEL_FILE
    )

    # 4. GUI
    app_gui = GUI(controller_instance=app_controller)
    app_gui.launch()
