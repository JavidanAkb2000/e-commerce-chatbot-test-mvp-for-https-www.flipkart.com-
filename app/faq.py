import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

faqs_path = Path(__file__).parent / 'resources/faq_data.csv'
chroma_client = chromadb.Client()
collection_name_faqs = 'faqs'

groq_client = Groq()

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='sentence-transformers/all-MiniLM-L6-v2',
)


def load_faq_data(path):
    if collection_name_faqs not in [c.name for c in chroma_client.list_collections()]:
        print('Ingesting FAQ data into Chromadb...')
        collection = chroma_client.get_or_create_collection(
            name=collection_name_faqs,
            embedding_function=ef
        )
        df = pd.read_csv(path)
        docs = df['question'].to_list()
        metadata = [{'answer': ans }for ans in df['answer'].to_list()]
        ids = [f'id_{i}' for i in range(len(docs))]

        collection.add(
            documents=docs,
            metadatas=metadata,
            ids = ids
        )

        print(f'FAQ Data successfully loaded into Chroma collection: {collection_name_faqs}')
    else:
        print(f'Collection {collection_name_faqs} already exists!')


def get_relevant_qa(query):
    collection = chroma_client.get_collection(collection_name_faqs)
    result = collection.query(
        query_texts=[query],
        n_results=2
    )

    return result

def faq_chain(query):
    result = get_relevant_qa(query)

    context = ''.join([r.get('answer') for r in result['metadatas'][0]])

    answer = generate_answer(query, context)
    return answer


def generate_answer(query, context):
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {query}
    '''

    chat_completion = groq_client.chat.completions.create(
        messages=[ # type: ignore
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=os.environ['GROQ_MODEL'],
        # model = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile'),
        temperature=0.5,  # Even lower for this model - it's good at following instructions
        max_tokens=500
    )

    return chat_completion.choices[0].message.content


if __name__ == '__main__':
    load_faq_data(faqs_path)
    query = "How much of discount HDFC cards usually get?"
    # result = get_relevant_qa(query)
    # print(result)
    answer = faq_chain(query)
    print(answer)