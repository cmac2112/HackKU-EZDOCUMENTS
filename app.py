from flask import Flask, render_template, request, jsonify
from chatbot_service import ChatbotService
from interaction_handler import InteractionHandler
import scrapetext
from doc_name_storage import DocNames
import time
import json
from get_doc_text import GetDocText

app = Flask(__name__, template_folder="templates")

# Sample document data
documents = {}

@app.route("/")
def hello():
    return render_template('index.html', documents=documents)

@app.route('/notes')
def notes():
    
    return render_template('notes.html')

@app.route('/refresh_doc_list', methods=['GET'])
def refresh_doc_list():
    global documents
    names = scrapetext.main()
    
    documents.clear()  # Clear the existing document list
    for i, k in enumerate(names):
        documents[f'Document{i+1}'] = k  # Adding new documents to the dictionary
    
    return jsonify({'documents': list(documents.values())})

@app.route('/process', methods=['POST'])
def process():
    user_query = request.form.get('query')
    print(user_query)
    
    # POC here then split it up to its own classes for architectural bounds
    index_name = "hackku"
    pinecone_name = InteractionHandler(index_name)
    index = pinecone_name.get_index()
    
    # Now query gemini
    new_query = ChatbotService(user_query, index)
    get_response = new_query.input_query()
    print(get_response)

    return str(get_response)

@app.route('/testing', methods=['POST'])
def testing():
    names = scrapetext.main()
    print(names)
    return 'Scraping done'

@app.route('/get_doc_text', methods=['POST'])
def get_doc_text():
    data = json.loads(request.data)
    doc_name = data['doc_name']
    # Fetch the document text based on doc_name, assuming scrapetext.main() can retrieve it
    text = GetDocText(doc_name)
    doc_text = text.get_text()
    return jsonify({'text': doc_text})

if __name__ == '__main__':
    app.run(debug=True)
