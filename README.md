# COVID19_Data

Auto fetching data from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) and [HealthData.gov](https://healthdata.gov/) with github schedule action. Processing with python script to get both csv data and json data.

```python
import pandas as pd

# fetching county covid-19 data
df = pd.read_csv('https://raw.githubusercontent.com/lit26/COVID19_Data/main/data/covid_19_county1.csv')
# fetching state covid-19 data
df = pd.read_csv('https://raw.githubusercontent.com/lit26/COVID19_Data/main/data/covid_19_state.csv')
```

# Time series data

Split data according to the dates.

# Data Format

## csv file
state.csv
```
Province_State,Date,Confirmed,Deaths,Daily_Confirmed,Daily_Deaths
Washington,2020-04-03,6846,291,457.0,20.0
...
```

county.csv
```
FIPS,Province_State,Admin2,Date,Confirmed,Deaths,Daily_Confirmed,Daily_Deaths
1001.0,Alabama,Autauga,2020-01-22,0,0,0.0,0.0
...
```
data/county1.csv: cases before 2020-11-01

data/county2.csv: cases after 2020-11-01

hospital.csv
```
state,collection_date,Inpatient Beds Occupied Estimated,Percentage of Inpatient Beds Occupied Estimated,Total Inpatient Beds,Inpatient Beds Occupied by COVID-19 Patients Estimated,Percentage of Inpatient Beds Occupied by COVID-19 Patients Estimated,Staffed Adult ICU Beds Occupied Estimated,Percentage of Staffed Adult ICU Beds Occupied Estimated,Total Staffed Adult ICU Beds
CW,2020-12-18,"530,571",74.56,"711,575","117,550",16.58,"67,513",78.05,"86,498"
AZ,2020-12-18,"11,119",78.5,"14,164","3,942",27.87,"1,582",72.67,"2,177"
...
```

## JSON file
state.json
```
{
    "Meta": {
        "Version": "v1",
        "Columns": [
              "Date",
              "Confirmed",
              "Deaths",
              "Daily_Confirmed",
              "Daily_Deaths"
        ]
  },
  "Data": {
        "Alabama": {
              "Date": [
                ...
              ],
              "Confirmed": [
                ...
              ],
              "Deaths": [
                ...
              ],
              "Daily_Confirmed": [
                ...
              ],
              "Daily_Deaths": [
                ...
              ]
        },...
}
...
```
county.json
```
{
    "Meta": {
        "Version": "v1",
        "Columns": [
              "Date",
              "Confirmed",
              "Deaths",
              "Daily_Confirmed",
              "Daily_Deaths"
        ]
  },
  "Data": {
        "Alabama": {
              "1001.0":{
                    "County": "Autauga",
                    "Date": [
                        ...
                    ],
                    "Confirmed": [
                        ...
                    ],
                    "Deaths": [
                        ...
                    ],
                    "Daily_Confirmed": [
                        ...
                    ],
                    "Daily_Deaths": [
                        ...
                    ]
              }
        }, ...
}
...
```
hospital.json
```
{
    "Meta": {
        "Version": "v1", 
        "Columns": [
            "collection_date", 
            "Inpatient Beds Occupied Estimated", 
            "Percentage of Inpatient Beds Occupied Estimated", 
            "Total Inpatient Beds", 
            "Inpatient Beds Occupied by COVID-19 Patients Estimated", 
            "Percentage of Inpatient Beds Occupied by COVID-19 Patients Estimated", 
            "Staffed Adult ICU Beds Occupied Estimated", 
            "Percentage of Staffed Adult ICU Beds Occupied Estimated", 
            "Total Staffed Adult ICU Beds"
        ]
    }, 
    "Data": {
        "DC": ...
        ...
    }
}
```
