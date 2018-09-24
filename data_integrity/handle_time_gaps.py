import numpy as np
import pandas as pd
import configurations as cnf

# Example Data
# t_sec_unique_arr = np.array([0.0,1,2,  5,6,  8,9,10,  19,20])
# vals_arr = np.array([np.nan,0,3,7,1,1,1,3,0,np.nan])
# params = cnf.load_parameters()

def handle_time_gaps(t_sec_unique_arr,vals_arr, params):
    gap_detection_dict = detect_time_gaps(t_sec_unique_arr, vals_arr, params)
    filled_values_dict = fill_missing_values(gap_detection_dict['padded_time_arr'],
                         gap_detection_dict['padded_vals_arr'],
                         gap_detection_dict['gap_boundaries_mat'],params)

    return{
        'gap_detection_dict': gap_detection_dict,
        'filled_values_dict': filled_values_dict
    }

def detect_time_gaps(t_sec_unique_arr, vals_arr, params):
    '''
    Author: Ehud Hahamy
    Date: 2018-07-17
    Synopsis: Format time and values array, locate time gaps from recording miss or
                time gap and compute total time gap statistics
    Input:
     t_sec_unique_arr: strictly increasing numerical times [numpy 1D array][float][sec]
     vals_arr: array of len(t_sec_unique_arr); resp. values. May be NaNs.
        [numpy 1D array][float][time series units]
    Params:
     time_step [scalar][float][sec]
    Output:

    '''

    # Build nan-padded arrays
    padded_arr_len = int((t_sec_unique_arr[-1]-t_sec_unique_arr[0]+1)/params['time_step'])
    padded_time_arr = np.linspace(t_sec_unique_arr[0],t_sec_unique_arr[-1],padded_arr_len)
    padded_vals_arr = np.empty(len(padded_time_arr))*np.nan

    t_sec_idxs = (t_sec_unique_arr - t_sec_unique_arr[0])/params['time_step']
    t_sec_idxs = np.asarray(t_sec_idxs, int)
    padded_vals_arr[t_sec_idxs] = vals_arr

    # Identify nan switches
    is_nan_padded_vals_arr = np.isnan(padded_vals_arr)
    nan_switch_arr = np.diff(np.asarray(is_nan_padded_vals_arr,int))

    is_padded_vals_nan_begins = nan_switch_arr == 1
    if is_nan_padded_vals_arr[0]:
        is_padded_vals_nan_begins = np.insert(is_padded_vals_nan_begins[1:],0,np.array([True,False]))
    else:
        is_padded_vals_nan_begins = np.insert(is_padded_vals_nan_begins,0,False)
    padded_vals_nan_begin_idxs = np.asarray(np.where(is_padded_vals_nan_begins)).flatten()

    is_padded_vals_nan_ends = nan_switch_arr == -1
    if is_nan_padded_vals_arr[-1]:
        is_padded_vals_nan_ends = np.append(is_padded_vals_nan_ends[:-1],np.array([False,True]))
    else:
        is_padded_vals_nan_ends = np.append(is_padded_vals_nan_ends, False)
    padded_vals_nan_end_idxs = np.asarray(np.where(is_padded_vals_nan_ends)).flatten()

    gap_boundaries_mat = np.stack((padded_vals_nan_begin_idxs, padded_vals_nan_end_idxs))
    gap_lengths = np.diff(gap_boundaries_mat,axis = 0).flatten()+1
    gap_lengths_counts = np.bincount(gap_lengths)
    val_range = np.arange(len(gap_lengths_counts))
    is_length_count = gap_lengths_counts > 0
    gap_lengths_stats = {'seq_len': val_range[is_length_count],
                       'num_seqs': gap_lengths_counts[is_length_count]}

    return{
        'padded_time_arr': padded_time_arr,
        'padded_vals_arr': padded_vals_arr,
        't_sec_idxs': t_sec_idxs,
        'gap_boundaries_mat': gap_boundaries_mat,
        'gap_lengths_stats': gap_lengths_stats
    }

#
def fill_missing_values(padded_time_arr, padded_vals_arr,gap_boundaries_mat,params):
    '''
    Author: Ehud Hahamy
    Date: 2018-07-23
    Input:
        padded_time_arr: array of numerical time values; may contain gaps [numpy 1D array][sec]
        padded_vals_arr: array of time series values of length len(padded_time_arr); may contain np.nan values
    Output:
        filled_vals_arr: array of length len(padded_time_arr). Values filled by interpolation.
            Edge gaps filled by forward/backward completion to nearest neighbor.
    '''
    ser = pd.Series(padded_vals_arr)
    ser.reindex(padded_time_arr)
    # Completion by interpolation at interior, nearest neighbor near edges.
    ser = ser.interpolate(method='linear',axis=0).ffill().bfill()
    filled_vals_arr = ser.values

    sz = gap_boundaries_mat.shape
    gap_lengths = np.diff(gap_boundaries_mat,axis = 0).flatten()+1

    for k in range(sz[1]):
        if gap_lengths[k] > params['gap_duration_thresh']:
            filled_vals_arr[gap_boundaries_mat[0,k]:gap_boundaries_mat[1,k]] = np.nan


    return {
        'filled_vals_arr': filled_vals_arr
    }




# Check Outputs:
# u = detect_time_gaps(t_sec_unique_arr, vals_arr, params)
# v = fill_missing_values(u['padded_time_arr'], u['padded_vals_arr'],u['gap_boundaries_mat'])
# w = handle_time_gaps(t_sec_unique_arr,vals_arr, params)
# print(1)



# Version without pandas - incomplete
# def fill_missing_values(padded_time_arr, padded_vals_arr, gap_boundaries_mat):
#
#     sz = len(gap_boundaries_mat)
#     for k in range(sz):
#         if gap_boundaries_mat[0,k] == 0:
#             padded_vals_arr[0:gap_boundaries_mat[1,k]] = padded_vals_arr[gap_boundaries_mat[1,k]+1]
#         elif gap_boundaries_mat[0,k] > 0 or gap_boundaries_mat[1,-1] < sz:
#             init = gap_boundaries_mat[0,k]-1
#             final = gap_boundaries_mat[1,k]+1
#             delta_vals = np.diff(padded_vals_arr[[init,final]])
#             delta_times = np.diff(padded_time_arr[gap_boundaries_mat[:,k]])
#             slope = delta_vals/delta_times
#             intercept = padded_vals_arr[gap_boundaries_mat[0,k]]






