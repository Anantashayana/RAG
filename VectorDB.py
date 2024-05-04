

def getData():
    loc = './doc.txt'
    with open(loc,'r', encoding='utf-8') as f:
        text = f.read()
    print(text)
    return text

def createEmbeddings():
    pass

def insertToDB():
    pass

def matchSimilar():
    pass

import chromadb

if __name__=="__main__":
    # model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    client = chromadb.PersistentClient(path="./data")
    collection_name = "rag"
    client.delete_collection(name=collection_name)
