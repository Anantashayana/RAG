# from transformers import RagTokenizer, RagTokenForGeneration
# from transformers import DistilBertTokenizer, DistilBertModel
from transformers import T5Tokenizer, T5ForConditionalGeneration
import chromadb
from embedding import CustomEmbeddingFunction
# from sentence_transformers import SentenceTransformer
import nltk
nltk.download('punkt')
import re
# import openai 
# openai.api_key = ""
# client = OpenAI(api_key="")

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
# Initialize the tokenizer and model
# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
# model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# Initialize the model and tokenize
# model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq")  #2GB
# tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")

# model = SentenceTransformer('distilbert-base-nli-mean-tokens')
client = chromadb.PersistentClient(path="./data")
collection_name = "rag"
# client.delete_collection(name=collection_name) # Delete a collection and all associated embeddings, documents, and metadata. ⚠️ This is destructive and not reversible
collection = client.get_or_create_collection(name=collection_name)#,  embedding_function=CustomEmbeddingFunction()) 


def getData(path='./doc.txt'):
    # loc = './doc.txt'
    with open(path,'r', encoding='utf-8') as f:
        text = f.read()
    pattern = r'[^\w\s\.]'
    # Replace special characters with an empty string
    cleaned_text = re.sub(pattern, '', text)    
    return cleaned_text

def formData(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

def generate_ids(input_list):
    ids_list = [str(id(item)) for item in input_list]
    return ids_list


def insertToDB(document,ids):
    # collection = client.get_or_create_collection(name=collection_name)#,  embedding_function=CustomEmbeddingFunction()) 
    # client.delete_collection(name=collection_name)
    collection = client.get_or_create_collection(name=collection_name)#,  embedding_function=CustomEmbeddingFunction()) 
    collection = client.get_or_create_collection(name=collection_name)#,  embedding_function=CustomEmbeddingFunction()) 
    collection.add(documents=document, ids=ids)


def queryDB(query):
    collection = client.get_or_create_collection(name=collection_name)#,  embedding_function=CustomEmbeddingFunction()) 
    result = collection.query(query_texts=[query],
                          n_results=5, include=["documents", 'distances',])
    return result

# i=1
# for dat in data:
#     embedding = convert_to_embeddings(dat)
#     i=i+1
#     insertToDB(embedding, dat, str(i))
# print(queryDB("What is Babylon?"))



def insertData(path):
    text = getData(path)
    sentences= formData(text) 
    ids = generate_ids(sentences)
    insertToDB(sentences,ids)

def queryDB2(query):
    result = queryDB(query)
    documents = result.get('documents')[0]
    # inputs = [query + " [SEP] " + sentence for sentence in documents]
    # encoded_inputs = tokenizer(inputs, return_tensors='pt', padding=True, truncation=True, max_length=512)
    # outputs = model(**encoded_inputs)
    # sentence_representations = outputs.last_hidden_state.mean(dim=1)
    # # Now you can use these representations to form an answer
    # # For example, you can take the average of all sentence representations
    # answer_representation = sentence_representations.mean(dim=0)

    # # Convert the answer representation back to text
    # answer = tokenizer.decode(answer_representation, skip_special_tokens=True)
    sentences =  " ".join(documents)
    # response = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "system", "content": "I will give you both question and answers you nedd to form a better answer"},
    #     {"role": "user", "content": "{query}"},
    #     {"role": "assistant", "content": "{sentences}"},
    #     {"role": "user", "content": "Based on the Query and Text give form better 4-5 line answer. "}
    # ]
    # )

    input_text = f"I am giving you both Query and information related to it. Use that to make better answer for give query.  Query:{query} and Answer: {sentences}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids)
    result = tokenizer.decode(outputs[0])
    return result


if __name__ == "__main__":
    """
    # text = getData()
    # sentences= formData(text) 
    # ids = generate_ids(sentences)
    # #print(f"Document:{sentences}, \n IDs:{ids}")
    # insertToDB(sentences,ids)
    """
    query = "What is The Brothers Karamazov?"
    result = queryDB(query)
    print("Query:", query)
    print("Most similar sentences:")
    # Extract the first (and only) list inside 'ids'
    ids = result.get('ids')[0]
    # Extract the first (and only) list inside 'documents'
    documents = result.get('documents')[0]
    # Extract the first (and only) list inside 'documents'
    distances = result.get('distances')[0]

    for id_, document, distance in zip(ids, documents, distances):
        # Cosine Similiarity is calculated as 1 - Cosine Distance
        print(f"ID: {id_}, Document: {document}, Similarity: {1 - distance}")


    print("########################################")
    print(result.get('documents'))

    print("########################################")
    print(queryDB2(query))
