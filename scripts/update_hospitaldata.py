import os
import pandas as pd
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

def get_data():
    url = 'https://healthdata.gov/dataset/covid-19-estimated-patient-impact-and-hospital-capacity-state'
    source = requests.get(url, headers=headers)

    # get html
    soup = BeautifulSoup(source.text, "html.parser")

    resources = soup.find(id='data-and-resources').findChildren()[1]
    link_row = resources.findAll('span', class_="links")

    df1 = pd.read_csv(link_row[0].findAll('a')[1].attrs['href'])
    df2 = pd.read_csv(link_row[1].findAll('a')[1].attrs['href'])
    df3 = pd.read_csv(link_row[2].findAll('a')[1].attrs['href'])
    df1 = df1[['state','collection_date','Inpatient Beds Occupied Estimated',
               'Percentage of Inpatient Beds Occupied Estimated','Total Inpatient Beds']]
    df2 = df2[['state','collection_date','Inpatient Beds Occupied by COVID-19 Patients Estimated',
               'Percentage of Inpatient Beds Occupied by COVID-19 Patients Estimated']]
    df3 = df3[['state','collection_date','Staffed Adult ICU Beds Occupied Estimated',
               'Percentage of Staffed Adult ICU Beds Occupied Estimated','Total Staffed Adult ICU Beds']]
    df = df1.merge(df2, on=['state','collection_date']).merge(df3, on=['state','collection_date'])
    return df

df = get_data()
base_path = 'time_series_data/'
for i in sorted(set(df['collection_date'].to_list())):
    dir_path = base_path + i
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    df2 = df[df['collection_date'] == i].to_csv(dir_path + '/hospital_data.csv')