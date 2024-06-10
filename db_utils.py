import yaml
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np

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
    df: pandas dataframe
        This is the dataframe to be modifed by the class, this was obatained from the csv file produced by the previous file.
        The file was returned as a dataframe by a previous function in this file.

    Attributes:
    ----------
    df: pandas dataframe
        Check Parameters section.

    Methods:
    ----------
    change_data_type_category(df)
        This function changes the data types of the following columns to category:
        Change TERM, GRADE, SUB_GRADE, EMPLOYMENT_LENGTH, HOME_OWNERSHIP, VERIFICATION_STATUS, LOAN_STATUS, PAYMENT_PLAN, PURPOSE, APPLICATION_TYPE to category.
    change_data_type_datetime(df)
        This function changes the data types of the following columns to datetime64:
        Change ISSUE_DATE, EARLIEST_CREDIT_LINE, LAST_PAYMENT_DATE, NEXT_PAYMENT_DATE, LAST_CREDIT_PULL_DATE to datetime64.
    """

    # Class constructor
    def __init__(self, df):
        self.df = df

    # Methods
    def change_data_type_category(self, df):
        for column in ["term", "grade", "sub_grade", "employment_length", "home_ownership", "verification_status", "loan_status", "payment_plan", "purpose", "application_type"]:
            df[column] = df[column].astype("category")
        return df
    def change_data_type_datetime(self, df):
        for column in ["issue_date", "earliest_credit_line", "last_payment_date", "next_payment_date", "last_credit_pull_date"]:
            df[column] = pd.to_datetime(df[column], format = "%d/%m/%Y")
        return df

payments_df = DataTransform(csv_to_df()).change_data_type_category(csv_to_df())
payments_df = DataTransform(payments_df).change_data_type_datetime(payments_df)


class DataFrameInfo:
    """
    This class defines some methods that can be used to get information from the dataframe.

    Parameters:
    ----------
    df: pandas dataframe
        This is the dataframe which information will be obtained from.

    Attributes:
    ----------
    df: pandas dataframe
        Check Parameters section.

    Methods:
    ----------
    df_describe_data(df)
        This function returns a variety of information about the dataframe.
        For numerical data these are: count, mean, standard deviation, min, max, lower/upper bounds, median.
        For object data these are: count, unique, top and frequency. (Timestamps include first and last.)
    df_mode(df)
        This function returns the mode for each column in the dataframe.
    df_shape(df)
        This function returns the shape (size) of the dataframe.
    df_null_count(df)
        This function returns the null count (number of missing values) for each colum in the dataframe.

    The above methods can also be used on specific columns of the dataframe if only data for some is required.
    """

    # Class constructor
    def __init__(self, df):
        self.df = df

    # Methods
    def df_describe_data(self, df):
        return df.describe()
    def df_mode(self, df):
        return df.mode()
    def df_shape(self, df):
        return df.shape
    def df_null_count(self, df):
        return df.isnull().sum()
    
DataFrameInfo(payments_df).df_shape(payments_df)
# There are 54231 rows of data.
DataFrameInfo(payments_df).df_null_count(payments_df)
# Rows to drop: mths_since_last_delinq (31002 NULL), mths_since_last_record (48050 NULL), next_payment_date (32608 NULL), mths_since_last_major_derog (46732 NULL).
payments_df = payments_df.drop(["mths_since_last_delinq", "mths_since_last_record", "next_payment_date", "mths_since_last_major_derog"], axis = 1)
DataFrameInfo(payments_df).df_shape(payments_df)
# 4 columns have been dropped

class Plotter:
    """
    This class defines some methods to plot information from the dataframe.

    Parameters:
    ----------
    df: pandas dataframe
        This is the dataframe which information will be obtained from.

    Attributes:
    ----------
    df: pandas dataframe
        Check Parameters section.

    Methods:
    ----------
    plot_null(df)
        This function plots a bar chart of the sum of null values for each column of the data frame.
    plot_data_boxplot(df)
        This function returns a boxplot to help visualise the data.
        This is best used for one column of the data frame at a time like: df["column name"].
    plot_data_line(df)
        This function returns a line graph to help visualise the data.
        This is best used for one column of the data frame at a time like: df["column name"].
    """

    # Class constructor
    def __init__(self, df):
        self.df = df
    
    # Methods
    def plot_null(self, df):
        df.isna().sum().plot(kind = "bar")
        plt.show()
    def plot_data_boxplot(self, df):
        df.plot(kind = "box")
        plt.show()
    def plot_data_line(self, df):
        df.plot()
        plt.show()

# Plotter(payments_df).plot_null(payments_df)
# The function above returns showing how many null values there are in each column.

class DataFrameTransform:
    """
    This class defines some methods to transform the data in the dataframe.

    Parameters:
    ----------
    df: pandas dataframe
        This is the dataframe which information will be obtained from.

    Attributes:
    ----------
    df: pandas dataframe
        Check Parameters section.

    Methods:
    ----------
    impute_missing(df)
        This function imputes missing values into the dataframe in the most appropriate way as follows:
        MEAN: funded_amount, int_rate
        MEDIAN: collections_12_mths_ex_med
        FORWARD FILL: last_payment_date, last_credit_pull_date
        MODE: term, employment_length
    reduce_skew(df)
        This function reduces the skew of some columns using either the log or square root transformations as follows:
        LOG: annual_inc, out_prncp, out_prncp_inv, total_rec_late_fee, recoveries, collection_recovery_fee, last_payment_amount.
        SQRT: delinq_2yrs, inq_last_6mths, total_rec_int.
    remove_outliers(df)
        This function removes outliers from the data as follows:
        OUTLIERS: instalment (remove above 1000), annual_inc (remove above 12.35 & under 9.70), delinq_2yrs (remove above 0), inq_last_6mths (remove above 2.5),
                  open_accounts (remove above 22), total_accounts (remove above 53.5), total_payment (remove above 31,850), total_payment_inv (remove above 31,500),
                  total_rec_prncp (remove above 24,870), total_rec_int (remove above 100), total_rec_late_fee (remove above 0), recoveries (remove above 0),
                  collection_recovery_fee (remove above 0), last_payment_amount (remove under 1.8).
        NO OUTLIERS: loan_amount, funded_amount, funded_amount_inv, int_rate, dti, out_prncp, out_prncp_inv, collections_12_mths_ex_med, policy_code.
    """

    # Class constructor
    def __init__(self, df):
        self.df = df

    # Methods
    def impute_missing(self, df):
        for column in ["funded_amount", "int_rate"]:
            df[column] = df[column].fillna(df[column]).mean()
        for column in ["collections_12_mths_ex_med"]:
            df[column] = df[column].fillna(df[column]).median()
        for column in ["last_payment_date", "last_credit_pull_date"]:
            df[column] = df[column].ffill()
        for column in ["term", "employment_length"]:
            df[column] = df[column].fillna(df[column]).mode()[0]
        return df
        
    def reduce_skew(self, df):
        for column in ["annual_inc", "out_prncp", "out_prncp_inv", "total_rec_late_fee", "recoveries", "collection_recovery_fee", "last_payment_amount"]:
            df[column] = np.log(df[column]+1)
        for column in ["delinq_2yrs", "inq_last_6mths", "total_rec_int"]:
            df[column] = np.sqrt(df[column])
        return df
        
    def remove_outliers(self, df):
        df = df[(df["instalment"] <= 1000) & (df["annual_inc"] <= 12.35) & (df["annual_inc"] >= 9.70) & (df["delinq_2yrs"] == 0) & (df["inq_last_6mths"] <= 2.5) &
                (df["open_accounts"] <= 22) & (df["total_accounts"] <= 53.5) & (df["total_payment"] <= 31850) & (df["total_payment_inv"] <= 31500) &
                (df["total_rec_prncp"] <= 24870) & (df["total_rec_int"] <= 100) & (df["total_rec_late_fee"] == 0) & (df["recoveries"] == 0) &
                (df["collection_recovery_fee"] == 0) & (df["last_payment_amount"] >= 1.8)]
        return df
        # OUTLIERS: instalment (remove above 1000), annual_inc (remove above 12.35 & under 9.70), delinq_2yrs (remove above 0), inq_last_6mths (remove above 2.5),
        #           open_accounts (remove above 22), total_accounts (remove above 53.5), total_payment (remove above 31,850), total_payment_inv (remove above 31,500),
        #           total_rec_prncp (remove above 24,870), total_rec_int (remove above 100), total_rec_late_fee (remove above 0), recoveries (remove above 0),
        #           collection_recovery_fee (remove above 0), last_payment_amount (remove under 1.8)
        # NO OUTLIERS: loan_amount, funded_amount, funded_amount_inv, int_rate, dti, out_prncp, out_prncp_inv, collections_12_mths_ex_med, policy_code.



payments_df = DataFrameTransform(payments_df).impute_missing(payments_df)
DataFrameInfo(payments_df).df_null_count(payments_df)
# There are now no NULL values in the data.
# Plotter(payments_df).plot_null(payments_df)
# When running the above function we can see the NULL values have all been removed.
payments_df.skew(numeric_only=True)
# Columns wih high SKEW (over 2): annual_inc, delinq_2yrs, inq_last_6mths, out_prncp, out_prncp_inv, total_rec_int, total_rec_late_fee, recoveries, collection_recovery_fee, last_payment_amount.
np.log(payments_df["last_payment_amount"]+1).skew()
np.sqrt(payments_df["last_payment_amount"]).skew()
new_payments_df = DataFrameTransform(payments_df).reduce_skew(payments_df)
new_payments_df.skew(numeric_only=True)
# When running the above function we can see that the columns' skewness has been reduced.
# Plotter(new_payments_df).plot_data_boxplot(new_payments_df["loan_amount"])
DataFrameInfo(new_payments_df).df_describe_data(new_payments_df["loan_amount"])
# Above 2 lines were used to identify outliers in the data.
new_payments_df = DataFrameTransform(new_payments_df).remove_outliers(new_payments_df)
DataFrameInfo(new_payments_df).df_shape(new_payments_df)
# Plotter(new_payments_df).plot_data_boxplot(new_payments_df["open_accounts"])
# When running the above function with different columns we can see that outliers have been removed.
new_payments_df.corr(numeric_only=True)
# Hihghly correlated columns to remove.
# loan_amount : funded_amount_inv, instalment, total_payment, total_payment_inv, total_rec_int
# out_prncp: out_prncp_inv
new_payments_df = new_payments_df.drop(["funded_amount_inv", "instalment", "total_payment", "total_payment_inv", "total_rec_int", "out_prncp_inv"], axis = 1)
DataFrameInfo(new_payments_df).df_shape(new_payments_df)
# When running the above function we can see that the 6 columns have been removed.
# Save the transformed data base to a csv file.
# new_payments_df.to_csv("transformed_data.csv")

# Milestone 4, Task 1
# total_payment, funded_amount_inv, funded_amount
def milestone4_task1():
    total_payment = payments_df["total_payment"].sum()
    funded_amount = payments_df["funded_amount"].sum()
    percentage_recovered = (total_payment / funded_amount) * 100
    print(f"The percentage of money recovered is{percentage_recovered}%")
    df = pd.DataFrame([total_payment, funded_amount])
    df.plot(kind = "bar", title="Amount paid back vs Amount funded")
    plt.show()
# milestone4_task1() - 91.3% of the loans have been recovered.

# Milestone 4, Task 2
# total_payment, loan_status, funded_amount
def milestone4_task2():
    charged_off_total = payments_df.loc[payments_df["loan_status"] == "Charged Off", "total_payment"].sum()
    charged_off_count = payments_df[(payments_df["loan_status"] == "Charged Off")].shape[0]
    print(f"The amount of charged off loans is {charged_off_count}")
    print(f"The amount of money paid towards these loans is £{round(charged_off_total, 2)}")
    percentage = round((charged_off_count/36408) * 100, 2)
    print(f"The percentage of charged off loans is {percentage}%")
# milestone4_task2() - 15.3% is the percetage of charged off loans, amount paid was £37,400,589.

# Milestone 4, Task 3
# total_payment, loan_status, funded_amount, last_payment_amount, term, issue_date, last_payment_date, int_rate
def milestone4_task3():
    payments_df["term"] = payments_df["term"].str.replace(r'\D', '', regex=True).astype(np.float64)
    payments_df["months_paid"] = (payments_df["last_payment_date"].dt.year - payments_df["issue_date"].dt.year) * 12 + (payments_df["last_payment_date"].dt.month - payments_df["issue_date"].dt.month)
    charged_off = payments_df[(payments_df["loan_status"] == "Charged Off")]
    payments_df["months_left"] = payments_df["term"] - payments_df["months_paid"]
    charged_off["revenue_lost"] = charged_off["last_payment_amount"]*pow(1+(charged_off["int_rate"]/100), (payments_df["months_left"]/12))
    revenue_lost_int = charged_off["revenue_lost"].sum()
    print(f"The amount of revenue lost on charged off loans due to interest is £{round(revenue_lost_int, 2)}")
    charged_off["unpaid_loss"] = charged_off["last_payment_amount"]*payments_df["months_left"]
    revenue_lost_total = charged_off["unpaid_loss"].sum() + revenue_lost_int
    print(f"The total amount lost is £{round(revenue_lost_total, 2)}")
# milestone4_task3() - £38,978.40 is lost due to interest, £680297.51 is lost overall.

# Milestone 4, Task 4
# total_payment, loan_status, funded_amount, last_payment_amount, term, issue_date, last_payment_date, int_rate
def milestone4_task4(revenue_lost_total):
    late_count = payments_df[(payments_df["loan_status"] == "Late (16-30 days)") | (payments_df["loan_status"] == "Late (31-120 days)")].shape[0]
    print(f"The number of late payments is {late_count}")
    percentage_late = round((late_count/36408) * 100, 2)
    print(f"The percentage of late payments out of the total is {percentage_late}%")
    payments_df["term"] = payments_df["term"].str.replace(r'\D', '', regex=True).astype(np.float64)
    payments_df["months_paid"] = (payments_df["last_payment_date"].dt.year - payments_df["issue_date"].dt.year) * 12 + (payments_df["last_payment_date"].dt.month - payments_df["issue_date"].dt.month)
    payments_df["months_left"] = payments_df["term"] - payments_df["months_paid"]
    late_payments = payments_df[(payments_df["loan_status"] == "Late (16-30 days)") | (payments_df["loan_status"] == "Late (31-120 days)")]
    late_payments["revenue_lost"] = late_payments["last_payment_amount"]*late_payments["months_left"]
    revenue_lost = late_payments["revenue_lost"].sum()
    print(f"The potential revenue loss if late customers were charged off is £{round(revenue_lost, 2)}")
    revenue_lost_total = revenue_lost_total + revenue_lost
    print(f"The potential revenue loss if late customers were charged off and current charged off customers is £{round(revenue_lost_total, 2)}")
# milestone4_task4(680297.51) - 1.88% of payments are late, £52,970.53 would be lost if late customers would be charged off, including already charged off customers this totals up to £733268.04.