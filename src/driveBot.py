from dotenv import load_dotenv
from typing import Union
import gspread
import os
import json
import pandas as pd


load_dotenv()

class DriveBot:

    def __init__(self) -> None:
        self.gc = gspread.service_account(filename="credentials.json")


    def get_data(self) -> pd.DataFrame:
        
        LINK_SHEET = os.getenv("LINK_SHEET")
        sh = self.gc.open_by_key(LINK_SHEET)
        worksheet = sh.sheet1
        # numeric_ignore=["all"] no get_all_records 
        work_sheet = worksheet.get_all_records()
        dataframe = pd.DataFrame(work_sheet)
        dataframe['NPS interno'] = dataframe['NPS interno'].apply(
            DriveBot.transform_nps).astype("float")
        
        dataframe['Setor'] = dataframe['Setor'].replace(
            {'Engenheiro de Software': 'Engenharia de Software'}
            )
        return dataframe
    
    @staticmethod
    def transform_nps(value: Union[int, float]) -> str:
        if value > 10:
            str_value = str(value)
            str_value = str_value[0] + '.' + str_value[1]
            return str_value
        else:
            return str(value)
    