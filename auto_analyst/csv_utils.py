import pandas as pd
import re

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the column names of the dataframe
    """
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_", regex=False)
    df.columns = df.columns.str.replace("-", "_", regex=False)
    df.columns = df.columns.str.replace("(", "", regex=False)
    df.columns = df.columns.str.replace(")", "", regex=False)
    df.columns = df.columns.str.replace("/", "_", regex=False)
    df.columns = df.columns.str.replace(".", "_", regex=False)
    df.columns = df.columns.str.replace(",", "", regex=False)
    df.columns = df.columns.str.replace("'", "", regex=False)
    df.columns = df.columns.str.replace("?", "", regex=False)
    df.columns = df.columns.str.replace(":", "", regex=False)
    df.columns = df.columns.str.replace(";", "", regex=False)
    df.columns = df.columns.str.replace("!", "", regex=False)
    df.columns = df.columns.str.replace("=", "", regex=False)
    df.columns = df.columns.str.replace("%", "", regex=False)
    df.columns = df.columns.str.replace("$", "", regex=False)
    df.columns = df.columns.str.replace("#", "", regex=False)
    df.columns = df.columns.str.replace("@", "", regex=False)
    df.columns = df.columns.str.replace("&", "", regex=False)
    df.columns = df.columns.str.replace("*", "", regex=False)
    df.columns = df.columns.str.replace("+", "", regex=False)
    df.columns = df.columns.str.replace(">", "", regex=False)
    df.columns = df.columns.str.replace("<", "", regex=False)
    df.columns = df.columns.str.replace("0", "", regex=False)
    df.columns = df.columns.str.replace("1", "", regex=False)
    df.columns = df.columns.str.replace("2", "", regex=False)
    df.columns = df.columns.str.replace("3", "", regex=False)
    df.columns = df.columns.str.replace("4", "", regex=False)
    df.columns = df.columns.str.replace("5", "", regex=False)
    df.columns = df.columns.str.replace("6", "", regex=False)
    df.columns = df.columns.str.replace("7", "", regex=False)
    df.columns = df.columns.str.replace("8", "", regex=False)
    df.columns = df.columns.str.replace("9", "", regex=False)  
    return df

def clean_column_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the column types of the dataframe
    """
    return df.convert_dtypes()

def clean_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the date columns of the dataframe
    """
    for column in df.columns:
        if df[column].dtype != "int":
            try:
                df[column] = pd.to_datetime(df[column])
            except:
                pass
    return df


def clean_currency(val):
    """Convert a currency string to a float."""
    # Remove any commas or spaces from the string
    val = re.sub(r"[^\d\.\-+]", "", val)
    # Convert the string to a float
    return float(val)

def clean_currency_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the currency columns of the dataframe
    """
    for col in df.columns:
        # Check if any value in the column contains a currency symbol
        if any(isinstance(val, str) and re.search(r"[$₹£€]", val) for val in df[col]):
            # Convert the column to a float using the clean_currency function
            df[col] = df[col].apply(clean_currency)
    return df

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    return clean_currency_columns(
        clean_date_columns(
            clean_column_types(
                clean_columns(df)
            )
        )
    )