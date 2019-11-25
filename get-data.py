from typing import Optional

import gspread
from gspread import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pandas as pd
import matplotlib as pt
from itertools import *
age_groups=[(8,13),(13,18),(18,30),(30,40),(40,50),(50,100)]
def get_age_group(age):

    for age_group in age_groups:
        if age_group[0]<=age<age_group[1]:
            return age_group
    return (-1,-1)





def get_responses():

    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("ScicanResponses").sheet1
    print(sheet.get_all_records())
    return sheet.get_all_records()


if __name__ == '__main__':
    frame=get_responses()
    fx=lambda x:get_age_group(int(x["age"]))
    frame.sort(key=fx)
    groupby(frame,key=fx)
    print(frame)



    #pop the first group because it is invalid (-1,-1)



