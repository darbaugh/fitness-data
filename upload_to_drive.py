import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load credentials from environment variable
service_account_info = json.loads(os.environ['GDRIVE_CREDENTIALS'])
credentials = service_account.Credentials.from_service_account_info(service_account_info)
drive_service = build('drive', 'v3', credentials=credentials)

folder_id = '1ad7X3Ha4HLxGw0JPQcHK8o-fBHngM5xN'
file_name = 'latest.json'

# 1. Check if the file already exists in that folder to overwrite it
query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
results = drive_service.files().list(q=query, spaces='drive', fields='files(id)').execute()
files = results.get('files', [])

media = MediaFileUpload(file_name, mimetype='application/json')

if files:
    # Update existing file
    file_id = files[0]['id']
    drive_service.files().update(fileId=file_id, media_body=media).execute()
    print(f"Updated existing file: {file_id}")
else:
    # Create new file
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Created new file: {file.get('id')}")
