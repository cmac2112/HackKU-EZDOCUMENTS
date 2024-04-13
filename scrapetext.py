import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from storage_service import StorageService #my class to store and embedd

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
#most of this is from the google drive api quickstart guide
#i have talored it to my needs


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

        results = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.document' and name contains 'notes'",
                orderBy="name",
                fields="nextPageToken, files(id, name)"
            )
            .execute()
        )

        items = results.get("files", [])

        if not items:
            print("No Google Docs with 'notes' in the name found.")
            return

        storage_list = []
        print("Google Docs:")
        for item in items:
            doc_id = item["id"]
            doc_name = item["name"]

            request = service.files().export_media(fileId=doc_id, mimeType="text/plain")
            response = request.execute()

            print(f"Content of {doc_name} ({doc_id}):")
            print(response.decode("utf-8"))
            storage_list.append(response.decode("utf-8"))

    except HttpError as error:
        print(f"An error occurred: {error}")

    storage_service = StorageService(storage_list)
    storage_service.get_embed_and_store()

if __name__ == "__main__":
    print("Starting OAuth flow...")
    main()
