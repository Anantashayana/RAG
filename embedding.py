# from transformers import BertTokenizer, TFBertModel
# import tensorflow as tf

# tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
# model = TFBertModel.from_pretrained("bert-base-cased")

# def createEmbedding(text):
#     encoded_input = tokenizer(text, return_tensors='tf')
#     output = model(encoded_input)

#     # Extract the hidden states (last-layer hidden-state of the model)
#     hidden_states = output.last_hidden_state

#     # In BERT, the [CLS] token (first token) embedding is often used as sentence embedding
#     cls_embedding = hidden_states[:, 0, :]

#     return cls_embedding

# print(createEmbedding("Hii My name is Anant, I am in my final year of Engineering"))



#########################################################################################
from chromadb import Documents, EmbeddingFunction, Embeddings 
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from torch import Tensor
import os

# We won't have competing threads in this example app
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Initialize tokenizer and model for GTE-base
tokenizer = AutoTokenizer.from_pretrained('thenlper/gte-base')
model = AutoModel.from_pretrained('thenlper/gte-base')


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(
        ~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def generate_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt',
                       max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)

    attention_mask = inputs['attention_mask']
    embeddings = average_pool(outputs.last_hidden_state, attention_mask)

    # (Optionally) normalize embeddings
    embeddings = F.normalize(embeddings, p=2, dim=1)

    return embeddings.numpy().tolist()[0]


# Inherit from the EmbeddingFunction class to implement our custom embedding function
class CustomEmbeddingFunction(EmbeddingFunction):
    def __call__(self, texts: Documents) -> Embeddings:
        return list(map(generate_embeddings, texts))