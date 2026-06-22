# Module: 2

### 2.1: Vector Search & Qdrant

- Traditional keyword search
    - Search happens on matching keywords
- Vector search
    - Able to match the query and the image or video or sound
    - Capable of matching the different texts but with the same meaning
        - VS works at semantics level
    - By using the vectorized representation of the texts, it can check the similarity of texts by measuring numerically with similarity metrics
- Qdrant
    - An opensource vector search engine to make vector search scalable
    - Written in Rust to be fast & scalable
- Required libraries
    - qdrant-client
        - For connecting Qdrant
    - fastembed
        - For vectorizing data

### 2.2: Embedding Text Data

- To embed the text data with Qdrant
    1. Connect to Qdrant instance with `QdrantClient`
        - Create a Qdrant client
    2. Study the dataset
        - To figure out the structure of data
            - Modality - text, images, videos or combination?
            - Specifics - if text: language used, how big text pieces are, any special char, etc…
        - It helps to define
            - Right schema - what to vectorize, what to store as metadata
            - Right embedding model - best fit based on domain, precision & resource requirement
        - Process flow of vector search
            - text (answers) ⇒ embedded NN ⇒  vectors ⇒ store in vector index
            - questions ⇒ embedded NN ⇒ vectors ⇒ compare in vector index
                - receives the most semantically similar answer
    3. Choose the embedding model with `FastEmbed`
        - Test & benchmark different options on data to select embedding model
        - FastEmbed
            - Supported embedding models
                - Dense text embeddings
                    - For text & image
                - Sparse text embeddings
                    - BM25 & sparse neural embeddings
                - Multivector embeddings
                    - ColPali & ColBERT, late interaction models
                - Rerankers
            - To view the supported models
                - from fastembed import TextEmbedding
                - TextEmbedding.list_supported_models()
            - To find the suitable embedding model
                - Check the dimension we’re interested
                - Check the similarity metric used in the selected model
            - Cosine Similarity
                - Measuring the cosine angle of two vectors
                    - Narrow angles are closed to 1
                        - Semantically similar objects
                    - The angles of opposite vectors are closed to -1

### 2.3: Indexing Data & Studying it Visually

- To index the text data with Qdrant
    1. Create a collection
        - It needs to specify:
            - Name:
                - Unique identifier for the collection
            - Vector configuration:
                - Size: the dimensionality of the vectors
                - Distance Metric: The method used to measure similarity between vectors
    2. Create, embed & insert points into the collection
        - Points consist of:
            - ID: unique identifier
            - Vector: embedding that represents the data point in vector space
            - Payload (optional): additional metadata as key-value pairs
        - Steps
            - FastEmbed will download the selected model & perform inference directly
            - The generated points will be upserted into the collection and the vector index will be built
- Entities in Qdrant
    - Point
        - A data point that has ID and embedding vectors along with optional metadata (payload)
    - Collection
        - It is a container of all data points that solves a business problem
- Qdrant supports batch upsert in both column & record oriented formats
    - Python client supports:
        - Parallelization
        - Retries
        - Lazy batching
- We can visualize the vectors in the Qdrant dashboard

### 2.4: Semantic Similarity Search

- To run the similarity search
    - client.create_payload_index()
    - client.query_points()
- How similarity search works
    - Qdrant compares the query vector to the stored vectors using the distance metric
    - The closest matches are returned, ranked by similarity
- ANN
    - Vector index is built for approximate nearest neighbor (ANN) search, making large-scale vector search feasible

### 2.5: RAG with Vector Search

- Vector Search
    - Create Qdrant client
    - Set embedding_dimensionality and model_handle
    - Create collection
    - Create payload index
    - Add all the documents into a list
    - Upsert all the points into the collection
    - Execute the vector search and get the result
        - client.query_points()
            - To do the search
        - models.Document()
            - To embed into vector
        - models.Filter()
            - To filter the vector
- RAG Flow
    - Search context ⇒ Build prompt ⇒ Get result from LLM

### 2.6: Hybrid Search

- Keyword-based search can also be implemented as vector search but the vectors will be sparse
- Sparse vector
    - The majority of dimensions of sparse vectors are zeros
- If vectors are sparse, the dictionary can grow indefinitely
    - Using flexible dictionary, sparse vectors are used in exact matches such as proper names or identifiers
- BM25
    - It stands for Best Matching 25, and is an industry standard and just a statistical model that makes it fast and lightweight
    - Two key concepts
        - Term Frequency (TF)
        - Inverse Document Frequency (IDF)
    - Scores are generated by BM25 formula
- Steps
    1. Connect to Qdrant
    2. Sparse vector search with BM25
        1. Create a collection with sparse vectors config with setting BM25 and IDF modifier
        2. Upsert the data points with BM25 vector
    3. Running sparse vector search with BM25
        1. Use query_points function with parameters - query and collection_name
    4. Prefetching with Qdrant Universal Query API
        1. query_points() supports building multi-step search pipeline
        2. Retrieval ⇒ Reranking
            1. Retrieve with dense vector search and rerank them with sparse search
        3. Create a new collection 
            1. with vector config with setting jina-small, 512 size and cosine distance
            2. with sparse vector config with setting BM25 and IDF modifier
        4. Upsert the data points with jina-small and BM25 vectors
        5. Use query_points function with parameters
            1. models.Prefetch() with jina-small
            2. query with BM25
    5. Building hybrid search
        1. Hybrid search is a technique for combining results from different search methods
        2. Dense and sparse search scores can’t be compared directly, so we need another method for the final result
        3. Two import terms of hybrid search
            1. Fusion
            2. Reranking
        4. Fusion
            1. The scores of each methods are used to calculate the final scores
            2. Reciprocal Rank Fusion is the most popular technique
                1. Document ⇒ Dense ranking + Sparse ranking ⇒ RRF score ⇒ Final ranking
        5. Use query_points function with parameters
            1. models.Prefetch() with jina-small
            2. models.Prefetch() with BM25
            3. query with models.FusionQuery and RRF
        6. Reranking
            1. Reranking is broader term related to Hybrid Search
                1. Fusion is one of the ways to rerank the results of multiple methods
        7. Dense and sparse vector search might not be enough for some cases
            1. More accurate but slower methods (cross-encoders or multivector representations) exist