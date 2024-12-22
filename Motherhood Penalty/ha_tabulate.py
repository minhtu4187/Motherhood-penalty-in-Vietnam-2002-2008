import pandas as pd

pd.set_option('display.max_rows', None)

def tab(df, variable, include_all=False):
    """
    Tabulate a variable, with an option to include all possible values.

    Parameters:
    - df: The DataFrame containing the data.
    - variable: The column name of the variable to tabulate.
    - include_all: Boolean flag indicating whether to include all values or only observed ones.

    Returns:
    - A DataFrame with Value, Frequency, Percent, Cumulative Percent columns, a NaN row, and a total row.
    """
    if include_all:
        # Get all possible unique values including NaN
        unique_values = df[variable].unique()
        
        # Create a DataFrame to ensure all unique values are included
        all_values_df = pd.DataFrame({variable: unique_values})
        
        # Tabulate the variable, including NaN counts
        value_counts = df[variable].value_counts(dropna=False).reset_index()
        
        # Rename the columns for better readability
        value_counts.columns = ['Value', 'Frequency']
        
        # Merge with the all_values_df to ensure all values are present
        tabulation = pd.merge(all_values_df, value_counts, how='left', left_on=variable, right_on='Value')
        
        # Fill NaN frequencies with 0
        tabulation['Frequency'].fillna(0, inplace=True)
        
        # Drop the extra 'Value' column generated by the merge
        tabulation.drop(columns=[variable], inplace=True)
    else:
        # Tabulate only the observed values
        tabulation = df[variable].value_counts(dropna=False).reset_index()
        tabulation.columns = ['Value', 'Frequency']

    # Calculate the percentage
    tabulation['Percent'] = (tabulation['Frequency'] / tabulation['Frequency'].sum()) * 100
    
    # Calculate the cumulative percentage
    tabulation['Cumulative Percent'] = tabulation['Percent'].cumsum()
    
    # Add a row for NaN values
    nan_frequency = df[variable].isna().sum()
    
    nan_row = pd.DataFrame({
        'Value': [pd.NA],
        'Frequency': [nan_frequency],
        'Percent': [(nan_frequency / len(df)) * 100],
        'Cumulative Percent': [None]  # Not applicable for NaN row
    })
    
    # Add a total row
    total_frequency = tabulation['Frequency'].sum()
    
    total_row = pd.DataFrame({
        'Value': ['Total'],
        'Frequency': [total_frequency],
        'Percent': [100],
        'Cumulative Percent': [None]  # Cumulative percent is not relevant for the total
    })
    
    # Append the NaN row and the total row to the tabulation
    tabulation = pd.concat([tabulation, nan_row, total_row], ignore_index=True)

    return tabulation
