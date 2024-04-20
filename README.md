# HackKU-EZDOCUMENTS
Hopefully a good tool for all students using AI. This program will connect user's google docs and google gemini will allow users to ask questions on what is on the notes, write flashcards, test themselves etc.

# Demo
https://youtu.be/6iCwlqhiG8Y


# JSON CREDENTIALS READ ME DO NOT SKIP!

my account 'cadenamcarthur@bethelks.edu' is the only one that has access to the app through google apis, let me know during judging if
in order to judge you need access. (918) 521-7500

## How to use
Start the program app.py and click on the localhost link it provides. When it starts
you will be met with a web page of 2 options, left go to notes, right generate a test

Go to Notes: (recommended you come here first)
- The main webpage of the project
- On the left you will find the button named 'Get Your Notes', upon clicking you will be directed to log into your google account so the program has access to your files.
- After the Oauth flow is complete, the program will begin loading the files and putting them on the left side
- When the docs have been loaded you can click on them and view them in the middle. There is also an option to edit each doc when toggling the edit button. 

- When editing the edit button for the doc you are looking at must be pressed, then after your changes are done, scroll down the middle box where the text from the doc is located and click save changes. If it says saved sucessfully you have just edited a doc on your google docs account through this program. If it says unsucessfully, close out all google web pages open, and restart the program.

- On the right side is where the AI assistant comes in. Here you can see an input box and a button named 'query'. When you load your docs on the left side, the program performs a scrape of all the text from documents that have the word 'notes' in their title, then it embedds and stores each paragraph in the text into pinecone as vectors. After that is complete, Gemini should have good context to your notes now.

- After querying Gemini, the bot will respond in a grey text bubble below your text bubble
- A query I have found that works well is 'tell me about user interviews from my notes'


Generate Test: (come here second)
- This page will allow the user to generate a simple practice test based on information in their own notes. This is unique because these tests can contain specific things someone may not find online.

- Similar to the other page, you can enter your query into the box to be sent to Gemini. The prompt on the backend is altered and you are using a different method in the Chatbot_Service to get Gemini to generate a test.
- A good query I have found is similar to the last 'make a test on my user interview notes'

## Closing Thoughts
- First hackathon, I dont think this little program is too bad. I would like to continue it this summer and make it into a real website though. Also I had to keep my json files in here with Google API credentials which is slightly sketchy, please dont do anything with them. 

## Chatbot_Service:
This service queries google gemini using context from pinecone

input_query() - prompts gemini to provide a response using context from the information stores in pinecone I.E your notes

generate_test() - prompts gemini to create a test using context found in pinecone, user defines what the test is over, prompt is concatenated and then sent to gemini

## scrapetext:
Through Oauth2.0 allows the program access to the user's google account to search and scrape text. It will only scrape from documents that have the words 'notes' in them.

Triggered when loading documents from the notes page, returns document names to be displayed on the left of the notes page, and document ids to target which documents to be edited.

## Storage_service:
This service works in tandem with scrape text, it is called in scrape text to embedd and store the list of text in pinecone.

get_embed_and_store() - embedds a list of text given to it using gemini embedding, then stores it into pinecone

store_doc_names() - stores the list of document names to be used by flask to display document names on the notes page

## app.py
Holds flask and other functions, the main driver of all of the project

## interaction_handler
Links gemini and pinecone together, returns the index where everything is being stored to then be used by gemini

## get_doc_text 
Quick way to get the text from a google doc onto the screen of notes.html 
Accepts a do name, searches for that doc in the user's google docs, displays the text unless it cant find it

## doc_name_storage
Simple method to store doc names for later

## Design
- a very very rough design of the architecture can be found here https://www.figma.com/file/A3QI8aUoYKoNBxK0yBC2mk/EZDOCS-Architecture-map?type=design&node-id=0%3A1&mode=design&t=FhGVTbPXO0d9ldDj-1

- This is not exacly how the flow of the program came out to be, but gives an idea to how it was made.
