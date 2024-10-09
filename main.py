from scripts.loadData import loadData
from scripts.processData import processData
from scripts.exportData import exportData
from scripts.makeReport import makeReport

def run():
    data = loadData()
    processedData = processData(data)
    exportData(processedData)
    makeReport(processedData)
    print("Data processing and report generation completed.")

if __name__ == '__main__':
    run()
