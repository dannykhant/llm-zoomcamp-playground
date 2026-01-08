# Agentic RAG

### Agenda

- Intro to RAG
    - RAG consists of 3 parts →
        - Search relevant context
        - Build prompt
        - Send prompt to LLM
- How to make RAG agentic
- Agentic search
- Function calling

### Building a custom agent without frameworks

- Step-1: Search relevant context
    - from minsearch import AppendableIndex
        - index.fit(doc)
        - index.search(query)
- Step-2: Build prompt
    - Create prompt template
        - Using XML like syntax in the template
            - <Question>What is the question?</Question>
- Step-3: Send the prompt to LLM
    - Using model: GPT-4o of OpenAI

### Agentic RAG

- To build agents that are capable of answering generic questions and specific questions by using the context database
    - We need different approach, and this is where agentic RAG comes into play
        - The agent needs to make decision whether searching context in the database or return directly
            - This becomes Agentic RAG
- Agents can observe the environment and perform the action accordingly
    - The environment could be - chat application
    - Agents can →
        - Perform actions
        - Has history of the actions taken
- Our use-case
    - Actions required
        - To decide to go search context from database or return the response directly
- Procedure
    - Design the prompt for agentic reasoning behavior
        - If context is empty ⇒ search the context
        - If can answer using context ⇒ answer based on context
        - If context doesn’t contain answer ⇒ use own knowledge to answer
    - Check the search result
        - If contains search action ⇒ call the search function

### Agentic Search

- Sometimes it requires multiple iteration of search to provide the answer
- Multi-step agentic search process
    - If context is empty ⇒ create keywords
        - Search context using the `keywords`
        - Add the keywords to the `search_queries`
        - Add the search action to the `previous_actions`
    - If still want to perform search ⇒ create keywords
        - Search context using the `keywords`
        - Add the keywords to the `search_queries`
        - Add the search action to the `previous_actions`
    - If action is not SEARCH or hit the maximum iteration ⇒ break
        - Return the answer

### Function Calling (Tool Use) - Part1

- When we are adding multiple actions to the prompt, it will become complicated and problematic to manage
- Instead of manually defining the actions, we can rely on tool invocation
- The idea behind function calling →
    - Describe what the function does
    - Then let LLM decides when to invoke the function
- Flow
    - Describe the function with the required properties
    - Use the OpenAI’s responses API
    - Split the prompt into →
        - Developer prompt
        - User prompt
    - LLM will ask to use the specific tool from the tools we provide if required
        - We can add more function call iterations by modifying the developer prompt
    - If entry type is `function_call` ⇒ call the function
    - If entry type is `message` ⇒ print the text
- Multiple tools
    - We can add more tools to perform the different actions →
        - Search
        - Add entry
        - etc…

### Function Calling - Part2

- Flow
    - Asking a question
    - Lookup the answer with the search function
        - The search function is defined as a tool with some parameters
    - Input the chat_messages using the developer prompt and question
        - For multiple search tool call, adjust the developer prompt to provide multiple search queries
    - Get the response from LLM
        - response.output includes the function tool call
    - Append each entry from response.output to chat_messages
    - If entry.type == ‘message’ ⇒ output the result
    - If entry.type == ‘function_call’ ⇒ invoke the function
    - Invoke the search function
        - `globals()` is used access global variables
        - Steps
            - entry.arguments has the arguments to pass
            - [entry.name](http://entry.name) is the function name to invoke
            - `fn = globals()[f_name]` will give us the dynamic function name
            - By calling `f(**args)` , we get back the result
    - Append the call_output to chat_messages
    - Get the response from LLM again
- Create the flow with a while-loop to be able to interact with user
- HTML can be used for getting clear formatted output
- `function.__name__` give the name of the function in string format
- Refactoring into Classes
    - IPythonChatInterface()
        - input()
            - To get the user’s question
        - display(content)
            - To display default message
        - display_func_call(name, args, output)
            - For function tool call
        - display_response(md_contend)
            - For final response
    - ChatAssistant()
        - `__init__` with developer_prompt, interface, openai_client
        - run()
            - To run the chat interface
    - Tools()
        - add_tool(func, desc)
            - To add a tool
            - Use generate_description() to add the description
        - get_tools()
            - To get the list of tools
        - function_call()
            - To make the dynamic function call
    - CourseFAQTools()
        - search()
        - add_entry()
- PydanticAI
    - Agent framework for the production
- OpenAI Agents SDK
    - To build agentic AI app