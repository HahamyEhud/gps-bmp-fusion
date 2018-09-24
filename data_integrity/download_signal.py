import pymysql
import configurations as cnf
import pandas as pd
from numpy import logical_not

def signal_download():
    connection_config = cnf.connection_configurations()
    signal_config = cnf.signal_configurations()

    connection = pymysql.connect(host=connection_config['host'],
                                 user=connection_config['user'],
                                 password=connection_config['password'],
                                 db=connection_config['db'],
                                 charset=connection_config['charset'],
                                 cursorclass=connection_config['cursorclass']
                                 )
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT event_timestamp, bmp_alt' \
                  ' FROM hawkeye_rawdata' \
                  ' WHERE event_timestamp > "{0}"' \
                  ' AND event_timestamp < "{1}"'\
                  ' AND device_sn = "{2}"'.format(signal_config['begin_date'], signal_config['end_date'],signal_config['device'])

            cursor.execute(sql)
            raw_data_array = cursor.fetchall()

    finally:
        connection.close()
    return raw_data_array








