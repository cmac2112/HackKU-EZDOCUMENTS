# HackKU-EZDOCUMENTS
Hopefully a good tool for all students using AI. This program will connect user's google docs and google gemini will allow users to ask questions on what is on the notes, write flashcards, test themselves etc.


JSON CREDENTIALS READ ME DO NOT SKIP
my account 'cadenamcarthur@bethelks.edu' is the only one that has access to the app through google apis, let me know during judging if
in order to judge you need access. (918) 521-7500

## Chatbot_Service:
this service queries google gemini using context from pinecone

## scrapetext:
through Oauth2.0 allows the program access to the user's google account to search and scrape text. It will only scrape from documents that have the words 'notes' in them.

## Storage_service:
this service works in tandem with scrape text, it is called in scrape text to embedd and store the list of text in pinecone.

## app.py
holds flask and other functions wip

