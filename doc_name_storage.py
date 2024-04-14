class DocNames:
    def __init__(self, texts):
        self.texts = texts
        self.doc_names = []
        #storing doc names so flask can access them later

    def store_doc_names(self):
        for i in self.texts:
            self.doc_names.append(i)
    
    def get_doc_names(self):
        return self.doc_names