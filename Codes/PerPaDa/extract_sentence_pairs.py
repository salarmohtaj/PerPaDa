import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from langdetect import detect
from bs4 import BeautifulSoup
from parsivar import Tokenizer, Normalizer
import pickle
import glob

def jaccard_similarity(list1, list2):
    try:
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(set(list1)) + len(set(list2))) - intersection
        return float(intersection) / union
    except:
        return 0


def text_cleanup(text):
    text = re.sub("[\<]mark.*?[\>]", " ", text)
    text = re.sub("([\(\[]).*?([\)\]])", " ", text)
    text = text.replace("</mark>", " ")
    text = re.sub(' +', ' ', text)
    return text


def offset_based_comparson(near_duplicate_pairs):
    check_to_be_unique = {}
    par_list = []
    sim = []
    for item in near_duplicate_pairs:
        sent = []
        text = re.sub("([\(\[]).*?([\)\]])", " ", list_of_docs[item[0]])
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.find_all("mark"):
            text = tag.text
            try:
                lan = detect(text)
            except:
                lan = "en"
            if ((lan == "fa") and (len(text) > 10)):
                str1 = list_of_docs[item[0]].find(text)
                if str1 != -1:
                    str = max(0, str1 - 200)
                    end = str1 + len(text) + 200
                    t = second_list[item[1]][str:end]
                    s1 = my_tokenizer.tokenize_sentences(my_normalizer.normalize(text))
                    s2 = my_tokenizer.tokenize_sentences(my_normalizer.normalize(t))
                    for sent1 in s1:
                        if (len(sent1) > 50):
                            words1 = my_tokenizer.tokenize_words(my_normalizer.normalize(sent1))
                            try:
                                words1.remove('.')
                            except:
                                pass
                            for sent2 in s2:
                                if (len(sent2) > 50):
                                    words2 = my_tokenizer.tokenize_words(my_normalizer.normalize(sent2))
                                    try:
                                        words2.remove('.')
                                    except:
                                        pass
                                    jj = jaccard_similarity(words1, words2)
                                    if ((jj > 0.7) and (jj < 0.99)):
                                        try:
                                            check_to_be_unique[sent1 + sent2]
                                        except:
                                            check_to_be_unique[sent1 + sent2] = 1
                                            par_list.append((sent1, sent2))
                                            sim.append(jj)
    return(par_list, sim)

def general_comparison(near_duplicate_pairs):
    sim = []
    par_list = []
    check_to_be_unique = {}
    for item in near_duplicate_pairs:
        sent = []
        text = re.sub("([\(\[]).*?([\)\]])", " ", list_of_docs[item[0]])
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.find_all("mark"):
            text = tag.text
            try:
                lan = detect(text)
            except:
                lan = "en"
            if ((lan == "fa") and (len(text) > 10)):
                s = my_tokenizer.tokenize_sentences(my_normalizer.normalize(text))
                for j in s:
                    sent.append(j)
        try:
            X1 = vectorizer.transform(sent)
            par_sents = my_tokenizer.tokenize_sentences(my_normalizer.normalize(second_list[item[1]]))
            X2 = vectorizer.transform(par_sents)
            cosine_similarities = cosine_similarity(X1, X2)
            temp1 = np.argwhere((cosine_similarities > 0.8) & (cosine_similarities < 0.9))
        except:
            continue
        for i in temp1:
            len_original = len(sent[i[0]])
            len_paraphrased = len(par_sents[i[1]])
            if ((len_original > 50) and (len_paraphrased > 50)):
                if ((sent[i[0]].replace(" ", "") in par_sents[i[1]].replace(" ", "")) or (
                        par_sents[i[1]].replace(" ", "") in sent[i[0]].replace(" ", ""))):
                    continue
                if ((len_original < 150) and (sent[i[0]].count("،") > 2)):
                    continue
                elif ((len_paraphrased < 150) and (par_sents[i[1]].count("،") > 2)):
                    continue
                if ((len_original > 300) or (len_paraphrased > 300)):
                    continue
                try:
                    difference_ratio = (len_original) / abs(len_original - len_paraphrased)
                except ZeroDivisionError:
                    difference_ratio = float('inf')
                if (difference_ratio < 5):
                    continue
                try:
                    check_to_be_unique[sent[i[0]] + par_sents[i[1]]]
                except KeyError:
                    check_to_be_unique[sent[i[0]] + par_sents[i[1]]] = 1
                    par_list.append((sent[i[0]], par_sents[i[1]]))
                    sim.append(cosine_similarities[i[0], i[1]])
    return(par_list,sim)

my_tokenizer = Tokenizer()
my_normalizer = Normalizer()
paraphrase_list = []
similarities = []


file_list = glob.glob("rawData/*.json")

for files in file_list:
    with open(files,'r') as f:
        list_of_docs = json.load(f)
    second_list = []
    for doc in list_of_docs:
        text = text_cleanup(doc)
        second_list.append(text)
    ### Find near duplicate documents ###
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(second_list)
    cosine_similarities = cosine_similarity(X, X)#.flatten()
    near_duplicate_pairs = np.argwhere((cosine_similarities > 0.8) & (cosine_similarities < 0.99))
    ### Compare DOCs with the later ones ###
    near_duplicate_pairs = near_duplicate_pairs[near_duplicate_pairs[:, 0] < near_duplicate_pairs[:, 1]]

    par_list, sim = general_comparison(near_duplicate_pairs)
    paraphrase_list.extend(par_list)
    similarities.extend(sim)

    #par_list, sim = offset_based_comparson(near_duplicate_pairs)
    #paraphrase_list.extend(par_list)
    #similarities.extend(sim)

with open("data/paraphrase_list.LIST", "wb") as f:
    pickle.dump(paraphrase_list, f)

with open("data/similarities.LIST", "wb") as f:
    pickle.dump(similarities, f)
