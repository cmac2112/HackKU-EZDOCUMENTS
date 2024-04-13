#place holder for what i need the real app.py to do


#get my docs button
#triggers scrape of all docs
#embedds with gemini
#stores in pinecone
#appears on ui as a list of docs
#OPTIONAL: search bar to search for docs, and edit capability 



import scrapetext
from flask import Flask,render_template, request , jsonify
from chatbot_service import ChatbotService
from interaction_handler import InteractionHandler


  
app = Flask(__name__,template_folder="templates") 
  
@app.route("/") 
def hello(): 
    return render_template('index.html') 


    return storage_test[15]
@app.route('/process', methods=['POST']) 
def process(): 
    user_query = request.form.get('query')
    print(user_query)
    #poc here then split it up to its own classes for architecural bounds
    index_name = "hackku"
    pinecone_name = InteractionHandler(index_name)
    index = pinecone_name.get_index()
    #now query gemini
    new_query = ChatbotService(user_query, index)
    get_response = new_query.input_query()
    print(get_response)

    return get_response

@app.route('/testing', methods=['POST'])
def testing():
    data = request.form.get('data') #leftover function, keep as an example
    if data == 'magic word':
        v1 = "YOU SAID THE"
        adding_space = ' '
        new_data = adding_space + data
        v2 = v1 + new_data
        return v2
    else:
        v3 = 'wrong'
        return v3
    
if __name__ == '__main__': 
    app.run(debug=True)