import cohere
from langchain.vectorstores import FAISS
from langchain.embeddings import CohereEmbeddings
import os
from langchain.memory import StreamlitChatMessageHistory
from decouple import config

def get_answer(message, chat_history):
    co = cohere.Client('z3T1qIYOP2WHNB0n6cMWFbHO9y6LSTaqPFMmdFh4')
    ctr = 0
    os.environ["COHERE_API_KEY"] = config("COHERE_API_KEY")    

    embeddings = CohereEmbeddings()

    db = FAISS.load_local("cohere_index", embeddings)


    context = db.similarity_search(message)


    context_str = ""

    for i in context:
        context_str = context_str + i.page_content
        # print(context_str)
        

    temp_prompt = f"You are a chatbot for the synthetic biology competition iGEM made to answer user queries. Your job is to answer questions based on the context provided. Only use the following context to answer the question. If you do not know the answer of the the question say I don't know. Try to structure the output as well as possible. \n Context: %s" %(context_str)
    question_prompt = f"\n Question: %s: " %(message)
    final_prompt = temp_prompt + question_prompt
    # generate a response with the current chat history
    print(f"Chat_History: {chat_history}")
    print(f"Question Prompt: {question_prompt}")

    response = co.chat(
        final_prompt,
        temperature=0,
        max_tokens=100,
        chat_history=chat_history
    )
    answer = response.text
    # print(f"Answer: {answer} \ns")

    # add message and answer to the chat history
    user_message = {"user_name": "User", "text": message}
    bot_message = {"user_name": "Chatbot", "text": answer}

        
    # chat_history.append(user_message)
    # chat_history.append(bot_message)
    
    return answer, user_message, bot_message
