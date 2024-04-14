import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class GetDocText:
    def __init__(self, doc_name):
        self.doc_name = doc_name

    def get_text(self):
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

            # Call the Drive v3 API to list the Google Docs
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
                return None

            # Find the document by name
            doc_id = None
            for item in items:
                if item["name"] == self.doc_name:
                    doc_id = item["id"]
                    break

            if not doc_id:
                print(f"Google Doc '{self.doc_name}' not found.")
                return None

            # Export the Google Doc as plain text
            request = service.files().export_media(fileId=doc_id, mimeType="text/plain")
            response = request.execute()

            # Decode the response from bytes to string
            text_content = response.decode("utf-8")
            return text_content

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

