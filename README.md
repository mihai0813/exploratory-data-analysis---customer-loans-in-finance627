# Exploratory Data Analysis: Customer Loans In Finance
This project is for the AiCore Data Analyst bootcamp. It is used to perform exploratory data analysis on a sample database.

## Installation instructions
This requires standard python installation. [WIP]

## Usage Instructions
[WIP]

## File structure
### 1. db_utils.py
This file contains the class RDSDatabaseConnector used to extract the data from the RDS dabatase onto the local machine as a csv file.

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

## License Information
Standard license, the author of this repository is mihai0813.
