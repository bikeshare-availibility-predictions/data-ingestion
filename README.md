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

