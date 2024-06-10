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