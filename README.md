# HackKU-EZDOCUMENTS
Hopefully a good tool for all students using AI. This program will connect user's google docs and google gemini will allow users to ask questions on what is on the notes, write flashcards, test themselves etc.


JSON CREDENTIALS READ ME DO NOT SKIP!

my account 'cadenamcarthur@bethelks.edu' is the only one that has access to the app through google apis, let me know during judging if
in order to judge you need access. (918) 521-7500

## Chatbot_Service:
this service queries google gemini using context from pinecone

input_query() - prompts gemini to provide a response using context from the information stores in pinecone I.E your notes

generate_test() - prompts gemini to create a test using context found in pinecone, user defines what the test is over, prompt is concatenated and then sent to gemini

## scrapetext:
through Oauth2.0 allows the program access to the user's google account to search and scrape text. It will only scrape from documents that have the words 'notes' in them.

triggered when loading documents from the notes page, returns document names to be displayed on the left of the notes page, and document ids to target which documents to be edited.

## Storage_service:
this service works in tandem with scrape text, it is called in scrape text to embedd and store the list of text in pinecone.

get_embed_and_store() - embedds a list of text given to it using gemini embedding, then stores it into pinecone

store_doc_names() - stores the list of document names to be used by flask to display document names on the notes page

## app.py
holds flask and other functions, the main driver of all of the project

## interaction_handler
links gemini and pinecone together, returns the index where everything is being stored to then be used by gemini

## get_doc_text 
quick way to get the text from a google doc onto the screen of notes.html 
Accepts a do name, searches for that doc in the user's google docs, displays the text unless it cant find it

## doc_name_storage
simple method to store doc names for later

