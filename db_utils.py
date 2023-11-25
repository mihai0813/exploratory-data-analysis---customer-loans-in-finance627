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
    """
    Extracts the remote database to a csv on the local machine.

    Parameters:
    ----------
    cred: dictionary
        These are the database credentials obtained from the credentials.yaml file.
        They have been converted to a dictionary by a previous function in this file.

    Attributes:
    ----------
    cred: dictionary
        Check Parameters section.
    engine: engine
        Database obtained from the SQLAlchemy method below.
    loan_payments: pd.DataFrame
        Pandas dataframe obtained from the extract_data method below.

    Methods:
    ----------
    SQLAlchemy(cred)
        Imports the RDS database using the credentials. Returns "engine".
    extract_data(engine)
         Converts the database to a pandas data frame. Returns the data frame "loan_payments".
    save_csv(loan_payments)
        Saves the previously obtained data frame to the current directory as a csv file.
    """

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