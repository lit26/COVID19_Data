# COVID19_Data

Auto fetching data from Johns Hopkins with github schedule action. Processing with python script.

```python
import pandas as pd

# fetching county covid-19 data
df = pd.read_csv('https://raw.githubusercontent.com/lit26/COVID19_Data/main/data/covid_19_county.csv')
# fetching state covid-19 data
df = pd.read_csv('https://raw.githubusercontent.com/lit26/COVID19_Data/main/data/covid_19_state.csv')
```