import Request_Classes3 as req
import math
import requests

sheets_prefix = "https://api.smartsheet.com/2.0/sheets/"
reports_prefix = "https://api.smartsheet.com/2.0/reports/"
workspace_prefix = "https://api.smartsheet.com/2.0/workspaces/"
folder_prefix = "https://api.smartsheet.com/2.0/folders/"
sights_prefix = "https://api.smartsheet.com/2.0/sights/"





def getSheet(SheetID, token, counter=5):
    SheetID = str(int(SheetID))
    URL = str(sheets_prefix + SheetID)
    call = req.get_call(URL, token, params="none")
    result = call.execute_call(counter)
    return result

def list_sheets(token, page, pageSize, counter=5):
    URL = str("https://api.smartsheet.com/2.0/sheets")
    params = {}
    params['page'] = page
    params['pageSize'] = pageSize
    call = req.get_call(URL, token, params=params)
    result = call.execute_call(counter)
    return result

def initiatesheets(run_token):
    data = list_sheets(run_token, 1, 500)
    report_len = data["totalCount"]
    if report_len < 500:
        total_pages = 1
    else:
        total_pages = int(math.ceil(report_len / 500))
    new_data = {}
    if total_pages == 1:
        new_data["id"] = []
        for row in data["id"]:
            new_data["id"].append(row)
    else:
        new_data["id"] = []
        for page in range(1, total_pages):
            row_data = list_sheets(run_token, page, 500)
            for row in row_data:
                new_data["id"].append(row)
    data["id"] = new_data["id"]
    return data




def list_reports(token, counter=5):
    URL = str("https://api.smartsheet.com/2.0/reports")
    call = req.get_call(URL, token)
    result = call.execute_call(counter)
    return result

def ListSights(token, counter=5):
    URL = str("https://api.smartsheet.com/2.0/sheets")
    call = req.get_call(URL, token)
    result = call.execute_call(counter)
    return result



def getAutomation(SheetID, token, counter=5):
    SheetID = str(int(SheetID))
    URL = str(sheets_prefix + SheetID + str("/automationrules"))
    call = req.get_call(URL, token)
    result = call.execute_call(counter)
    return result

def getShare(SheetID, token, counter=5):
    SheetID = str(int(SheetID))
    URL = str(sheets_prefix + SheetID + str("/shares"))
    call = req.get_call(URL, token)
    result = call.execute_call(counter)
    return result


def get_Folder(folderId, run_token, params):
    URL = "https://api.smartsheet.com/2.0/folders/" + str(int(folderId))
    call = req.get_call(URL, run_token, params="none")
    result = call.execute_call(5)
    return result


def get_workspace(workspaceId, run_token, params):
    URL = str(workspace_prefix + str(int(workspaceId)))
    call = req.get_call(URL, run_token, params)
    result = call.execute_call(5)
    return result


def updateRows(payload, run_token, SheetID, counter=5):
    URL = str(sheets_prefix + str(int(SheetID)) + "/" + "rows")
    params = "none"
    call = req.put_call(URL, run_token, payload, params)
    result = call.execute_call(counter)
    return result


def update_sheet_share(payload, run_token, SheetID, counter=5):
    URL = str(sheets_prefix + str(int(SheetID)) + "/shares")
    call = req.post_call(URL, run_token, payload)
    result = call.execute_call(counter)
    return result

def move_sheet(run_token, SheetID, destinationId, destinationType, counter=5):
    package = {}
    package['destinationType'] = destinationType
    package['destinationId'] = destinationId
    URL = str(sheets_prefix + str(int(SheetID)) + "/move")
    call = requests.post(URL, run_token, package)
    result = call.json()
    return result


def update_report_share(payload, run_token, ReportID, counter=5):
    URL = str(reports_prefix + str(int(ReportID)) + "/shares")
    call = req.post_call(URL, run_token, payload)
    result = call.execute_call(counter)
    return result

def update_sight_share(payload, run_token, SightID, counter=5):
    URL = str(sights_prefix + str(int(SightID)) + "/shares")
    call = req.post_call(URL, run_token, payload)
    result = call.execute_call(counter)
    return result


def build_insert_column_package(sheet, name, col_type, index, width, package, pick_list_items=None):
    temp_package = {"title": name, "type": col_type, "options": pick_list_items, "index": index, "width": width}
    package.append(temp_package)
    return package


def submit_insert_columns_package(sheetData, package, token):
    SheetID = sheetData["id"]
    URL = str("https://api.smartsheet.com/2.0/sheets/" + str(int(SheetID)) + "/" + "columns")
    call = req.post_call(URL, token, package)
    result = call.execute_call(5)
    return result


def submit_insert_rows(package, SheetID, token):
    URL = str(sheets_prefix + str(int(SheetID)) + "/" + "rows")
    call = req.post_call(URL, token, package)
    result = call.execute_call(5)
    return result


def copy_Sheet_To_Folder(copyId, destinationFolderId, newName, token):
    URL = str("https://api.smartsheet.com/2.0/sheets/" + str(copyId) + "/" + "copy?include=all")
    payload = {"destinationType": "folder", "destinationId": destinationFolderId, "newName": newName}
    response = req.post_call(URL, token, payload)
    return response


# def share_sheet(sheetId, email, access, send_email=False, subject=None, body=None, token):
#     package = {"email": email, "accessLevel": access.upper(), "subject": subject, "body": body}
#     URL = str("https://api.smartsheet.com/2.0/sheets/" + str(sheetId) + "/" + "/shares?sendEmail=" + str(send_email))
#     response = req.post_call(URL, token, package)
#     return response


def copy_rows_to_another_sheet_including_formulas(rows, target_sheet_id, target_inv_map, source_col_map, run_token,
                                                  location_type="toBottom", location_value="true", strict="false"):
    package = []
    if type(rows) == dict:
        rows = [rows]
    for row in rows:
        cells_pack = []
        for cell in row["cells"]:
            cell_temp = {}
            try:
                cell_temp["columnId"] = target_inv_map[source_col_map[cell["columnId"]]]
            except KeyError:
                continue
            for attribute in cell:
                if attribute in ["columnId", "strict", "linksOutToCells"]:
                    continue
                else:
                    cell_temp[attribute] = cell[attribute]
            if 'value' not in cell_temp:
                cell_temp["value"] = None
            if 'formula' in cell_temp or 'linkInFromCell' in cell_temp:
                cell_temp["value"] = None
            cell_temp["strict"] = strict
            cells_pack.append(cell_temp)
        package.append({location_type: location_value, "cells": cells_pack})
    URL = str("https://api.smartsheet.com/2.0/sheets/" + str(int(target_sheet_id)) + "/" + "rows")
    call = req.post_call(URL, run_token, package)
    response = call.execute_call(5)
    return response


def initiateSheet(sheetId, run_token):
    data = getSheet(sheetId, run_token)
    # if 'data' not in data:
    #    print data
    colMap, rowMap, invMap = createSheetMap(data)
    return data, colMap, rowMap, invMap


def createSheetMap(sheetData):
    colMap = {}
    rowMap = {}
    for rows in sheetData["rows"]:
        rowMap[rows["rowNumber"]] = rows["id"]
    for col in sheetData["columns"]:
        colMap[col["id"]] = col["title"]
    invMap = {}
    for col in colMap:
        invMap[colMap[col]] = col
    return colMap, rowMap, invMap

def update_formatting_from_report(reportId, format_string, target_column, run_token, update_column_formatting = False):
   data, colMap, rowMap, invMap = initiateReport(reportId, run_token)
   current_sheet_id = None
   updates_package = {}
   for row in data["rows"]:
       cellPackage = []
       current_row_id = row["id"]
       current_sheet_id_check = row["sheetId"]
       if current_sheet_id_check != current_sheet_id:
           current_sheet_id = row["sheetId"]
           Cdata, CcolMap, CrowMap, CinvMap = initiateSheet(current_sheet_id, run_token)
           if update_column_formatting == True:
               if target_column in CinvMap:
                   package = {"format":format_string}
                   response = updateColumns(package, invMap[target_column],run_token, current_sheet_id)
       if current_sheet_id not in updates_package:
           updates_package[current_sheet_id] = []
       for cell in row["cells"]:
           current_column_name = colMap[cell["virtualColumnId"]]
           if current_column_name == target_column:
               if 'formula' in cell:
                   cellPackage.append({"columnId": CinvMap[current_column_name], "format": format_string,'formula':cell["formula"], "strict": "false"})
               elif 'linkInFromCell' in cell:
                   cellPackage.append({"columnId": CinvMap[current_column_name], "format": format_string,"linkInFromCell": cell["linkInFromCell"], "strict": "false"})
               elif 'value' in cell:
                   cellPackage.append({"columnId": CinvMap[current_column_name], "format": format_string,"value": cell["value"], "strict": "false"})
               else:
                   cellPackage.append({"columnId": CinvMap[current_column_name], "format": format_string,"value": None, "strict": "false"})
       updates_package[current_sheet_id].append({"id": current_row_id, "cells": cellPackage})
   print(updates_package)
   for sheet in updates_package:
       result = updateRows(updates_package[sheet], run_token, sheet)
       print(result)
   return "complete"

def update_colformatting_from_report(reportId, format_string, target_column, run_token):
   data, colMap, rowMap, invMap = initiateReport(reportId, run_token)
   for row in data["rows"]:
     sheetid = row["sheetId"]
     columnid = row["cells"][4]['columnId']
     result = updateColumns({'locked': True}, columnid, run_token, sheetid)
     print(result)
   return "complete"

def update_rowformatting_from_report(reportId, run_token):
   data, colMap, rowMap, invMap = initiateReport(reportId, run_token)
   for row in data["rows"]:
     SheetID = row["sheetId"]
     RowID = row["id"]
     print('Sheet ID' + str(SheetID))
     result = updateRows({'id':RowID,'locked': False}, run_token, SheetID, counter=5)
     print(result)
   return "Complete"


def update_sharing_from_report(reportId, access_level, email, run_token):
   access_payload = {"accessLevel": str(access_level), 'email': email}
   data, colMap, rowMap, invMap = initiateReport(reportId, run_token)
   current_sheet_id = None
   updates_package = {}
   for row in data["rows"]:
       current_sheet_id_check = row["sheetId"]
       if current_sheet_id_check != current_sheet_id:
           current_sheet_id = row["sheetId"]
       if current_sheet_id not in updates_package:
           updates_package[current_sheet_id] = []
           r = update_sheet_share(access_payload, run_token, current_sheet_id)
           print(r)
   return "complete"




def find_sheetformatting_from_report(reportId, run_token):
   data, colMap, rowMap, invMap = initiateReport(reportId, run_token)
   current_sheet_id = None
   updates_package = {}
   for row in data["rows"]:
     current_sheet_id_check = str(row["sheetId"])
     if current_sheet_id_check != current_sheet_id:
        current_sheet_id = str(row["sheetId"])
     if current_sheet_id not in updates_package:
        result = getAutomation(current_sheet_id, run_token)
        sheetname = row["cells"][0]['value']
        totalcount = result['totalCount']
        updates_package[current_sheet_id] = []
        if totalcount > 0:
            updates_package[current_sheet_id].append({"SheetName": sheetname, "TotalAutomationRules": totalcount})
            for row in result['data']:
                try:
                    rulename = row['name']
                except:
                    rulename = "NULL"
                createdby = row['createdBy']['email']
                frequency = row['action']['frequency']
                print(sheetname + ", " + str(totalcount) + ", " + rulename + ", " + createdby + ", " + frequency)
                # updates_package[current_sheet_id].append({"RuleName": rulename, "createdby": createdby, "frequency": frequency})
                # for row in updates_package.values():
                #     for dict in row:
                #         if 'SheetName' in dict:
                #             SheetName = str(dict['SheetName'])
                #         elif 'RuleName' in dict:
                #             RuleName = str(dict['RuleName'])
                #             Createdby = dict['createdby']
                #             frequent = dict['frequency']
                #             print(SheetName + ", " + RuleName + ", " + Createdby + ", " + frequent)
   return(updates_package)


def update_cellvalue_from_report(reportId, cell_value, target_column, run_token):
   data, colMap, rowMap, invMap = initiateReport(reportId, run_token)
   current_sheet_id = None
   updates_package = {}
   for row in data["rows"]:
       cellPackage = []
       current_row_id = row["id"]
       current_sheet_id_check = row["sheetId"]
       if current_sheet_id_check != current_sheet_id:
           current_sheet_id = row["sheetId"]
           Cdata, CcolMap, CrowMap, CinvMap = initiateSheet(current_sheet_id, run_token)
       if current_sheet_id not in updates_package:
           updates_package[current_sheet_id] = []
       for cell in row["cells"]:
           current_column_name = colMap[cell["virtualColumnId"]]
           if current_column_name == target_column:
               if 'value' in cell:
                   cellPackage.append({"columnId": CinvMap[current_column_name], "value": cell_value , "strict": "false"})
               else:
                   cellPackage.append({"columnId": CinvMap[current_column_name], "value": None, "strict": "false"})
       updates_package[current_sheet_id].append({"id": current_row_id, "cells": cellPackage})
   print(updates_package)
   for sheet in updates_package:
       result = updateRows(updates_package[sheet], run_token, sheet)
       print(result)
   return "complete"




def find_row_by_identifiers(column_value_pair_dict, colMap, rows, start_row=0, end_row=10000):
    """column_value_pair_dict must be a dictionary of format {'column_name1':'value1','column_name2','value2'   """
    output = []
    for row in rows:
        if row["rowNumber"] >= start_row and row["rowNumber"] <= end_row:
            found = False
            for cell in row["cells"]:
                try:
                    colName = colMap[cell["columnId"]]
                except KeyError:
                    continue
                if colName in column_value_pair_dict:
                    if cell.has_key("value") and column_value_pair_dict[colMap[cell["columnId"]]] == cell["value"]:
                        found = True
                    else:
                        found = False
                        break
            if found == True:
                output.append(row)
    if len(output) > 1:
        output = "Found more than 1 row, use better criteria"
    else:
        output = output[0]
    return output


def update_row_to_match_template_row(rows, target_sheet_id, target_sheet_data, target_inv_map, target_col_map,
                                     source_col_map, cols_to_update, run_token, column_value_pair_dict, start_row=0,
                                     end_row=10000, strict="false"):
    package = []
    targetRow = find_row_by_identifiers(column_value_pair_dict, target_col_map, target_sheet_data["rows"], start_row,
                                        end_row)
    if type(rows) == dict:
        rows = [rows]
    for row in rows:
        cells_pack = []
        for cell in row["cells"]:
            cell_temp = {}
            try:
                cell_temp["columnId"] = target_inv_map[source_col_map[cell["columnId"]]]
            except KeyError:
                continue
            if str(source_col_map[cell["columnId"]]) not in cols_to_update:
                continue
            for attribute in cell:
                if attribute == "columnId" or attribute == "strict":
                    continue
                else:
                    cell_temp[attribute] = cell[attribute]
            if 'value' not in cell_temp:
                cell_temp["value"] = None
            if 'formula' in cell_temp or 'linkInFromCell' in cell_temp:
                cell_temp["value"] = None
            cells_pack.append(cell_temp)
        package.append({"id": targetRow["id"], "cells": cells_pack})
    URL = str("https://api.smartsheet.com/2.0/sheets/" + str(int(target_sheet_id)) + "/" + "rows")
    call = req.put_call(URL, run_token, package)
    response = call.execute_call(5)
    return response


def getAllSheetsinFolder(folderId, sheets, run_token):
    data = get_Folder(folderId, run_token)
    if data.has_key("sheets"):
        for sheet in data["sheets"]:
            sheets[sheet["id"]] = {"name": sheet["name"], "parentType": "Folder", "parentName": data["name"],
                                   "parentId": data["id"], "link": sheet["permalink"], "type": "Sheet"}
    if data.has_key("reports"):
        for report in data["reports"]:
            sheets[report["id"]] = {"name": report["name"], "parentType": "Folder", "parentName": data["name"],
                                    "parentId": data["id"], "link": report["permalink"], "type": "Report"}
    if data.has_key("sights"):
        for sight in data["sights"]:
            sheets[sight["id"]] = {"name": sight["name"], "parentType": "Folder", "parentName": sight["name"],
                                   "parentId": sight["id"], "link": sight["permalink"], "type": "Sight"}
    if data.has_key("folders"):
        for folder in data["folders"]:
            sheetsTemp = {}
            sheetsTemp = getAllSheetsinFolder(str(folder["id"]), sheets, run_token)
            for i in sheetsTemp:
                sheets[i] = sheetsTemp[i]
    return sheets


def move_folder(folder_id, destinationType, destination_Id, run_token):
    url = folder_prefix + str(int(folder_id)) + "/move"
    package = {"destinationType": destinationType, "destinationId": str(int(destination_Id))}
    call = req.post_call(url, run_token, package)
    response = call.execute_call(5)
    return response


def getSheetIdsFromReport(reportId, run_token):
    data, colMap, rowMap, invMap = initiateReport(reportId, run_token)
    sheets = []
    for row in data["rows"]:
        sheets.append(row["sheetId"])
    return sheets


def initiateReport(reportID, run_token):
    data = getReport(reportID, 1, 500, run_token)
    report_len = data["totalRowCount"]
    if report_len < 500:
        total_pages = 1
    else:
        total_pages = int(math.ceil(report_len / 500))
    columns = data["columns"]
    colMap = {}
    invMap = {}
    rowMap = {}
    for col in columns:
        colMap[col["virtualId"]] = col["title"]
        invMap[col["title"]] = col["virtualId"]
    new_data = {}
    if total_pages == 1:
        new_data["rows"] = []
        for row in data["rows"]:
            rowMap["rowNumber"] = row["id"]
            new_data["rows"].append(row)
    else:
        new_data["rows"] = []
        for page in range(1, total_pages):
            row_data = getReport(reportID, page, 500, run_token)
            for row in row_data["rows"]:
                new_data["rows"].append(row)
                rowMap[row["rowNumber"]] = row["id"]
    data["rows"] = new_data["rows"]
    return data, colMap, rowMap, invMap


def getReport(reportId, page, pageSize, run_token, Prefix="https://api.smartsheet.com/2.0/reports/"):
    URL = str(Prefix + reportId)
    headers1 = {"Authorization": str("Bearer " + run_token), 'Content-Type': 'application/json'}
    perameters = {}
    perameters['page'] = page
    perameters['pageSize'] = pageSize
    # call = req.get_call(URL,run_token)
    # result = call.execute_call(5)
    sheet = requests.get(URL, params=perameters,
                         headers={"Authorization": str("Bearer " + run_token), 'Content-Type': 'application/json'})
    result = sheet.json()
    return result


def updateColumns(payload, columnId, run_token, SheetID):
    URL = str(sheets_prefix + str(SheetID) + "/" + "columns" + "/" + str(columnId))
    call = req.put_call(URL, run_token, payload)
    result = call.execute_call(5)
    return result



def create_cross_sheet_reference(name, referenced_sheet_Id, start_column_id, end_column_id, target_sheet_id, run_token,
                                 start_row_id=None, end_row_id=None):
    URL = str(sheets_prefix + str(int(target_sheet_id)) + "/" + "crosssheetreferences")
    if start_row_id == None:
        payload = {"name": name, "sourceSheetId": referenced_sheet_Id, "startColumnId": start_column_id,
                   "endColumnId": end_column_id}
    elif start_row_id != None:
        payload = {"name": name, "sourceSheetId": referenced_sheet_Id, "startColumnId": start_column_id,
                   "endColumnId": end_column_id, "startRowId": start_row_id, "endRowId": end_row_id}
    client = req.post_call(URL, run_token, payload)
    output = client.execute_call(5)
    return output



def update_column_formatting_from_report(reportId, colNames, format_string, run_token):
    sheets = getSheetIdsFromReport(reportId, run_token)
    already_complete = []
    if type(sheets) == dict:
        sheets = [sheets]
    for sheet in sheets:
        update_package = []
        if sheet not in already_complete:
            data,colMap,rowMap,invMap = initiateSheet(sheet,run_token)
            for row in data["rows"]:
                row_package = {"id":row["id"]}
                cell_package = []
                blank_check = 0
                for cell in row["cells"]:
                    if colMap[cell["columnId"]] in colNames:
                        if "value" in cell:
                            blank_check += 1
                        if "value" in cell:
                            cell_package.append({"value":cell["value"],"format":format_string,"columnId":cell["columnId"],"strict":"false"})
                if blank_check >0:
                    row_package["cells"]=cell_package
                    update_package.append(row_package)
            if len(update_package) == 1:
                update_package = update_package[0]
            result = updateRows(update_package, run_token, sheet, 5)
        for colName in colNames:
            if colName in invMap:
                package = {"format":format_string}
                response = updateColumns(package, invMap[colName],run_token, sheet)
        already_complete.append(sheet)

def create_cross_sheet_reference(name, referenced_sheet_Id, start_column_id, end_column_id, target_sheet_id,
                                 run_token, start_row_id=None, end_row_id=None):
    URL = str(sheets_prefix + str(int(target_sheet_id)) + "/" + "crosssheetreferences")
    if start_row_id == None:
        payload = {"name": name, "sourceSheetId": referenced_sheet_Id, "startColumnId": start_column_id,
                   "endColumnId": end_column_id}
    elif start_row_id != None:
        payload = {"name": name, "sourceSheetId": referenced_sheet_Id, "startColumnId": start_column_id,
                   "endColumnId": end_column_id, "startRowId": start_row_id, "endRowId": end_row_id}
    client = req.post_call(URL, run_token, payload)
    output = client.execute_call(5)
    return output


def insert_new_metadata_field(summary_sheet_id, row_labels, label_col, data_col, row_label_correct_link,
                              target_label_col, target_data_cols, additions, run_token):
    data, colMap, rowMap, invMap = initiateSheet(summary_sheet_id, run_token)
    to_update = {}
    package = []
    for addition in additions:
        package.append({"toBottom": "true", "cells": [{"columnId": invMap[label_col], "value": addition}]})
    result = submit_insert_rows(package, summary_sheet_id, run_token)
    data, colMap, rowMap, invMap = initiateSheet(summary_sheet_id, run_token)
    for row in data["rows"]:
        flag = 0
        row_temp = {}
        for cell in row["cells"]:
            if "linkInFromCell" in cell:
                row_temp[colMap[cell["columnId"]]] = cell["linkInFromCell"]
            elif "value" in cell:
                row_temp[colMap[cell["columnId"]]] = cell["value"]
            if "value" in cell and cell["value"] == row_label_correct_link:
                flag = 1
        if flag == 1:
            sheetId = row_temp[data_col]["sheetId"]
        if label_col in row_temp and row_temp[label_col] in row_labels:
            to_update[row_temp[label_col]] = row["id"]
    data1, colMap1, rowMap1, invMap1 = initiateSheet(sheetId, run_token)
    for row in data1["rows"]:
        cellpack = []
        flag = 0
        row_temp = {}
        for cell in row["cells"]:
            if "linkInFromCell" in cell:
                row_temp[colMap1[cell["columnId"]]] = cell["linkInFromCell"]
            elif "value" in cell:
                row_temp[colMap1[cell["columnId"]]] = cell["value"]
            elif 'value' not in cell:
                row_temp[colMap1[cell["columnId"]]] = None
        if row_temp[target_label_col] in row_labels:
            cellpack.append({"columnId": invMap[data_col], "value": None,
                             "linkInFromCell": {"columnId": invMap1[target_data_cols], "sheetId": sheetId,
                                                "rowId": row["id"]}})
        if row_temp[target_label_col] in to_update:
            package = {"id": to_update[row_temp[target_label_col]], "cells": cellpack}
            result = updateRows(package, run_token, summary_sheet_id)


def udpate_master_roll_up(summary_sheet_id,label_col,data_col,target_sheet,run_token,row_id, additions):
    data,colMap,rowMap,invMap = initiateSheet(summary_sheet_id,run_token)
    update_package = {}
    cell_link_package = []
    cols_already_included = []
    for row in data["rows"]:
        row_temp = {}
        for cell in row["cells"]:
            if "value" in cell:
                row_temp[colMap[cell["columnId"]]] = cell["value"]
        if label_col in row_temp:
            if row_temp[label_col] not in cols_already_included:
                update_package[row_temp[label_col]] = [{"columnId":invMap[data_col],"rowId":row["id"],"sheetId":summary_sheet_id}]
                cell_link_package.append({"columnId":row_temp[label_col],"value":None,"linkInFromCell":{"columnId":invMap[data_col],"rowId":row["id"],"sheetId":summary_sheet_id}})
                cols_already_included.append(row_temp[label_col])
    data,colMap,rowMap,invMap = initiateSheet(target_sheet,run_token)
    cellpack = []
    for cell_link in cell_link_package:
        if cell_link["columnId"] in invMap and cell_link["columnId"] in additions:
            cell_link["columnId"] = invMap[cell_link["columnId"]]
            cellpack.append(cell_link)
    package = [{"id":row_id,"cells":cellpack}]
    result = updateRows(package, run_token,target_sheet)
    return result

def find_col_value_in_row(row,col_name,invMap):
   output = "No Value"
   for cell in row["cells"]:
       if "value" in cell and invMap[col_name] == cell["columnId"]:
           output = cell["value"]
   return output

def find_value_in_column(data,colMap,value,columns_to_search):
   output = {}
   counter = 0
   for row in data["rows"]:
       for cell in row["cells"]:
           if "value" in cell and colMap[cell["columnId"]] in columns_to_search and cell["value"]==value:
               output[counter] = {"rowId":row["id"],"rowNumber":row["rowNumber"],"cell":cell,"column":colMap[cell["columnId"]],"row":row}
               counter +=1
   return output


#pull all objects at workspace level, will recursively do subfolders if found.
def getAllObjectsinWorkspace(workpsaceID,run_token):
    sheets = {}
    data = functions.get_workspace(workpsaceID, run_token, "none")
    folders = []
    if "sheets" in data:
        for sheet in data["sheets"]:
            sheetslist.append(sheet["id"])
    if "reports" in data:
        for report in data["reports"]:
            reports.append(report["id"])
    if "sights" in data:
        for sight in data["sights"]:
            sights.append(sight["id"])
    if "folders" in data:
        for folder in data["folders"]:
            sheetsTemp = {}
            sheetsTemp = getAllSheetsinFolder(str(folder["id"]),sheets,run_token)
            for i in sheetsTemp:
                sheets[i] = sheetsTemp[i]
    return sheets