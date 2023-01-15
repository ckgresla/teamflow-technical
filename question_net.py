import nltk
import nltk.corpus


class QuestionModel():
    def __init__(self, trained=True) -> None:
        self.trained = trained
        if self.trained:
            self.training_data = self.get_training_set()
            self.model = nltk.NaiveBayesClassifier.train(self.training_data) #simple model as per- https://www.nltk.org/api/nltk.classify.naivebayes.html?highlight=naivebayes#nltk.classify.naivebayes.NaiveBayesClassifier
        pass

    def get_training_set(self):
        # Get NPS Chat Data- https://www.nltk.org/howto/corpus.html#nps-chat
        nps_chat = nltk.corpus.nps_chat.xml_posts()
        train_set = []
        for post in nps_chat:
            features = self.get_features(post.text)
            print(post.text)
            train_set.append((features, post.get("class"))) #data to infer question + class in NPS (is question or not for training)
            print(features, post.get("class"))
        return train_set

    # Given a String, convert it into "features" for the naive bayes model
    def get_features(self, text: str):
        features = {} #per instance
        tokens = nltk.word_tokenize(text)
        for tok in tokens:
            features['contains({})'.format(tok.lower())] = True
        return

    # Given some text, use trained model to for inference (classify y/n for text being a question)
    def is_question(self, text: str=None):
        inp = self.get_features(text.lower())
        out = self.model.classify(inp)
        print(out)

        return

qm = QuestionModel() #trains simple model on import

out = qm.is_question("who the hell are you?")
print(out)