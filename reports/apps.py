from django.apps import AppConfig
import pandas as pd
import os


class ReportsConfig(AppConfig):
    name = 'reports'

    def ready(self):
        global sales_db
        xl = pd.ExcelFile(os.path.join(os.path.dirname(__file__), "data/SalesDataFull.xlsx"))
        sales_db = xl.parse('Orders')
        print("Setup connection to Sales database!")