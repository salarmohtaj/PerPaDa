import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


with open("data/paraphrase_list.LIST",'rb') as f:
   paraphrase_list = pickle.load(f)

with open("similarities.LIST", 'rb') as f:
    similarities = pickle.load(f)

with open("data/perpada_sim_list.DIC", "rb") as f:
    dic_perpada = pickle.load(f)
with open("../Hamta/data/hamta_sim_list.DIC", "rb") as f:
    dic_hamta = pickle.load(f)

output_dir = "data"
color_1 = "darkorange"
color_2 = "royalblue"
colors = [color_1, color_2]

def plot_length_boxplot(paraphrase_list, colors, output_dir):
    plot_name = "paraphrase_boxplot.eps"
    my_dict = {'Original': [], 'Paraphrased': []}
    for item in paraphrase_list:
        my_dict["Original"].append(len(item[0]))
        my_dict["Paraphrased"].append(len(item[1]))
    fig, ax = plt.subplots()
    ax.boxplot(my_dict.values(), positions=[0.5,1.5], notch=False, patch_artist=False, widths=(0.25, 0.25),
                boxprops=dict(color=colors[1]),
                capprops=dict(color=colors[1]),
                whiskerprops=dict(color=colors[1]),
                flierprops=dict(color=colors[1], markeredgecolor=colors[1]),
                medianprops=dict(color=colors[1]),
                )
    ax.set_xticklabels(my_dict.keys())
    ax.set_ylabel("Length (in characters)")
    ax.set_xlabel("Sentences")
    plt.gcf().subplots_adjust(left=0.15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, plot_name), format='eps')
    plt.show()


def plot_length_boxplot(similarities, colors, output_dir):
    plot_name = 'similarity_distribution.eps'
    ax = sns.distplot(similarities, hist=False, kde=True,
                 hist_kws={'edgecolor':'black',"color":colors[0]},
                 kde_kws={'linewidth': 4 , 'color':colors[1]})
    ax.set(xlabel='Pair-wise cosine similarity', ylabel='Probability')
    ax.set_xlim(0.75,0.95)
    plt.gcf().subplots_adjust(left=0.15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, plot_name), format='eps')



### VSM cosine similarity for n in range of 1 to 10
# dic = {}
# for i in range(1,11):
#     dic[i] = []
#     vectorizer = TfidfVectorizer(use_idf=False,ngram_range=(i,i))
#     for item in list:
#         try:
#             X = vectorizer.fit_transform(item)
#         except:
#             continue
#         dic[i].append(cosine_similarity(X)[0,1])



def vsm_comparison_boxplot(dic_perpada, dic_hamta, colors, output_dir):
    plot_name = 'perpada_hamta_comparison.eps'
    fig, ax = plt.subplots()
    bp1 = ax.boxplot(dic_hamta.values(),  notch=False, patch_artist=False, showfliers=False, whis=0,widths=0.8,
                positions=[1,5,9,13,17,21,25,29,33,37],
                boxprops=dict(color=colors[1], linestyle='--'),
                capprops=dict(color=colors[1]),
                whiskerprops=dict(color=colors[1],linestyle='--'),
                flierprops=dict(color=colors[1], markeredgecolor=colors[1]),
                medianprops=dict(color=colors[1]),
                )
    bp2 = ax.boxplot(dic_perpada.values(),  notch=False, patch_artist=False, showfliers=False, whis=0,widths=0.8,
                positions=[2.5,6.5,10.5,14.5,18.5,22.5,26.5,30.5,34.5,38.5],
                boxprops=dict(color=colors[0]),
                capprops=dict(color=colors[0]),
                whiskerprops=dict(color=colors[0]),
                flierprops=dict(color=colors[0], markeredgecolor=colors[0]),
                medianprops=dict(color=colors[0]),
                )
    ax.set_ylim(0, 1)
    ticks = ["n=1","2","3","4","5","6","7","8","9","10"]
    ax.set_xticks(range(2, len(ticks) * 4, 4), ticks)
    ax.set_xlim(0, len(ticks)*4)
    ax.set_ylabel("Similarity")
    ax.set_xlabel("n-gram VSM")
    ax.legend([bp1["boxes"][0],bp2["boxes"][0]], ["HAMTA","PerPaDa"], loc='upper right')
    plt.gcf().subplots_adjust(left=0.15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, plot_name), format='eps')
    plt.show()


plot_length_boxplot(paraphrase_list, colors, output_dir)
plot_length_boxplot(similarities, colors, output_dir)
vsm_comparison_boxplot(dic_perpada, dic_hamta, colors, output_dir)