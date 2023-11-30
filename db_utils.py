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


def csv_to_df():
    with open("loan_payments.csv", "r") as payments:
        payments_df = pd.read_csv(payments)
        return payments_df

class DataTransform:
    """
    Transforms the data types of the columns in the dataframe.

    Parameters:
    ----------
    payments_df: pandas dataframe
        This is the dataframe to be modifed by the class, this was obatained from the csv file produced by the previous file.
        The file was returned as a dataframe by a previous function in this file.

    Attributes:
    ----------
    payments_df: pandas dataframe
        Check Parameters section.

    Methods:
    ----------
    change_data_types(payments_df)
        This function changes the data types of the columns as required.
    """

    # Class constructor
    def __init__(self, payments_df):
        self.payments_df = payments_df

    # Methods
    def change_data_types(self, payments_df):
        for column in ["term", "grade", "sub_grade", "employment_length", "home_ownership", "verification_status", "loan_status", "payment_plan", "purpose", "application_type"]:
            payments_df[column] = payments_df[column].astype("category")
        for column in ["issue_date", "earliest_credit_line", "last_payment_date", "next_payment_date", "last_credit_pull_date"]:
            payments_df[column] = pd.to_datetime(payments_df[column], format = "%d/%m/%Y")
        return payments_df
        # Change TERM, GRADE, SUB_GRADE, EMPLOYMENT_LENGTH, HOME_OWNERSHIP, VERIFICATION_STATUS, LOAN_STATUS, PAYMENT_PLAN, PURPOSE, APPLICATION_TYPE to category.
        # Change ISSUE_DATE, EARLIEST_CREDIT_LINE, LAST_PAYMENT_DATE, NEXT_PAYMENT_DATE, LAST_CREDIT_PULL_DATE to datetime64.


payments_df = DataTransform(csv_to_df()).change_data_types(csv_to_df())


class DataFrameInfo:
    """
    This class defines some methods that can be used to get information from the dataframe.

    Parameters:
    ----------
    payments_df: pandas dataframe
        This is the dataframe which information will be obtained from.

    Attributes:
    ----------
    payments_df: pandas dataframe
        Check Parameters section.

    Methods:
    ----------
    df_describe_data(payments_df)
        This function returns a variety of information about the dataframe.
        For numerical data these are: count, mean, standard deviation, min, max, lower/upper bounds, median.
        For object data these are: count, unique, top and frequency. (Timestamps include first and last.)
    df_mode(payments_df)
        This function returns the mode for each column in the dataframe.
    df_shape(payments_df)
        This function returns the shape (size) of the dataframe.
    df_null_count(payments_df)
        This function returns the null count (number of missing values) for each colum in the dataframe.

    The above methods can also be used on specific columns of the dataframe if only data for some is required.
    """

    # Class constructor
    def __init__(self, payments_df):
        self.payments_df = payments_df

    # Methods
    def df_describe_data(self, payments_df):
        return payments_df.describe()
    def df_mode(self, payments_df):
        return payments_df.mode()
    def df_shape(self, payments_df):
        return payments_df.shape()
    def df_null_count(self, payments_df):
        return payments_df.isnull().sum()
