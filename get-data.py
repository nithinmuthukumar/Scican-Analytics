from collections import defaultdict
from collections import Counter
from typing import Optional

import gspread
from gspread import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
age_groups=[(10,15),(15,20),(20,30),(30,40),(40,50),(50,100)]
frequencyVals={"Very Rarely":0,"Rarely":1,"Occasionally":2,"Frequently":3,"Very Frequently":4}
def get_group(responses,ind,col):
    x=responses[col].loc[ind]

    for j,i in enumerate(age_groups):
        if i[0]<=x<i[1]:
            return j
def get_responses():

    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("ScicanResponses").sheet1
    print(sheet.get_all_records())
    return sheet.get_all_records()


if __name__ == '__main__':
    responses=pd.DataFrame(get_responses())
    #gender analysis
    print("gender analysis")
    num_males=sum(1 for i in responses['Gender'] if i == 'Male')
    num_fems=sum(1 for i in responses['Gender'] if i=='Female')
    for j in responses.iloc[:,5:9]:
        print(j)
        if j=="Frequency":
            m_interest_avg = sum(frequencyVals[a] for a, b in zip(responses[j], responses['Gender']) if b == 'Male')/num_males
            f_interest_avg = sum(frequencyVals[a] for a, b in zip(responses[j], responses['Gender']) if b == 'Female')/num_fems

        else:
            m_interest_avg=sum(a for a,b in zip(responses[j],responses['Gender']) if b=='Male' and a)/num_males
            f_interest_avg=sum(a for a, b in zip(responses[j], responses['Gender']) if b == 'Female' and a)/num_fems
        print(f"male average {m_interest_avg}")
        print(f"female {f_interest_avg}")

    #age analysis
    #partition by age groups
        data = defaultdict(list)
        genre_data =[]
        print("age analysis")

        age_partitions = responses.groupby(lambda x: get_group(responses, x, 'Age'))
        for i in range(6):
            group = age_partitions.get_group(i)
            size = len(group)
            print(f"Age group: {age_groups[i][0]}-{age_groups[i][1] - 1}")
            for j in group.iloc[:, 5:9]:
                print(j)
                data[j].append(sum(x if type(x) != str else frequencyVals[x] for x in [w for w in group[j] if w])/size)
                print(sum(x if type(x) != str else frequencyVals[x] for x in [w for w in group[j] if w])/size)
            # gets frequency of genres which have been cleaned
            genre_freq = Counter(map(lambda x: x.title().strip(),group['Favourite Genre']))
            genre_data.append(genre_freq.items())



        for var, values in data.items():

            plt.bar([f'{age_groups[i][0]}-{age_groups[i][1]-1}' for i in range(6)], values)
            plt.xlabel("Age Groups")
            plt.ylabel(var)
            plt.title(f"Age groups vs. {var}")
            plt.savefig(f"Age groups vs. {var}.png")
            plt.close()
        for i,j in enumerate(genre_data):
            labels=[i[0] for i in j]
            values=[i[1] for i in j]


            fig1, ax1 = plt.subplots()
            ax1.pie(values,labels=labels,startangle=90)
            ax1.axis('equal')
            plt.tight_layout()
            plt.savefig(f'Favourite genre breakdown of {age_groups[i][0]}-{age_groups[i][1]-1} year olds')
            plt.close()













    #pop the first group because it is invalid (-1,-1)



