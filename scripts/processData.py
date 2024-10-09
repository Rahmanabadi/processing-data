import pandas as pd
import logging
from dateutil import parser
import os

os.makedirs('logs', exist_ok=True)

logFile = 'logs/process.log'
logLevel = logging.INFO
logFormat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=logFile, level=logLevel, format=logFormat)

def processData(data):
    initialCount = len(data)
    logging.info('Initial number of records: ' + str(initialCount))

    data = data.dropna(subset=['resolution_time', 'customer_satisfaction'])
    afterDropCount = len(data)
    logging.info('Dropped ' + str(initialCount - afterDropCount) + ' records with missing values.')

    validStatusData = data[data['status'].between(0, 2)]
    removedInvalidStatusCount = afterDropCount - len(validStatusData)
    logging.info('Removed ' + str(removedInvalidStatusCount) + ' records with out-of-range status values.')

    validStatusData.loc[:, 'timestamp'] = validStatusData['timestamp'].apply(convert_to_iso)
    validStatusData = validStatusData.dropna(subset=['timestamp'])
    logging.info('Converted timestamps to ISO-8601 format and removed rows with invalid timestamps.')

    validStatusData['anomaly_flag'] = False
    for index, row in validStatusData.iterrows():
        if row['resolution_time'] > 120 or row['customer_satisfaction'] < 2:
            validStatusData.at[index, 'anomaly_flag'] = True


    anomaliesCount = validStatusData['anomaly_flag'].sum()
    logging.info('Total number of anomalies detected and flagged: ' + str(anomaliesCount))

    validStatusData['day'] = None
    for index, row in validStatusData.iterrows():
        date_time = pd.to_datetime(row['timestamp'])
        validStatusData.at[index, 'day'] = date_time.date()


    aggregatedData = []
    grouped = validStatusData.groupby(['day', 'team_id'])
    for (day, team_id), group in grouped:
        avg_resolution_time = group['resolution_time'].mean()
        avg_customer_satisfaction = group['customer_satisfaction'].mean()
        count_status_0 = (group['status'] == 0).sum()
        count_status_1 = (group['status'] == 1).sum()
        count_status_2 = (group['status'] == 2).sum()
        anomalies_flagged = group['anomaly_flag'].sum()

        result = {
            'day': day,
            'team_id': team_id,
            'avg_resolution_time': avg_resolution_time,
            'avg_customer_satisfaction': avg_customer_satisfaction,
            'count_status_0': count_status_0,
            'count_status_1': count_status_1,
            'count_status_2': count_status_2,
            'anomalies_flagged': anomalies_flagged
        }
        aggregatedData.append(result)

    aggregatedData = pd.DataFrame(aggregatedData)

    logging.info('Data aggregation completed. Aggregated data has ' + str(len(aggregatedData)) + ' rows.')
    return aggregatedData


def convert_to_iso(timestamp):
    try:
        dt = parser.parse(timestamp)
        return dt.isoformat() + 'Z'
    except Exception as e:
        logging.warning('Failed to parse timestamp: ' + str(timestamp) + ' - ' + str(e))
        return None
