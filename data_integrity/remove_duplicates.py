import numpy as np
# t_sec = format_out['t_sec_rsp_begin']

# Example Data
# t_sec = np.array([0,0,1,2,3,3,3,4,5,5,8,8,8,9,9,10,10])
# ts_values = np.arange(len(t_sec))
# ts_values[1] = ts_values[0]
# ts_values[-2]=ts_values[-1]

t_sec = np.array([0,1,2])
ts_values = np.array([4,5,6])

def build_unique_time_arr(t_sec,ts_values):
    '''
    Author: Ehud Hahamy
    Date: 2018-07-12
    Input:
        t_sec [numpy array][float][sec]
    Output:
        t_sec_unique [numpy array][float][sec]
        dup_boundaries [numpy 2D array][float][sec]
        dup_lengths_tbl [dict]
            seq_len - duplicate sequences lengths [numpy array][float][sec]
            num_seqs - num of occurrence of each length [numpy array][float][sec]
    '''

    # Build unique time array
    is_dt_sec_arr = np.diff(t_sec).astype(np.bool)
    is_unique_arr = np.insert(is_dt_sec_arr, 0, True)
    t_sec_unique_arr = t_sec[is_unique_arr]


    # Detect duplicate sequences
    is_unique_begin_arr = is_unique_arr[:-1]
    is_unique_end_arr = is_unique_arr[1:]

    is_dup_begin_arr = np.logical_and(is_unique_begin_arr, np.logical_not(is_unique_end_arr))
    is_dup_begin_arr = np.append(is_dup_begin_arr,False)
    is_dup_end_arr = np.logical_and(np.logical_not(is_unique_begin_arr),is_unique_end_arr)
    is_dup_end_arr = np.append(is_dup_end_arr,not is_unique_arr[-1])

    # Build duplicate sequences boundary indices matrix
    dup_begins_idxs = np.where(is_dup_begin_arr)
    dup_begins_idxs = np.asarray(dup_begins_idxs).flatten()
    dup_ends_idxs = np.where(is_dup_end_arr)
    dup_ends_idxs = np.asarray(dup_ends_idxs).flatten()
    dup_boundaries_mat = np.stack((dup_begins_idxs,dup_ends_idxs))

    # Duplicate sequences length descriptive statistics
    dup_seq_lengths = np.diff(dup_boundaries_mat,axis=0)+1
    dup_lengths_counts = np.bincount(dup_seq_lengths[0])
    val_range = np.arange(len(dup_lengths_counts))
    is_length_count = dup_lengths_counts > 0
    dup_lengths_stats = {'seq_len': val_range[is_length_count],
                       'num_seqs': dup_lengths_counts[is_length_count]}

    # Apply rule to select value to duplicates


    for k in range(dup_boundaries_mat.shape[1]):
        dup_timestamp_values = ts_values[dup_boundaries_mat[0,k]:dup_boundaries_mat[1,k]]
        ts_values[dup_boundaries_mat[0,k]] = duplicate_timestamp_value_selection(dup_timestamp_values)

    ts_values_unique_arr = ts_values[is_unique_arr]


    return {
        't_sec_unique': t_sec_unique_arr,
        'ts_values_unique': ts_values_unique_arr,
        'dup_boundaries_mat': dup_boundaries_mat,
        'dup_lengths_stats': dup_lengths_stats
    }


def duplicate_timestamp_value_selection(values):
    '''
    Áuthor: Ehud Hahamy
    Date: 2018-07-16
    Synopsis: Rule for selecting a number from a tupe
    Input:
        values [numpy 1D array][float]
    Ouput:
        values[0] [scalar][float]
    '''
    return values[0]


u = build_unique_time_arr(t_sec,ts_values)





