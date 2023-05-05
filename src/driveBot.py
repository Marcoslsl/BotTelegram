from dotenv import load_dotenv
import gspread
import os
import json
import pandas as pd


load_dotenv()

class DriveBot:

    def __init__(self) -> None:
        self.gc = gspread.service_account(filename="credentials.json")


    def get_data(self):
        
        LINK_SHEET = os.getenv("LINK_SHEET")
        sh = self.gc.open_by_key(LINK_SHEET)
        worksheet = sh.sheet1
        dataframe = pd.DataFrame(worksheet.get_all_records())
        return dataframe
    