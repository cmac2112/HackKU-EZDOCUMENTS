import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from storage_service import StorageService  # my class to store and embed
from doc_name_storage import DocNames  # my class to store doc names

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8081)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API to list the first 10 Google Docs
        results = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.document'",
                fields="nextPageToken, files(id, name)"
            )
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No Google Docs found.")
            return

        # List to store document names
        doc_names = []
        doc_ids = []
        print("Google Docs:")
        for item in items:
            doc_id = item["id"]
            doc_name = item["name"]
            if "notes" in doc_name.lower():  
                doc_names.append(doc_name)  
                doc_ids.append(doc_id)

                # Export the Google Doc as plain text
                request = service.files().export_media(fileId=doc_id, mimeType="text/plain")
                response = request.execute()

                # Decode the response from bytes to string
                text_content = response.decode("utf-8")

                # Split the text into paragraphs
                paragraphs = text_content.split("\n\n")  # Assuming paragraphs are separated by two newlines
                # Store each paragraph
                storage_service = StorageService(paragraphs)
                storage_service.get_embed_and_store()

    except HttpError as error:
        print(f"An error occurred: {error}")

    return doc_names, doc_ids

if __name__ == "__main__":
    print("Starting OAuth flow...")
    main()
