import pandas as pd

def calculate_distance_matrix(df):
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    distance_matrix = distance_matrix + distance_matrix.T
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0
    return distance_matrix


def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = df.melt(id_vars=['id_start'], var_name='id_end', value_name='distance')
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_distance
    result_df = df.groupby('id_start').filter(lambda x: abs(x['distance'].mean() - reference_distance) <= threshold)
    return result_df


def calculate_toll_rate(df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    df['toll_rate'] = df['distance'] * 0.1 
    return df


def calculate_time_based_toll_rates(df):
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """

    df['time_based_toll'] = df['distance'] * 0.05  
    return df


df = pd.read_csv(r'C:\Users\BALA GANESH\AnalystTasksofBalaGanesh\submissions\dataset-3.csv')
print(calculate_distance_matrix(df))
print(unroll_distance_matrix(df))
reference_id=int(input())
print(find_ids_within_ten_percentage_threshold(df, reference_id))
print(calculate_toll_rate(df))
print(calculate_time_based_toll_rates(df))