import os, json
from creds_manager import get_drive_service

#Cache file for already retrived folder_id
CACHE_FILE = os.path.join(os.path.dirname(__file__),'folder_cache.json')
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)


def get_file_id(folder_id,book_query):
    query=f"'{folder_id}' in parents and name contains '{book_query}' and trashed = false"
    service = get_drive_service()
    response = service.files().list(
        q=query,
        fields='files(id, name)',
        pageSize=1000
    ).execute()
    main_file=response.get('files',[])
    return main_file[0]["id"]


#Get the folder id
def get_folder_id_from_path(path,book_query,service=get_drive_service(), cache=load_cache()):
    folders = path.strip('/').split('/')
    current_folder_id = 'root'
    full_path = ''

    for folder in folders:
        full_path = f"{full_path}/{folder}" if full_path else folder
        if full_path in cache:
            current_folder_id = cache[full_path]
            continue

        if current_folder_id == 'root':
            # For root
            query = f"name = '{folder}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        else:
            query = f"'{current_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"

        # Get all folders under current parent
        response = service.files().list(
            q=query,
            fields='files(id, name)',
            pageSize=1000
        ).execute()
        matching_folder = next((f for f in response.get('files', []) if f['name'] == folder), None)
        if not matching_folder:
            raise FileNotFoundError(f"Folder '{folder}' not found in path '{full_path}'")
        current_folder_id = matching_folder['id']
        cache[full_path] = current_folder_id
    
    save_cache(cache)
    main_file_id=get_file_id(current_folder_id,book_query)
    return [current_folder_id,main_file_id]



# if __name__ == "__main__":
#     path = "IOE/BCT/4/Microprocessor"
#     folder_id = get_folder_id_from_path(path,'full-book')
#     print(f"Folder ID for '{path}': {folder_id}")
