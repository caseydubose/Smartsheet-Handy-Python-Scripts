import Basic_Functions3 as functions

def find_value_in_column(data, colMap, searchvalue, columns_to_search):
    output = {}
    counter = 0
    for row in data["rows"]:
        for cell in row["cells"]:
            if "value" in cell and colMap[cell["columnId"]] in columns_to_search and cell["value"] == searchvalue:
                output[counter] = {"rowId": row["id"], "rowNumber": row["rowNumber"], "cell": cell,
                                   "column": colMap[cell["columnId"]], "row": row}
                counter += 1
    return output


'''
This script will search for a project in an aggregate sheet by a criteria, collect a list of matching rows, and find the target sheets of a searched hyperlink in that row, and gather that into a list of target sheet ids. 
The target sheet ids can be used to their own find and replace function. 
'''


#pull data from aggregate sheet
token = XXXXXXX
data, colMap, rowMap, invMap = functions.initiateSheet(aggsheetid, token)

#search aggregate sheet to find projects that match criteria
aggsheetid = XXXXXXX
searchvalue = "XXXX"
columns_to_search = "XXXXX"
output = find_value_in_column(data, colMap, searchvalue, columns_to_search)

#create list of matching rowids
matchingrows = []
for row in output.values():
    rowId = row['rowId']
    matchingrows.append(rowId)

#find target sheets in aggregate that match target link name value and return sheetid of hyperlink
targetsheets = []
targetlinkvalue = "XXXX"
for id in matchingrows:
    for row in data['rows']:
        if id == row['id']:
            for cell in row['cells']:
                try:
                    if cell['value'] == targetlinkvalue:
                        targetsheets.append(cell['hyperlink']['sheetId'])
                except KeyError:
                    pass

#search target sheets for value to update in target column, adjust payload to fit update needed on target sheet

searchvalue = 'XXXX'
columns_to_search = "XXXX"

for targetsheetid in targetsheets:
    data, colMap, rowMap, invMap = functions.initiateSheet(targetsheetid, token)
    output = find_value_in_column(data, colMap, searchvalue, columns_to_search)
    for values in output.values():
        rowid = values['rowId']
        colid = values['cell']['columnId']
        payload = {'id': rowid, 'cells': [
            {'columnId': colid, 'value': "OmniChannel"}]}
        results = functions.updateRows(payload, token, targetsheetid)
        print(results)







