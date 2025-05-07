import GUI
from BSkyAPI import get_posts_from_search, get_posts_from_handle
from analyse import model as sentiment_model_class

app = GUI.GUI()


app.launch()

class controler:

    def get_api_requirements(self):
        app.predict_sentiment()

    def call_api(self):
        self.get_api_requirements()

    def call_sentiment_anayliser(self):

    def call_display_result(self):
