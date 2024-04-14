from flask import Flask, render_template, request, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import scrapetext
import json
from get_doc_text import GetDocText
from chatbot_service import ChatbotService
from interaction_handler import InteractionHandler

app = Flask(__name__, template_folder="templates")

# Google Docs API Setup
SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'hackku-420202-c273e2b45f18.json' #dont steal pls

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service = build('docs', 'v1', credentials=creds)

# global data to allow for editing of documents and name display
documents = {}
docu_id = {}

#inital webpage render
@app.route("/")
def hello():
    return render_template('index.html', documents=documents)
#rendering the quizes page
@app.route('/quizes')
def quizes():
    return render_template('quizes.html')

#test function for scraping the text from the documents
@app.route('/tests', methods=['POST'])
def tests():
    names = scrapetext.main()
    print(names)
    return 'Scraping done'
#rendering the notes page
@app.route('/notes')
def notes():
    return render_template('notes.html')
#refreshing the document list on button press on the notes page
@app.route('/refresh_doc_list', methods=['GET'])
def refresh_doc_list():
    global documents
    global docu_id
    #scraping the text from the documents, returning the document names and ids
    names, ids = scrapetext.main()
    
    documents.clear()  # Clear the existing document list
    docu_id.clear()  # Clear the existing document id list
    
    # Add the new documents to the dictionary required fancy formatting to display the document names and ids
    for i, (name, doc_id) in enumerate(zip(names, ids)):
        document_name = f'Document{i+1}'
        documents[document_name] = name  # Adding new documents to the dictionary
        docu_id[document_name] = doc_id  # Mapping Google Doc IDs to document names
    
    return jsonify({'documents': list(documents.values())})

#function to process the user query and return the chatbot response
@app.route('/process', methods=['POST'])
def process():
    #get the user query
    user_query = request.form.get('query')
    print(user_query)
    
    index_name = "hackku"
    #get the pinecone storage
    pinecone_name = InteractionHandler(index_name)
    index = pinecone_name.get_index()

    #using that storage index, get the chatbot response 
    new_query = ChatbotService(user_query, index)
    get_response = new_query.input_query()
    print(get_response)

    return str(get_response)

#function to generate a test based on the user query
@app.route('/generate_test', methods=['POST'])
def query():
    #very similar to the process function
    user_query = request.form.get('query')
    print(user_query)
    print("Generating test...")
    index_name = "hackku"
    pinecone_name = InteractionHandler(index_name)
    index = pinecone_name.get_index()
    
    #similar but uses new method to generate test instead of general query
    new_query = ChatbotService(user_query, index)
    get_response = new_query.generate_test()
    print(get_response)

    #return the response to the webpage
    return str(get_response)

#function that gets the text from the document to be displayed in the middle of the notes page
@app.route('/get_doc_text', methods=['POST'])
def get_doc_text():
    data = json.loads(request.data)
    doc_name = data['doc_name']
    text = GetDocText(doc_name)
    doc_text = text.get_text()
    return jsonify({'text': doc_text})

@app.route('/save_doc_text', methods=['POST'])
def save_doc_text():
    data = json.loads(request.data)
    doc_name = data['doc_name']
    text = data['text']
    
    # Convert the doc_name to the format 'Document1', 'Document2', etc.
    document_key = next((key for key, value in documents.items() if value == doc_name), None)
    
    if document_key:
        doc_id = docu_id[document_key]
    
        # Get the current content length of the document
        doc = service.documents().get(documentId=doc_id).execute()
        content_length = len(doc['body']['content'])

        # Clear the existing text and insert the edited text
        body = {
            'requests': [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': content_length
                        }
                    }
                },
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': text
                    }
                }
            ]
        }
    
        service.documents().batchUpdate(documentId=doc_id, body=body).execute()
    
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Document not found'})


if __name__ == '__main__':
    app.run(debug=True)
