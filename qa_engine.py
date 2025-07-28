from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def answer_question(context_chunks, question, openai_api_key=None):
    context = " ".join(context_chunks)

    result = qa_pipeline(question=question, context=context)

    return result["answer"]
