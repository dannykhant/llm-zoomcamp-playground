# Module: 3

### 3.1: Evaluation Metrics for Retrieval

- Selecting evaluation metrics are depending on the type of data and requirements
- Ground truth data
    - The correct answers to compare
- Evaluation metric
    - The way of measuring the performance against ground truth data
        - Checking whether retrieved documents == ground truth
    - The reason is to check retrieval quality and answer quality
- Some evaluation metrics for ranking
    - Hit Rate
    - Mean Reciprocal Rank

### 3.2: Ground Truth Dataset Generation for Retrieval Evaluation

- Ground truth is also known as gold standard
- Process
    - Plan to generate 5 questions for each FAQ record using LLM
        - In real world, human annotators can be used for
            - generating ground truth data
            - evaluating the answer using queries
    - Generate the document id using the combined data in each record
        - Combine the course name, question, a few texts
        - Hash the combined texts to serve it as ID
    - Generate the user questions using LLM
        - Create the prompt to generate question for each FAQ record
        - Parse the questions
            - question, course, document_id
        - Export the questions dataframe as CSV
- Python `defaultdict` collection
    - It automatically assigns a default value to keys that don’t exist
    - It can be used to check unique records like using groupBy

### 3.3: Evaluation of Text Retrieval Techniques

- Plan
    - We will check for all the questions from ground truth data
        - Query the result for the question
        - Check whether documents are the same or not
    - Metrics we will use are -
        - Hit Rate
            - Check whether it is able to retrieve the relevant document
        - Mean Reciprocal Rank
            - Check whether able to retrieve the relevant document and how good the ranking is
- HIt Rate
    - Hit Rate = Total relevant results / Total results
        - Total relevant results → the number of the queries that has the relevant document exists in top 5 document list
        - Total results →the total number of queries
- MRR
    - MRR = Total relevant results calculated with rank / Total results
        - Total relevant results with rank
            - 1 / the position of document exists in the top 5 document list of the result
                - 1 ⇒ 1
                - 2 ⇒ 1 / 2
                - 3 ⇒ 1 / 3
                - 4 ⇒ 1 / 4
                - 5 ⇒ 1 / 5
                - rank ⇒ 1 / rank

### 3.5: Evaluation and Monitoring in LLM

- RAG flow
    - search(query) ⇒ build_prompt(search_result) ⇒ llm(prompt) ⇒ answer
- Evaluating retrieval
    - Hit rate
    - MRR
- How do we evaluate for →
    - Prompt
    - LLM
- Evaluation
    - Offline evaluation
        - Cosine similarity
            - The measurement of how close the answer that LLM produced to the answer we expect
            - Using the ground truth dataset
                - answer_original → question → answer_llm
                - cosine_similarity(answer_original, answer_llm)
                    - This provides how good the RAG system is
        - LLM as a judge
            - llm_as_a_judge(answer_original, answer_llm)
                - How similar they are, how good the answers is
    - Online evaluation
        - A/B tests and experiments
        - User feedback
- Monitoring
    - Overall health of the system
    - How good the answer is

### 3.6: Offline RAG Evaluation

- Offline evaluation
    - The evaluation before rolling out the RAG system
- The evaluation flow
    - Load documents with ID
    - Load ground truth dataset
    - Index the data for text vectors using sentence transformers
        - model: `multi-qa-MiniLM-L6-cos-v1`
    - Retrieve the data from vector store
    - RAG Flow
    - Offline Evaluation
        - Cosine similarity metric
            - Dot product
                - `vector_ans_llm.dot(vector_ans_orig)`
                    - vector_ans_orig
                    - vector_ans_llm
- We can use multi-threading for the getting results from LLM

### 3.7: Cosine Similarity

- Evaluating GPT-4o vs GPT-3.5
    - The mean of GPT-4o
        - 0.67
    - The mean of GPT-3.5
        - 0.65
    - The mean of GPT-4o-mini
        - 0.68
- Computing similarity
    - The dot product of two vectors (ans_orig, ans_llm)
- Creating distribution plot
    - import seaborn as sns
    - sns.distplot()

### 3.8: LLM as a Judge

- Creating prompts using LLM
    - You are an expert prompt engineer and create the prompt for the following →
        - Prompt 1
            - There are original answer, generated question and generated answer and I want LLM to analyze how similar and relevant they are, the output should be such as “non-relevant”, “partly-relevant”, “relevant” depending on how relevant the answer is
            - The reason:
                - We can use this for our offline evaluation
        - Prompt 2
            - I have only question and generated answer, I want LLM to analyze how relevant the answer is, the output should be such as “non-relevant”, “partly-relevant”, “relevant” depending on how relevant the answer is
            - The reason:
                - There are some cases that we don’t have the original answers
                - When we need to do the online evaluation on the fly, we will need this
- Using the prompt template with original answers, questions and generated answers, we can get the result data in JSON format