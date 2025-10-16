import faiss
import openai
import PyPDF2
import numpy as np
import pickle

openai.api_key = ""

def pdf_to_vectors(Path):
    with open(Path,'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        total_page = len(pdf_reader)

        page_texts = []
        for page_num,page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            page_texts.append({
                'text': page_text,
                'page_number':page_num+1
            })

            text = ''.join(p['text'] for p in page_texts)
        print("Total Pages: ",total_page)
        print("total text Length: ",len(text))
        chunks = []
        chunk_metadata = []

        for i in range(0,len(text),400):
            chunk_text = text[i:(i + 500)]
            chunks.append(chunk_text)


