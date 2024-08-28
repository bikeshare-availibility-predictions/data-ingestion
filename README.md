# data-ingestion
Data Ingestion Pipline for BikeShare availability and weather data.

## Data Collection

We collect real-time data every minute from all bike share stations in Toronto using the [City of Toronto's Open Data API](https://open.toronto.ca/dataset/bike-share-toronto/) and combine it with weather data from [OpenWeatherMap](https://openweathermap.org/city/6167865). The following data is stored:

- Station ID
- Time of query
- Number of bikes
- Number of Docks
- Logitude of Station
- Latitude of Station
- Current temperature
- Weather condition code (one of [these](https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2) OpenWeatherMap codes)

Currently, data is loaded into in an Azure SQL Server database, and the ingestion pipeline runs every minute via Azure Functions. In total, the dataset grows by slightly over 1 million records daily.

## Development
Create a python venv using 
`python3 -m venv venv`


Next, activate the venv
#### 💻 **Windows:**
```bash
venv\Scripts\activate
```
🍏 MacOS or Linux:
```bash
source venv/bin/activate
```

Finally, install the requirements using 
`pip install -r requirements.txt`

Refer to the [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python) documentation for further setup instructions
