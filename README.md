# COVID19_Data

Auto fetching data from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) with github schedule action. Processing with python script to get both csv data and json data.

```python
import pandas as pd

# fetching county covid-19 data
df = pd.read_csv('https://raw.githubusercontent.com/lit26/COVID19_Data/main/data/covid_19_county.csv')
# fetching state covid-19 data
df = pd.read_csv('https://raw.githubusercontent.com/lit26/COVID19_Data/main/data/covid_19_state.csv')
```
