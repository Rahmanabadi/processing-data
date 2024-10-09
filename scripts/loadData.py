import pandas as pd
import os

def loadData():
    dataFolder = os.path.join(os.path.dirname(__file__), 'data')
    files = os.listdir(dataFolder)
    csvFiles = []

    for file in files:
        if file.endswith('.csv'):
            csvFiles.append(file)

    dataFrames = []
    for csvFile in csvFiles:
        filePath = os.path.join(dataFolder, csvFile)
        df = pd.read_csv(filePath)
        dataFrames.append(df)

    combinedData = pd.concat(dataFrames, ignore_index=True)
    return combinedData
