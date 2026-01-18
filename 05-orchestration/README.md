# Module: 5

### 5.1: LLM Orchestration - Ingest

- Bring text/data from a single source into a pipeline so it’s usable for downstream steps
    - API Data Loader
    - Custom code
    - Github repository loader
    - Local file loader
- Mage
    - Data pipeline tool for ETL tasks, data flow, orchestrating transformations

### 5.2: Chunking

- Once the data is ingested, we break it into manageable chunks: smaller, semantically meaningful pieces
- Chunking a foundational step in building RAG pipeline because it balances granularity with coverage

### 5.3: Tokenization

- The process of splitting text into basic units (tokens) that LLM understands
- LLM responses are constrained by the number of tokens in the input plus the response
- Tokenization is a crucial step in text processing and preparing the data for effective retrieval

### 5.4: Embed

- Embedding data translates text into numerical vectors that can be processed by models
- Two texts with similar meaning end up close in vector space
- This makes easier to do semantic search rather than simple keyword matching

### 5.5: Export

- After processing, data needs to be exported for storage so that it can be retrieved for better contextualization of user queries
- It can be stored in any vector databases such as Elasticsearch, Qdrant, Pinecone, etc…

### 5.6: Retrieval - Test Vector Search Query

- After exporting the chunks and embeddings, we can test the search query to retrieve relevant documents on sample queries
- Retrieval supplies real context from curated corpus, greatly improving accuracy and relevance of responses

### 5.7: Trigger Daily Runs

- Automation is key to maintaining and updating systems
- Mage can schedule and trigger daily runs for data pipelines, ensuring up-to-date and consistent data processing