import pandas as pd

def calculate_monthly_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly averages and fill missing values."""
    monthly_columns = df.columns[3:15]
    monthly_averages = df[monthly_columns].mean()
    for col in monthly_columns:
        df.loc[:, col] = df[col].fillna(monthly_averages[col])
    return df

def calculate_yearly_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate yearly average and standard deviation."""
    monthly_columns = df.columns[3:15]
    df["Yearly Average"] = df[monthly_columns].mean(axis=1)
    df["Yearly StdDev"] = df[monthly_columns].std(axis=1)
    return df
