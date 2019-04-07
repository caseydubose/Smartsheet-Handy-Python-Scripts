import Basic_Functions3 as functions
import maintoken

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

#pull all objects at folder level
def getAllSheetsinFolder(folderId,sheets,run_token):
    data = functions.get_Folder(folderId,run_token, "none")
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

sheetslist = []
reports = []
sights = []

token = maintoken.contok
access_payload = {"accessLevel": "ADMIN", 'email': "useremail"}
workspaceid = "xxxx"

getAllObjectsinWorkspace(workspaceid, token)

#update sheets
for id in sheetslist:
    sheetresult = functions.update_sheet_share(access_payload, token, id)
    print(sheetresult)

#update reports
for id in reports:
    result = functions.update_report_share(access_payload, token, id)
    print(result)

#update sights
for id in sights:
    result = functions.update_sight_share(access_payload, token, id)
    print(result)
