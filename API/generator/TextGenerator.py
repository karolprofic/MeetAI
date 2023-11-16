

class TextGenerator:
    def __init__(self, path, openAI):
        self.path = path
        self.openAI = openAI

    def generate(self, model):
        model = model.lower().replace(" ", "_")

