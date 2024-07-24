import logging
import azure.functions as func
from src.extract_and_transform import BikeShareDataSource, BikeShareDataSourceConfig
from src.load import DataLoader

app = func.FunctionApp()

@app.schedule(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')    

    data_source_config = BikeShareDataSourceConfig()
    data_source = BikeShareDataSource(data_source_config)
    data = data_source.fetch_bike_data()
    data_loader = DataLoader()
    data_loader.load_data_into_storage(data)

