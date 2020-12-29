import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json

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
df.to_csv('data/hospital_data.csv', index=False)
base_path = 'time_series_data/'
for i in sorted(set(df['collection_date'].to_list())):
    dir_path = base_path + i
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    df[df['collection_date'] == i].to_csv(dir_path + '/hospital_data.csv', index=False)

state_list = list(set(list(df['state'].values)))
meta = {
        "Version": "v1",
        "Columns": ["collection_date", "Inpatient Beds Occupied Estimated",
                    "Percentage of Inpatient Beds Occupied Estimated", "Total Inpatient Beds",
                    "Inpatient Beds Occupied by COVID-19 Patients Estimated",
                    "Percentage of Inpatient Beds Occupied by COVID-19 Patients Estimated",
                    "Staffed Adult ICU Beds Occupied Estimated",
                    "Percentage of Staffed Adult ICU Beds Occupied Estimated",
                    "Total Staffed Adult ICU Beds"]
    }
data = {}
for state in state_list:
    df2 = df[df['state'] == state]
    n_inpatient_bed_occupy = df2['Inpatient Beds Occupied Estimated'].to_list()
    n_inpatient_bed_occupy = [int(''.join(i.split(','))) for i in n_inpatient_bed_occupy]
    n_inpatient_bed = df2['Total Inpatient Beds'].to_list()
    n_inpatient_bed = [int(''.join(i.split(','))) for i in n_inpatient_bed]
    n_inpatient_bed_covid_occupy = df2['Inpatient Beds Occupied by COVID-19 Patients Estimated'].to_list()
    n_inpatient_bed_covid_occupy = [int(''.join(i.split(','))) for i in n_inpatient_bed_covid_occupy]
    n_icu_beds_occupy = df2['Staffed Adult ICU Beds Occupied Estimated'].to_list()
    n_icu_beds_occupy = [int(''.join(i.split(','))) for i in n_icu_beds_occupy]
    n_icu_beds = df2['Total Staffed Adult ICU Beds'].to_list()
    n_icu_beds = [int(''.join(i.split(','))) for i in n_icu_beds]

    data[state] = {
        'collection_date': df2['collection_date'].to_list(),
        'Inpatient Beds Occupied Estimated': n_inpatient_bed_occupy,
        'Percentage of Inpatient Beds Occupied Estimated':
            df2['Percentage of Inpatient Beds Occupied Estimated'].to_list(),
        'Total Inpatient Beds': n_inpatient_bed,
        'Inpatient Beds Occupied by COVID-19 Patients Estimated': n_inpatient_bed_covid_occupy,
        'Percentage of Inpatient Beds Occupied by COVID-19 Patients Estimated':
            df2['Percentage of Inpatient Beds Occupied by COVID-19 Patients Estimated'].to_list(),
        'Staffed Adult ICU Beds Occupied Estimated': n_icu_beds_occupy,
        'Percentage of Staffed Adult ICU Beds Occupied Estimated':
            df2['Percentage of Staffed Adult ICU Beds Occupied Estimated'].to_list(),
        'Total Staffed Adult ICU Beds': n_icu_beds
    }
jsondata = {
        "Meta": meta,
        "Data": data
}
with open('data/hospital_data.json', 'w') as f:
    f.write(json.dumps(jsondata))
