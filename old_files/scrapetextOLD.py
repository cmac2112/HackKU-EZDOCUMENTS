import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from storage_service import StorageService  # my class to store and embedd
from doc_name_storage import DocNames  # my class to store doc names

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
# most of this is from the google drive api quickstart guide
# i have tailored it to my needs


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8081)
        # Save the credentials for the next run
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
        print("Google Docs:")
        for item in items:
            doc_id = item["id"]
            doc_name = item["name"]
            if "notes" in doc_name.lower():  # Check if the document name contains the word "notes"
                doc_names.append(doc_name)  # Store the document name in the list
                # Export the Google Doc as plain text
                request = service.files().export_media(fileId=doc_id, mimeType="text/plain")
                response = request.execute()

                #now i need to store this text on its own and send it to flask to be displayed on the front end
    except HttpError as error:
        # Handle errors from Drive API
        print(f"An error occurred: {error}")

    # Store the document names in a separate class for later use in another program
    #doc_names_storage = DocNames(doc_names)
    # Store and embed the text from the Google Docs
    
    storage_service = StorageService(doc_names)  # Pass the list of document names to StorageService
    storage_service.get_embed_and_store()
    # storage and scrape done

    return doc_names
if __name__ == "__main__":
    print("Starting OAuth flow...")
    main()
