from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import os

ABS_FILEPATH = os.path.dirname(os.path.abspath(__file__))


# Labels:
# 1: Byg
# 2: Dan
# 3: Mat


class TextClassifierModel:
    def __init__(self):
        self.model_file = fr"{ABS_FILEPATH}\data\classes\combined_test.txt"
        self.filepath_dict = {
            "combined": self.model_file,
        }
        self.create_dataframe()
        self.create_model()

    def create_dataframe(self):
        df_list = []
        for text_class, filepath in self.filepath_dict.items():
            df = pd.read_csv(filepath, names=["sentence", "label"], sep="\t")
            df["text_class"] = text_class
            df_list.append(df)

        self.df = pd.concat(df_list)

    def create_model(self):
        self.df_combined = self.df[self.df["text_class"] == "combined"]

        sentences = self.df_combined["sentence"].values
        y = self.df_combined["label"].values

        (
            self.sentences_train,
            self.sentences_test,
            self.y_train,
            self.y_test,
        ) = train_test_split(sentences, y, test_size=0.25, random_state=1000)

        self.vectorizer = CountVectorizer()
        self.vectorizer.fit(self.sentences_train)

        self.X_train = self.vectorizer.transform(self.sentences_train)
        self.X_test = self.vectorizer.transform(self.sentences_test)

        self.classifier = LogisticRegression()
        self.classifier.fit(self.X_train, self.y_train)

    def add_data(self, data):
        with open(self.model_file, "ab") as f:
            f.write(data)

    def refresh_model(self):
        self.create_dataframe()
        self.create_model()

    def print_score(self):
        score = self.classifier.score(self.X_test, self.y_test)
        print("Accuracy:", score)

    def get_score(self):
        score = self.classifier.score(self.X_test, self.y_test)
        score_precent = "{0:.2f}%".format(score * 100)
        return score_precent

    def prepare_model_data(self, body, class_id):
        body_for_model = body.replace("\t", "    ")
        body_for_model = str.join(" ", body_for_model.splitlines())
        body_for_model = body_for_model + "\t" + str(class_id)
        body_for_model = "\n" + body_for_model
        body_for_model = body_for_model.encode("UTF-8")
        return body_for_model

    def prepare_data(self, data):
        data = [data]
        self.prepare_vectorizer = CountVectorizer()
        self.prepare_vectorizer.fit(data)
        self.prepared_data = self.vectorizer.transform(data)

    def predict_class(self):
        prediction = self.classifier.predict(self.prepared_data)
        return prediction[0]


if __name__ == "__main__":
    model = TextClassifierModel()
    model.print_score()
    test_data = str(input("Give me some text!: "))
    model.prepare_data(test_data)
    prediction = model.predict_class()
    print(f"Prediction: {prediction=}")
