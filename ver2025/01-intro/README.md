# Module: 1

### 1.1: Intro to LLM & RAG

- The problem we will solve
    - The current FAQ document is not very easy to find the answers
    - We will build a solution to response the answers for the student questions by using LLM and RAG
- LLM
    - It stands for Large Language Model
    - Language models are the things that predicts the next words (tokens) based on the words you typed in, for example - you typed “how are” and it suggests “you”
    - LLM is just language model that is trained with tons of parameters and trained on tons of data inside
    - Input (Prompt) ⇒ LLM ⇒ Answer
- RAG
    - It stands for Retrieval Augmented Generation
        - Retrieval = Search
        - Generation = LLM
    - Components
        - Knowledge Base (KB)
        - LLM
    - RAG Framework
        - `User` → query ⇒
            - `Database (KB)` → context ⇒
                - question & context → `LLM` → answer ⇒ `User`

### 1.2: Environment Configuration

- Python Dependencies
    - tdqm
    - notebook
    - openai
    - elasticsearch
    - scikit-learn
    - pandas
- OpenAI
    - Go to the URL
        - `platform.openai.com`
    - Create an API key to connect to OpenAI
    - Set the key in the environment
        - export OPENAI_API_KEY=”…”
    - Connecting to OpenAI
        
        ```python
        from openai import OpenAI
        
        client = OpenAI()
        response = client.chat.completions.create(
        	model="gpt-4o"
        	message=[{"role": "user", "content": "how to enroll"}]
        )
        ```
        

### 1.3: Retrieval & Search

- We will search the information from knowledge base to create context for the question users asked
- Use `minsearch` as search engine
    - pip install minsearch
- Index the documents from a JSON file with `minsearch.index()`
    - text_fields
    - keyword_fields
- Perform the search with `index.search()`
    - query
        - The query string
    - filter_dict
        - Filtering the results by keyword
    - boost_dict=boost
        - The weight of the importance of the fields
    - num_results
        - The number of top results to return

### 1.4: Generating Answers with `gpt-4o`

- We will send the search result as context to LLM for the question users asked
- Create client for chat completion API below
    - model=”gpt-4o”
    - message=[{”role”: “user”, “content”: q}]
- Create prompt template to give a role
    - prompt_template
        - You’re a teaching assistant. Answer the QUESTION based on the CONTEXT.
        - QUESTION: {question}
        - CONTEXT: {context}
- Create context to send to LLM
    - context += “section: {doc[’section’]}\nquestion: {doc[’question’]}\nanswer: {doc[’answer’]}\n\n”

### 1.5: RAG Flow: Cleaning & Modularizing Code

- Create the function to search context
- Create the function to build the prompt with the context
- Create the function to send the prompt to LLM
- Create the function to put every functions into one group

### 1.6: Search with Elasticsearch

- Import modules
    - from elasticsearch import Elasticsearch
- Create client
    - es_client = Elasticsearch(”localhost:9200”)
- Create index settings for the search
    - text, section, question ⇒ text
    - course ⇒ keyword
- Create an index for the course-questions
    - es_client.indices.create(index=index_name, body=index_settings)
- Index the data with the index created
    - es_client.index(index=index_name, document=doc)
- Create the progress with tqdm
    - from [tqdm.auto](http://tqdm.auto) import tqdm
- Create search-query to query the data
    - “question^3”
        - It means - question is 3 times more important
    - size
        - To return only 5 results
- Send the search query
    - response = es_client.search(index=index_name, body=search_query)