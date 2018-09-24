import pymysql

def connection_configurations():
    return {
    'host': 'vnmysql.c4a62i7b81an.us-east-2.rds.amazonaws.com',
    'user': 'vndbroot',
    'password': 'AkuoKfo321!',
    'db': 'vndb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
    }

def signal_configurations():
    '''Signal download from database'''

    return {
    'begin_date': '2018-06-03',
    'end_date': '2018-06-04',
    'device': 'he00001'
    }

def load_parameters():
    '''Signal-independent parameters'''
    return {
        'time_step': 1.0,
        # 'gap_duration_thresh': 10
        'gap_duration_thresh': 5
    }

