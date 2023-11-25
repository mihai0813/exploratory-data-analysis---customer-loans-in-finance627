import yaml
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def credentials():
    with open("credentials.yaml", "r") as stream:
        try:
            cred = yaml.safe_load(stream)
            return cred
        except yaml.YAMLError:
            print(yaml.YAMLError)

class RDSDatabaseConnector:

    # Class constructor
    def __init__(self, cred):
        self.cred = cred
        
    # Methods
    def SQLAlchemy(self, cred):
        engine = create_engine(f"postgresql+psycopg2://{self.cred["RDS_USER"]}:{self.cred["RDS_PASSWORD"]}@{self.cred["RDS_HOST"]}:{self.cred["RDS_PORT"]}/{self.cred["RDS_DATABASE"]}")
        return engine
    
    def extract_data(self, engine):
        sql_query = pd.read_sql_table("loan_payments", engine)
        loan_payments = pd.DataFrame(sql_query)
        return loan_payments

    def save_csv(self, loan_payments):
        return loan_payments.to_csv("loan_payments.csv")

db = RDSDatabaseConnector(credentials())
db.SQLAlchemy(credentials())
db.extract_data(db.SQLAlchemy(credentials()))
db.save_csv(db.extract_data(db.SQLAlchemy(credentials())))