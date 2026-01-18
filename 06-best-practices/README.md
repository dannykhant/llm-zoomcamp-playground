# Module: 6

### 6.1: Techniques to Improve RAG Pipeline

- Indexing stage
    - Parse initial documents
    - Split texts into chunks or paragraphs
    - Embed each chunk into a vector
    - Store the vectors in a database
- Q&A stage
    - Turn user question into vector form
    - Extract top K document from database
    - Show question and most relevant documents to LLM
    - LLM returns answer
- Tip to improve retrieval part
    - Small to big chunk retrieval
        - Choose the right embedding size of the chunks
        - Use small chunks on indexing stage and large chunks on Q&A stage
    - Leveraging document metadata
        - Adding metadata can be useful
        - Ask LLM to produce the metadata
    - Hybrid search
        - Combines 2 methods - vector search and keyword search in a pipeline
        - Vector search is looking for the closest chunks in the embedding space (semantic search)
        - Keyword search is looking for the matches of the separate words (lexical search)
    - User query rewriting
        - Users are not always good at formulating the questions
        - Rephrase user questions into more better structured way using LLM
    - Document reranking
        - Documents with highest embedding similarity may not be the most relevant
        - Rerank the retrieved document chunks using LLM

### 6.2: Hybrid Search

- **What it is:** Combine *different ways of searching* at the same time.
- **How:** Usually **keyword search** (exact words) + **vector/semantic search** (meaning).
- **Why:** You don’t miss results—keywords catch exact matches, vectors catch similar meaning.
- **Output:** A merged list of candidates.
- Equation
    - `hybrid_score = (1 - a) * match_score + a * vec_score`

### 6.3: Document Reranking

- **What it is:** Reorder results you already found.
- **How:** Use a stronger model (often a cross-encoder/LLM) to score each result against the query.
- **Why:** Put the *best* results at the top.
- **Output:** Same results, better order.
- Relevance score
    - NDCG
    - MAP@k
    - Reciprocal Rank Fusion (RRF)

### 6.4: Hybrid Search with LangChain

- LangChain
    - It’s a framework for developing applications powered by LLMs
- A retriever is an interface that returns documents given an unstructured query.
    - It is more general than a vector store.
    - A retriever does not need to be able to store documents, only to return (or retrieve) them.