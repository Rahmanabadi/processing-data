from faker import Faker
import pandas as pd
import random
import os

fake = Faker()
teams = ['team1', 'team2', 'team3', 'team4', 'team5']
dataFolder = os.path.join(os.getcwd(), 'data')
os.makedirs(dataFolder, exist_ok=True)

for team in teams:
    timestamps = []
    resolution_times = []
    customer_satisfaction_scores = []
    statuses = []

    for _ in range(100):
        timestamp = fake.date_time_this_month().strftime('%m/%d/%Y %H:%M:%S')
        timestamps.append(timestamp)

        resolution_time = random.choice([None, random.randint(5, 120), random.randint(150, 300)])
        resolution_times.append(resolution_time)

        customer_satisfaction = random.choice([None, random.randint(1, 2), random.randint(3, 5)])
        customer_satisfaction_scores.append(customer_satisfaction)

        status = random.choice([random.randint(0, 2), random.randint(3, 5)])
        statuses.append(status)

    data = {
        'timestamp': timestamps,
        'team_id': [team] * 100,
        'resolution_time': resolution_times,
        'customer_satisfaction': customer_satisfaction_scores,
        'status': statuses
    }

    csvFilePath = os.path.join(dataFolder, f'{team}.csv')
    pd.DataFrame(data).to_csv(csvFilePath, index=False)
    print(f"Data saved for {team} at {csvFilePath}")
