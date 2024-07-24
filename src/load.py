import pandas as pd
import pyodbc
import os

class BikeShareDatabaseConfig:
    def __init__(self):
        self.server = os.getenv('Server')
        self.database = os.getenv('Database')
        self.username = os.getenv('UID')
        self.password = os.getenv('PWD')
        self.driver = os.getenv('Driver')
        self.table_name = os.getenv('TableName')

class DataLoader:
    """Functionality to load data into storage."""

    def __init__(self):
        self._config = BikeShareDatabaseConfig() 

    def load_data_into_storage(self, data: pd.DataFrame) -> None:
        """Load the rows from data into the storage."""
        conn = pyodbc.connect('DRIVER='+self._config.driver+';SERVER=tcp:'+self._config.server+';PORT=1433;DATABASE='+self._config.database+';UID='+self._config.username+';PWD='+ self._config.password)
        cursor = conn.cursor()

        INSERT_QUERY = f"""
            INSERT INTO 
            {self._config.table_name} (StationID, Time, NumBikes, NumDocks, Latitude, Longitude, Temperature, WeatherStatus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Iterate over DataFrame rows and insert each row into the SQL table
        for _, row in data.iterrows():
            cursor.execute(INSERT_QUERY, 
                           row['StationID'],
                           row['Time'], 
                           row['NumBikes'], 
                           row['NumDocks'], 
                           row['Latitude'], 
                           row['Longitude'], 
                           row['Temperature'],
                           row['WeatherStatus'])

        # Commit the transaction to save the changes
        conn.commit()
