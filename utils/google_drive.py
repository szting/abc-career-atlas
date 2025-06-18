import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class GoogleDriveManager:
    def __init__(self):
        self.folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.service = None
        self.initialize_service()
    
    def initialize_service(self):
        """Initialize Google Drive service"""
        try:
            # Check if service account credentials file exists
            creds_file = 'service_account_key.json'
            if os.path.exists(creds_file):
                credentials = service_account.Credentials.from_service_account_file(
                    creds_file,
                    scopes=['https://www.googleapis.com/auth/drive.file']
                )
                self.service = build('drive', 'v3', credentials=credentials)
            else:
                st.warning("Google Drive service account credentials not found. Cloud backup disabled.")
        except Exception as e:
            st.error(f"Failed to initialize Google Drive service: {str(e)}")
    
    def upload_file(self, local_path, drive_path):
        """Upload a file to Google Drive"""
        if not self.service or not self.folder_id:
            return None
        
        try:
            file_metadata = {
                'name': os.path.basename(drive_path),
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(local_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return file.get('id')
        
        except Exception as e:
            st.error(f"Failed to upload to Google Drive: {str(e)}")
            return None
    
    def download_file(self, file_id, local_path):
        """Download a file from Google Drive"""
        if not self.service:
            return False
        
        try:
            request = self.service.files().get_media(fileId=file_id)
            with open(local_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
            return True
        
        except Exception as e:
            st.error(f"Failed to download from Google Drive: {str(e)}")
            return False
    
    def list_files(self, folder_name=None):
        """List files in Google Drive folder"""
        if not self.service or not self.folder_id:
            return []
        
        try:
            query = f"'{self.folder_id}' in parents and trashed = false"
            if folder_name:
                query += f" and name contains '{folder_name}'"
            
            results = self.service.files().list(
                q=query,
                fields="files(id, name, createdTime, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
        
        except Exception as e:
            st.error(f"Failed to list files from Google Drive: {str(e)}")
            return []
    
    def create_folder(self, folder_name):
        """Create a folder in Google Drive"""
        if not self.service or not self.folder_id:
            return None
        
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.folder_id]
            }
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            return folder.get('id')
        
        except Exception as e:
            st.error(f"Failed to create folder in Google Drive: {str(e)}")
            return None
    
    def delete_file(self, file_id):
        """Delete a file from Google Drive"""
        if not self.service:
            return False
        
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        
        except Exception as e:
            st.error(f"Failed to delete file from Google Drive: {str(e)}")
            return False
    
    def share_file(self, file_id, email, role='reader'):
        """Share a file with a specific email"""
        if not self.service:
            return False
        
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            
            self.service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id'
            ).execute()
            
            return True
        
        except Exception as e:
            st.error(f"Failed to share file: {str(e)}")
            return False
