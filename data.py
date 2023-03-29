import requests


class Data:
    def __init__(self, args):
        self.args = args
        self.response = requests.get("https://opentdb.com/api.php", params=self.args)
        self.question_data = self.response.json()["results"]
