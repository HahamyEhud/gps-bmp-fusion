import pandas as pd
import numpy as np

def convert_raw_data(raw_data_array):
    '''
    Author: Ehud Hahamy
    Date: 2018-07-29
    Synopsis: format raw data for numpy use
    Input:
     raw_data_array: 2-by-N list, one column for timestamps, the other of time-series values [list of dicts][timestamps, float]
    Output:
     ts_values_arr: array of time series values [1D numpy array][float]
     t_sec_arr: array of numerical time values with respect to the first recorded timestamp [1D numpy array][float]
     padded_timestamp_range: a gap-free timestamps array ranging from first to last timestamps
        in raw_data_array [1D numpy array][np.datetime64]
    '''

    frame = pd.DataFrame(raw_data_array)
    cols = frame.columns
    is_timestamp = cols == 'event_timestamp'
    frame.columns.values[np.logical_not(is_timestamp)] = 'ts_values'
    ts_values_arr = frame['ts_values'].values
    t_sec_arr = frame['event_timestamp'].values
    t_sec_arr = (t_sec_arr - t_sec_arr[0])/np.timedelta64(1, 's')
    padded_timestamp_range = pd.date_range(start=raw_data_array[0]['event_timestamp'],
                                           end=raw_data_array[-1]['event_timestamp'],
                                           freq='1s').values

    return {
        'ts_values_arr': ts_values_arr,
        't_sec_arr': t_sec_arr,
        'padded_timestamp_range': padded_timestamp_range
    }




