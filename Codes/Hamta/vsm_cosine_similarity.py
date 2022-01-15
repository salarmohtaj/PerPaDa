from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

with open("data/list_of_fragments.LIST", 'rb') as f:
    list_of_fragments = pickle.load(f)

dic = {}
####computing VSM cosine similarity for differen ranges of n
for i in range(1, 11):
    dic[i] = []
    vectorizer = TfidfVectorizer(use_idf=False, ngram_range=(i, i))
    for item in list_of_fragments:
        try:
            X = vectorizer.fit_transform(item)
        except:
            continue
        dic[i].append(cosine_similarity(X)[0, 1])

with open("data/hamta_vsm_similarities.DIC","wb") as f:
    pickle.dump(dic, f)

