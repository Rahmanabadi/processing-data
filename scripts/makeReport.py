import pandas as pd
import os

def makeReport(aggregatedData):

    flaggedData = aggregatedData[aggregatedData['anomalies_flagged'] > 0]
    totalFlaggedRows = flaggedData.shape[0]
    totalAnomalies = flaggedData['anomalies_flagged'].sum()
    summary = pd.DataFrame({
        'Total Anomalies': [totalAnomalies],
        'Total Flagged Rows': [totalFlaggedRows]
    })

    os.makedirs('output', exist_ok=True)
    
    with pd.ExcelWriter('output/flagged_report.xlsx') as writer:
        flaggedData.to_excel(writer, sheet_name='Flagged Rows', index=False)
        summary.to_excel(writer, sheet_name='Summary', index=False)

    print('Report generated: ' + str(totalAnomalies) + ' anomalies flagged in ' + str(totalFlaggedRows) + ' flagged rows.')

