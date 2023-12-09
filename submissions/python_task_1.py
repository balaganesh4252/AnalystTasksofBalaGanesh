import pandas as pd

def generate_car_matrix(df):
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
    return car_matrix

def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    type_counts = df['car'].value_counts().to_dict()
    return type_counts

def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    bus_mean = df['bus'].mean()
    df.reset_index(drop=True, inplace=True) 
    high_bus_indexes = df.loc[df['car'] == 'bus'].loc[df['bus'] > 2 * bus_mean].index.tolist()
    return high_bus_indexes

def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    avg_truck_values = df.groupby('route')['truck'].mean()
    routes_above_threshold = avg_truck_values[avg_truck_values > 7].index.tolist()
    return routes_above_threshold

def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 2 if x > 5 else x)
    return modified_matrix

def time_check(df):
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['startTime'] = pd.to_datetime(df['startTime'])
    df['endTime'] = pd.to_datetime(df['endTime'])
    df['startDay_of_week'] = df['startTime'].dt.dayofweek
    df['startTime'] = df['startTime'].dt.time
    df['endDay_of_week'] = df['endTime'].dt.dayofweek
    df['endTime'] = df['endTime'].dt.time
    start_time = pd.to_datetime('00:00:00').time()
    end_time = pd.to_datetime('23:59:59').time()
    completeness_check = df.groupby(['id', 'id_2']).apply(
        lambda x: (x['startTime'].min() == start_time) and (x['endTime'].max() == end_time) and 
                  (set(x['startDay_of_week']) == set(range(7))) and (set(x['endDay_of_week']) == set(range(7)))
    )
    return completeness_check

df=pd.read_csv(r'C:\Users\BALA GANESH\AnalystTasksofBalaGanesh\submissions\dataset-1.csv')
df1=pd.read_csv(r'C:\Users\BALA GANESH\AnalystTasksofBalaGanesh\submissions\dataset-2.csv')
print(generate_car_matrix(df))
print(get_type_count(df))
print(get_bus_indexes(df))
print(filter_routes(df))
print(multiply_matrix(df))
print(time_check(df1))