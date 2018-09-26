#import sys
#sys.path.append('../data_integrity')
#import download_signal as dnl
import datetime
import pandas as pd
import pymysql

################
# Configurations
################
def generate_signal_configs_list():
    device = 'he00001'
    begin_time = datetime.datetime(2018, 9, 16, 6, 0, 0)
    date_diff = datetime.timedelta(days = 1)
    hours_diff = datetime.timedelta(hours = 13)
    local_to_utc_offset = datetime.timedelta(hours = -3)

    return [{'device': device,
            'local_begin_datetime': begin_time + i*date_diff,
            'local_end_datetime': begin_time + i*date_diff + hours_diff,
            'utc_begin_datetime': begin_time + i*date_diff + local_to_utc_offset,
            'utc_end_datetime': begin_time + i*date_diff + hours_diff + local_to_utc_offset,
            'utc_time_begin': pd.Timestamp(begin_time + i*date_diff + local_to_utc_offset).value//10**9,
            'utc_time_end': pd.Timestamp(begin_time + i*date_diff + hours_diff + local_to_utc_offset).value // 10**9}
            for i in range(6)]

def connection_configurations():
    return {
    'host': 'vnmysql.c4a62i7b81an.us-east-2.rds.amazonaws.com',
    'user': 'vndbroot',
    'password': 'AkuoKfo321!',
    'db': 'vndb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
    }

def load_parameters():
    '''Signal-independent parameters'''
    return {
        'time_step': 1.0,
        'gap_duration_thresh': 5.0
    }

def signal_download(signal_config):
    connection_config = connection_configurations()
    connection = pymysql.connect(host=connection_config['host'],
                                 user=connection_config['user'],
                                 password=connection_config['password'],
                                 db=connection_config['db'],
                                 charset=connection_config['charset'],
                                 cursorclass=connection_config['cursorclass']
                                 )
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT event_timestamp, bmp_alt, gps_alt' \
                  ' FROM hawkeye_rawdata' \
                  ' WHERE event_timestamp > "{0}"' \
                  ' AND event_timestamp < "{1}"'\
                  ' AND device_sn = "{2}"'.format(signal_config['begin_date'], signal_config['end_date'],signal_config['device'])

            cursor.execute(sql)
            raw_data_array = cursor.fetchall()

    finally:
        connection.close()
    return raw_data_array


signal_configs_list = generate_signal_configs_list()
# print(scl)
# print(scl[0]['utc_time_begin'])
# print(scl[0]['utc_time_end'])
# print(scl[-1]['utc_time_begin'])
# print(scl[-1]['utc_time_end'])







# Import signals
# Apply data integrity:
#   detect duplicates, view duplicates statistics
#   detect and complete gaps, view gap statistics
#   get a duplicate-free signal with corrected gaps (if required)
# Plot signals and difference signals
# Shift gps signal to match bmp signal if required. Shift constant selected manually or by correlation.
# Apply paper parameters estimation techniques to signals and difference signals.
#   estimate difference signal mean and std
#   apply altitude correction: regression line parameter estimation
#   apply drift correction




