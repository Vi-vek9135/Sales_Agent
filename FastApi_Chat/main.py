







@app.post("/qa/")
async def perform_qa(user_input: str):
    # Search Chroma Vector Database for relevant segments
    try:
      relevant_segments = search_chroma_db(user_input)
      
    #   answer = get_answer_using_palm2(relevant_segments, user_input)
      

      sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)
      # init sales agent
      sales_agent.seed_agent()

      while True:
        sales_agent.determine_conversation_stage()
        sleep(2)
        sales_agent.step()

        human = input(f"\nUser Input =>{user_input}  ")
        if human:
            sales_agent.human_step(human)
            sleep(2)
            print("\n")


    #   return {"answer": answer}
    except Exception as e:
      return {"error": f"Error answering question or answer not found: {e}"}
    



def search_chroma_db(question):
    # Add code to query Chroma Vector Database based on user question
    docs = vector_index.get_relevant_documents(question)
    # return relevant_segments
    return docs



def get_answer_using_palm2(relevant_segments, question):
    prompt_template = """
      Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
      provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
      Context:\n {context}?\n
      Question: \n{question}\n

      Answer:
    """


    try:
      if not relevant_segments:
        return "Answer not available in the context."



      prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
      model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
      chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
      response = chain({"input_documents":relevant_segments, "question": question}, return_only_outputs=True)
      return response
    except Exception as e:
       return f"An error occurred while retrieving answer: {str(e)}"






if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",reload=True)