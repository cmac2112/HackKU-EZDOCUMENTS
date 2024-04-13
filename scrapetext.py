import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the text content of the first 10 Google Docs the user has access to.
    """
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
                pageSize=10,
                q="mimeType='application/vnd.google-apps.document'",
                fields="nextPageToken, files(id, name)"
            )
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No Google Docs found.")
            return

        print("Google Docs:")
        for item in items:
            doc_id = item["id"]
            doc_name = item["name"]
            # Export the Google Doc as plain text
            request = service.files().export_media(fileId=doc_id, mimeType="text/plain")
            response = request.execute()
            print(f"Content of {doc_name} ({doc_id}):")
            print(response.decode("utf-8"))
            print("=" * 50)
    except HttpError as error:
        # Handle errors from Drive API
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    print("Starting OAuth flow...")
    main()
