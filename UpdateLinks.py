import Basic_Functions3 as functions
import csv

token = "api key"

'''
This script ended up being a bit more manual but can be helpful if you want to stage data before  committing it to 
update. 
1) Pulls data from an aggregate sheet, finds the targets of the hyperlinks, and loads into a .CSV file.  (I'd likely 
merge with a find formula to streamline this in the future.)
2) Iterate through each target sheet to search for target hyperlink and update.  (I manually adjusted the search 
value for each run through)
'''


# 1) Pull in Aggregate Sheet, Load target sheet link, Load target hyperlink destination value
def loadcsv():
    with open('aggexport.csv', mode='w', newline='') as csv_file:
        fieldnames = ['criticalpathid', 'projectcontactsurl', 'projectcharterurl', 'impactedstoresurl', 'prjname']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        data = functions.getSheet(5392989494241156, token)
        rows = data['rows']
        for r in rows:
            try:
                column = r['cells']
                criticalpathid = column[12]['hyperlink']['sheetId']
                projectcontactsurl = column[14]['hyperlink']['url']
                projectcharterurl = column[11]['hyperlink']['url']
                impactedstoresurl = column[16]['hyperlink']['url']
                prjname = column[9]['value']
                writer.writerow({'criticalpathid': criticalpathid, 'projectcontactsurl': projectcontactsurl,
                                 'projectcharterurl': projectcharterurl, 'impactedstoresurl': impactedstoresurl,
                                 'prjname': prjname})
            except KeyError:
                print(KeyError)


# loadcsv()


# 2) Iterate through each target sheet to search for target hyperlink and update.
def find_value_in_column(data, col_map, value, columns_to_search):
    output = {}
    counter = 0
    for row in data["rows"]:
        for cell in row["cells"]:
            if "value" in cell and col_map[cell["columnId"]] in columns_to_search and cell["value"] == value:
                output[counter] = {"rowId": row["id"], "rowNumber": row["rowNumber"], "cell": cell,
                                   "column": col_map[cell["columnId"]], "row": row}
                counter += 1
    return output


def create_cell_link_dict():
    search_value41 = "Identify any additional Impacted Stores"
    with open('aggexport.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            criticalpathid = row['criticalpathid']
            projectcontactsurl = row['projectcontactsurl']
            projectcharterurl = row['projectcharterurl']
            impactedstoresurl = row['impactedstoresurl']
            data, col_map, row_map, inv_map = functions.initiateSheet(criticalpathid, token)
            output = find_value_in_column(data, col_map, search_value41, "Task Name")
            for values in output.values():
                rowid = values['rowId']
                colid = values['cell']['columnId']
                payload = {'id': rowid, 'cells': [
                    {'columnId': colid, 'value': search_value41, 'hyperlink': {'url': projectcharterurl}}]}
                results = functions.updateRows(payload, token, criticalpathid)
                print(results)
        return results

# Run
# create_cell_link_dict()
