# Exploratory Data Analysis: Customer Loans In Finance
This project is for the AiCore Data Analyst bootcamp. It is used to perform exploratory data analysis on a sample database.

## Installation instructions
This requires standard python installation. [WIP]

## Usage Instructions
[WIP]

## File structure
### 1. db_utils.py
This file contains several classes that have been used to work with the data.

1. RDSDatabaseConnector

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

2. DataTransform

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
    change_data_types(df)
        This function changes the data types of the columns as follows:
        Change TERM, GRADE, SUB_GRADE, EMPLOYMENT_LENGTH, HOME_OWNERSHIP, VERIFICATION_STATUS, LOAN_STATUS, PAYMENT_PLAN, PURPOSE, APPLICATION_TYPE to category.
        Change ISSUE_DATE, EARLIEST_CREDIT_LINE, LAST_PAYMENT_DATE, NEXT_PAYMENT_DATE, LAST_CREDIT_PULL_DATE to datetime64.
    """

3. DataFrameInfo

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

4. Plotter

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

5. DataFrameTransform

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

### 2. loan_payments.csv

This is the data obtained from the online database using the RDSDatabaseConnector class. This is the original form of the data.

## License Information
Standard license, the author of this repository is mihai0813.
