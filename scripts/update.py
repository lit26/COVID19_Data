import pandas as pd
import json
import os

state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', \
            'Diamond Princess', 'District of Columbia', 'Florida', 'Georgia', 'Grand Princess', 'Guam', 'Hawaii',
            'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', \
            'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', \
            'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', \
            'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', \
            'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

def readFile(base_path, file, choice, col_name):
    df_file = pd.read_csv(base_path+file)

    df_file = df_file.drop(
        ["UID", "iso2", "iso3", "code3", "Country_Region", "Combined_Key"], axis=1)
    if choice == 'Deaths':
        df_file = df_file.drop(["Population"], axis=1)
    df_county = df_file.iloc[:, 0:5]
    df_diff = df_file.iloc[:, 5:len(df_file.columns)].diff(axis=1)
    df_diff = df_county.join(df_diff)
    df_file = df_file.melt(id_vars=col_name,
                           var_name="Date",
                           value_name=choice)
    df_diff = df_diff.melt(id_vars=col_name,
                           var_name="Date",
                           value_name=choice)
    df_diff = df_diff.rename(columns={choice: "Daily_"+choice})
    df_file = df_file.merge(df_diff, on=['Date']+col_name)
    df_file['Date'] = pd.to_datetime(df_file['Date'])
    return df_file

def readData():
    col_name = ["FIPS","Province_State", "Admin2", "Lat","Long_"]
    base_path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    df = readFile( base_path, 'time_series_covid19_confirmed_US.csv', 'Confirmed', col_name)
    df2 = readFile(base_path, 'time_series_covid19_deaths_US.csv', 'Deaths', col_name)
    df = df.merge(df2, on=['FIPS','Date', 'Province_State', 'Admin2'])

    # df = df.drop(['Lat_y', 'Long__y'], axis=1)
    # df = df.rename(columns={"Lat_x": "Latitude", "Long__x": "Longitude"})
    # df = df.drop(df[(df.Confirmed == 0) & (df.Deaths == 0)].index)
    df[["Confirmed", "Deaths", "Daily_Confirmed", "Daily_Deaths"]] = \
        df[["Confirmed", "Deaths", "Daily_Confirmed", "Daily_Deaths"]].fillna(0)
    return df[["FIPS","Province_State", "Admin2","Date","Confirmed","Deaths",
               "Daily_Confirmed", "Daily_Deaths"]]
def jsonOutput(df, geo):
    meta = {
        "Version": "v1",
        "Columns": ["Date", "Confirmed", "Deaths", "Daily_Confirmed", "Daily_Deaths"]
    }
    data = {}
    for state in state_list:
        if geo =='state':
            df2 = df[df["Province_State"] == state]
            data[state] = {
                'Date': df2['Date'].dt.strftime('%Y-%m-%d').to_list(),
                'Confirmed': df2['Confirmed'].to_list(),
                'Deaths': df2['Deaths'].to_list(),
                'Daily_Confirmed': df2['Daily_Confirmed'].to_list(),
                'Daily_Deaths': df2['Daily_Deaths'].to_list()
            }
        else:
            county_list = df[df["Province_State"] == state]['Admin2'].unique()
            data[state] = {}
            for county in county_list:
                df2 = df.loc[(df['Province_State'] == state) & (df['Admin2'] == county)]
                data[state][df2["FIPS"].values[0]] = {
                    'County': county,
                    'Date': df2['Date'].dt.strftime('%Y-%m-%d').to_list(),
                    'Confirmed': df2['Confirmed'].to_list(),
                    'Deaths': df2['Deaths'].to_list(),
                    'Daily_Confirmed': df2['Daily_Confirmed'].to_list(),
                    'Daily_Deaths': df2['Daily_Deaths'].to_list()
                }
    jsondata = {
        "Meta": meta,
        "Data": data
    }
    with open('data/covid_19_'+geo+'_v1.json', 'w') as f:
        f.write(json.dumps(jsondata))

def getTimeSeriesData(df, df_state):
    base_path = 'time_series_data/'
    for i in sorted(set(df_state['Date'].to_list())):
        dir_path = base_path + i.strftime("%Y-%m-%d")
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        df_state[df_state['Date'] == i][
            ['Province_State', 'Confirmed', 'Deaths', 'Daily_Confirmed', 'Daily_Deaths']].to_csv(
            dir_path + '/covid_19_state.csv', index=False)
        df[df['Date'] == i][
            ['FIPS', 'Province_State', 'Admin2', 'Confirmed', 'Deaths', 'Daily_Confirmed', 'Daily_Deaths']].to_csv(
            dir_path + '/covid_19_county.csv', index=False)

def loadData():
    print('[INFO] Fetching Data...')
    df = readData()
    df["Admin2"] = df["Admin2"].fillna(df["Province_State"])
    df_state = df.groupby(["Province_State", "Date"]).sum().reset_index()
    df_state = df_state[["Province_State","Date","Confirmed","Deaths","Daily_Confirmed","Daily_Deaths"]]
    print('[INFO] Processing timeseries data...')
    getTimeSeriesData(df, df_state)
    print('[INFO] Printing csv data...')
    df.to_csv('data/covid_19_county.csv', index=False)
    df_state.to_csv('data/covid_19_state.csv', index=False)
    print('[INFO] Printing json data...')
    jsonOutput(df_state, 'state')
    jsonOutput(df, 'county')
    print('[INFO] Done.')

if __name__ == '__main__':
    loadData()