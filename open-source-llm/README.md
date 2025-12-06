# Open Source LLM

### 1: Intro

- Open source LLMs
    - LLaMa
    - FLAN-T5
    - Mistral
- We will replace the ChatGPT with an open source LLM in the RAG flow

### 2: GPU in Saturn Cloud

- Open source LLMs require GPU
- Other options
    - Google Colab
    - Sagemaker
- Saturn Cloud
    - Add secrets used for ENV in notebook
    - Choose saturn-python-llm image
    - Required extra packages
        - transformers
        - accelerate
        - bitsandbytes
- Google Colab
    - Required extra packages
        - transformers
        - accelerate
        - bitsandbytes
    - Check runtime with `!nvidia-smi`

### 3: FLAN-T5

- The model
    - `google/flan-t5-xl` published on Hugging Face
- Hugging Face
    - Repository for publishing models
    - `transformers`
        - The library that is used to download models from Hugging Face
- Tokenizer
    - A tool converting the raw language text into the smaller units that models can understand
- Flow
    - input_text ⇒ tokenizer(input) ⇒ model.generate(tokens) ⇒ decode(outputs)
- Parameters
    - max_length: for longer responses
    - temperature: lower → confident, higher → diversity, typical 0.7 - 1.5

### 4: Phi-3-mini

- The model
    - `microsoft/Phi-3-mini-128k-instruct` published on Hugging Face
- Flow
    - message ⇒ pipeline(model, tokenizer, generation_args) ⇒ output

### 5: Mistral-7B

- The model
    - `mistralai/Mistral-7B-v0.1` published on Hugging Face
    - It is a completion model that takes plain text as input and continues it without any chat structure, it just predicts the next tokens based on the prompt
- To use the Mistral model, it requires to accept their agreement
    - Create access token on Hugging Face
    - Create an environment variable to access it on the notebook
- To login
    - from huggingface_hub import login
    - login(token=os.environ[’my_token’])
- To load model
    - AutoModelForCausalLM.from_pretrained()
- To tokenize
    - AutoTokenizer.from_pretrained()
- Flow
    - tokenizer(message) ⇒ model.generate(input) ⇒ batch_decode(output)
- We can save the model in our local and load it later and can deploy with FastAPI as well
- Base Model vs Instruct Model
    - Base
        - Read the text and predict the next tokens, not designed to follow instructions
    - Instruct
        - Fine-tuned to follow directions like “explain this”, or “write code”

### 6: Exploring Open Source Models

- Other models
    - `LLM360/Amber`
    - `google/gemma-7B`
    - `openlm-research/open_llama_7b`
- How to find good models
    - Open LLM Leaderboard
    - Open LLM Perf Leaderboard
- Quantization
    - The process of reducing the precision of model weights
        - 16-bits or 32-bit floats down to 8-bit, 4-bit, or 2-bit
    - Pros
        - Less RAM
        - Run faster
        - Can run on smaller hardware
    - Cons
        - Loss in accuracy, but acceptable

### 7: Running LLMs locally without CPU with Ollama

- Ollama
    - It’s a service to run LLM locally
    - Docker image is also available
- We will replace OpenAI with Ollama in the OpenAI API
    - base_url=”<local-url>”
    - api_key=”ollama”
- Ollama CLI
    - To start server
        - `ollama start`
    - To run model
        - `ollama run <model>`
    - To download model
        - `ollama pull <model>`

### 8: Ollama & Elasticsearch in Docker-Compose

- For containerization, docker-compose will be used for
    - Ollama
    - Elastic-search
- Once the containers are started, we need to pull the model
    - The model we will use: `phi3`
- We will update the RAG flow with below
    - query ⇒ elastic-search → context ⇒ ollama/phi3 → output

### 9: Streamlit UI

- Streamlit will be serve as UI for our RAG app
- Streamlit CLI
    - To run Streamlit
        - `streamlit run app.py`