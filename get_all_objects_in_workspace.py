import requests

from Token import maintoken  # Use your preferred token process


def get_all_workspace(workspace_id, run_token):
    params = {'loadAll': True}
    url = str("https://api.smartsheet.com/2.0/workspaces/" + str(int(workspace_id)))
    output = requests.get(url, params=params,
                          headers={"Authorization": str("Bearer " + run_token), 'Content-Type': 'application/json'})
    result = output.json()
    return result


def get_all_objects_in_workspace(workspace_id, run_token):
    data = get_all_workspace(workspace_id, run_token)
    sheets_list = []
    reports_list = []
    sights_list = []
    folders_list = []
    sheets = {}

    def get_all_objects_in_folder(folder):
        data = folder
        for sheet in data.get('sheets', {}):
            sheets_list.append(sheet["id"])
        for report in data.get('reports', {}):
            reports_list.append(report["id"])
        for sight in data.get('sights', {}):
            sights_list.append(sight["id"])
        if "folders" in data:
            for folder in data["folders"]:
                folders_list.append(folder['id'])
                sheets_temp = get_all_objects_in_folder(folder)
                for i in sheets_temp:
                    sheets[i] = sheets_temp[i]
        return sheets

    for sheet in data.get('sheets', {}):
        sheets_list.append(sheet["id"])
    for report in data.get('reports', {}):
        reports_list.append(report["id"])
    for sight in data.get('sights', {}):
        sights_list.append(sight["id"])
    if "folders" in data:
        for folder in data["folders"]:
            folders_list.append(folder['id'])
            sheets_temp = get_all_objects_in_folder(folder)
            for i in sheets_temp:
                sheets[i] = sheets_temp[i]
    return sheets_list, reports_list, sights_list, folders_list


run_token = maintoken.caseytok
workspace_id = 6283724624029572
sheets_list, reports_list, sights_list, folders_list = get_all_objects_in_workspace(workspace_id, run_token)

print(sheets_list)