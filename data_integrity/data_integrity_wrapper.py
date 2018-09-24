import sys
sys.path.append('../db_reads')
import download_signal as dnl

import configurations as cnf
import format_data as fd
import remove_duplicates as rd
import handle_time_gaps as htg
# import loading_data as dnl
import matplotlib.pyplot as plt
# from sig_cleanup import build_unique_time_array

def cleanup_scheme():
    params = cnf.load_parameters()
    raw_data_array = dnl.signal_download()
    formatted_data_array = fd.convert_raw_data(raw_data_array)
    unique_data_dict = rd.build_unique_time_arr(formatted_data_array['t_sec_arr'],formatted_data_array['ts_values_arr'])
    time_gaps_dict = htg.detect_time_gaps(unique_data_dict['t_sec_unique'],
                        unique_data_dict['ts_values_unique'],
                        params)
    # times = frame['event_timestamp']
    # values = frame['ts_values']
    # dup_ts = pd.Series(data=values.values, index=times.values)
    # grouped = dup_ts.groupby(level=0)
    # group_counts = grouped.count()
    # fig = plt.figure()
    # ax1 = fig.add_subplot(2,1,1)
    # plt.plot(group_counts.values)
    # ax2 = fig.add_subplot(2,1,2)
    # ax2.hist(group_counts,bins=100)
    # ticks = ax2.set_xticklabels(np.ara)
    # plt.show()

    # ascending_sorted_time_array = list(map(lambda x: x['event_timestamp'], numerical_raw_data))
    # time_arr_unique = build_unique_time_array(ascending_sorted_time_array)


    return {
        'unique_data_dict': unique_data_dict,
        'time_gaps_dict': time_gaps_dict
    }


out = cleanup_scheme()
# print(out[0:5])
