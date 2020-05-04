from sklearn.feature_extraction.text import CountVectorizer

sentences = ['I dansk kan man skrive med bogstager', 'I matematik kan man regne med tal']

vectorizer = CountVectorizer(min_df=0, lowercase=False)
vectorizer.fit(sentences)

print(vectorizer.vocabulary_)
# {'dansk': 1, 'kan': 2, 'man': 3, 'skrive': 7, 'med': 5, '
#  bogstager': 0, 'matematik': 4, 'regne': 6, 'tal': 8}
print(vectorizer.transform(sentences).toarray())
# [[1 1 1 1 0 1 0 1 0]
#  [0 0 1 1 1 1 1 0 1]]
