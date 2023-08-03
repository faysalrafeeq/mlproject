# Aim is to read the data from any source
# Split the data into raw, train, test 
# log that in the logging file.


import os
# for exception sys
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# The dataclass hold the variables of a class and these variables are initialized without the 
# Init method. This will serve as the input to my data ingestion.

@dataclass
class DataIngestionConfig:
    # Define Variables 
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str  = os.path.join('artifacts','test.csv')
    raw_data_path : str = os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or components")
        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            # making a raw data csv file.
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info('Train test Split')
            train_set,test_set= train_test_split(df,test_size=0.2,random_state=42)
            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)
            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)

if __name__ =='__main__':
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data,test_data)
    Modeltrainer = ModelTrainer()
    print ( Modeltrainer.initiate_model_trainer(train_arr,test_arr) )