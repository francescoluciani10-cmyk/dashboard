# transformations.py
import pandas as pd

def pivot_long_to_wide(df, index, columns, values):
    """
    Converte un DataFrame da formato long a wide.
    df: DataFrame con colonne index, columns e values
    """
    return df.pivot(index=index, columns=columns, values=values).reset_index()
