import pandas as pd
import os

def exportData(aggregatedData):
    if not os.path.exists('output'):
        os.makedirs('output')
        
    outputFile = 'output/processed_data_for_database.csv'
    reshapedData = []

    for index, row in aggregatedData.iterrows():
        day = row['day']
        team_id = row['team_id']
        reshapedData.append({'day': day, 'team_id': team_id, 'metric_name': 'avg_resolution_time', 'metric_value': str(row['avg_resolution_time'])})
        reshapedData.append({'day': day, 'team_id': team_id, 'metric_name': 'avg_customer_satisfaction', 'metric_value': str(row['avg_customer_satisfaction'])})
        reshapedData.append({'day': day, 'team_id': team_id, 'metric_name': 'count_status_0', 'metric_value': str(row['count_status_0'])})
        reshapedData.append({'day': day, 'team_id': team_id, 'metric_name': 'count_status_1', 'metric_value': str(row['count_status_1'])})
        reshapedData.append({'day': day, 'team_id': team_id, 'metric_name': 'count_status_2', 'metric_value': str(row['count_status_2'])})
        reshapedData.append({'day': day, 'team_id': team_id, 'metric_name': 'anomalies_flagged', 'metric_value': str(row['anomalies_flagged'])})

    reshapedData = pd.DataFrame(reshapedData)
    reshapedData.to_csv(outputFile, index=False)
    print("The data has been saved to:", outputFile)

