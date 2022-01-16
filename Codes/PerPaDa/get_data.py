import mysql.connector
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
import json
from info import connection_info, query1, query2, query3, business_account

mydb = mysql.connector.connect(
  host=connection_info["host"],
  user=connection_info["user"],
  password=connection_info["password"],
  database=connection_info["database"]
)

mycursor = mydb.cursor()
mycursor.execute(query)
field_names = [i[0] for i in mycursor.description]
df = DataFrame(mycursor.fetchall())
df.columns = field_names
df = df[~df.user_id.isin(business_account)]



plt.hist(df["counts"], density=False, bins=200)  # density=False would make counts
plt.ylabel('Probability')
plt.xlabel('Data')
plt.show()


ax = sns.distplot(df["counts"], hist=False, kde=True,
             color = 'royalblue',
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})
ax.set(xlabel='Number of submitted documents', ylabel='Probability')
ax.set_xlim(0,350)
#plt.show()
plt.savefig('data/Num_of_Req_PDF.eps', format='eps')


df = df[df['counts'] > 1]
users = df["user_id"].tolist()
users = tuple(users)
mycursor.execute(query2.format(users))
num_fields = len(mycursor.description)
field_names = [i[0] for i in mycursor.description]
df_doc = DataFrame(mycursor.fetchall())
df_doc.columns = field_names

l = []
def retuen_length(text):
    return len(text.split(" "))
df_doc["len"]=df_doc.sus_text.apply(retuen_length)


ax = sns.distplot(df["len"], hist=True, kde=True,
             hist_kws={'edgecolor':'black',"color":"darkorange"},
             kde_kws={'linewidth': 4 , 'color':'royalblue'})
ax.set(xlabel='Document length (in words)', ylabel='Probability')
ax.set_xlim(0,100000)
plt.gcf().subplots_adjust(left=0.15)
plt.tight_layout()
#plt.show()
plt.savefig('data/length_distribution.eps', format='eps')




### Save each user's documents in a separated json file ###
users = df['user_id'].tolist()

for user in users:
    mycursor.execute(query3.format(user))
    df_text = DataFrame(mycursor.fetchall())
    list_of_doc = df_text[0].tolist()
    with open("rawData/"+str(user)+".json", 'w') as f:
        json.dump(list_of_doc, f)
###########################################################