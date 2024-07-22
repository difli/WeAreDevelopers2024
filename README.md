# WeAreDevelopers Conference 2024 Talk
Accelerating GenAI Development: Harnessing Astra DB Vector Store and Langflow for LLM-Powered Apps

## Abstract

Join Dieter and Michel in this session as they demonstrate how leveraging Astra DB’s vector store and Langflow can significantly expedite the development of applications powered by LLMs. This session will provide a detailed look into how these technologies streamline the creation and deployment of LLM-driven solutions, significantly speeding up development processes.

The session will start with an introduction to the vector capabilities of Astra DB, which are essential for managing the high-dimensional data demands of generative AI applications. We will then focus on how Langflow, a pioneering low-code platform, accelerates the development lifecycle of LLM-powered applications. By facilitating rapid prototyping and iteration, Langflow enables developers to reduce development time dramatically.

## Content

- [Talk Recording](https://www.youtube.com/watch?v=mR-UzyWheX0)
- [PDF Version of the Talk](./assets/Accelerating%20GenAI%20Development.pdf)
- [Demos](#demos)

## Demos

The theme of the demos is the implementation of a Bicycle Recommendation Service. 
![chatbot](./assets/chatbot.jpg)
All demos use the same bicycle catalog as context data. The catalog contains 100 bicycles with the following fields: `id`, `bicycle_type`, `product_name`, `product_description`, and `price`. The field `product_description` is the one that will be vectorized to perform a semantic search to find the perfect bike based on user preferences. The demos cover Astra DB, Astra Vectorize, RAGStack, and Langflow. 

### Demo Overview
1. **Without vs. with RAG**: Shows the impact of Retrieval-Augmented Generation (RAG) on the relevance of responses.
2. **Vectorize the Easy Path**: Illustrates the ease of vectorizing data using Astra DB’s Vectorize capability.
3. **Coding Demo with RAGStack**: Demonstrates the implementation of RAGStack for an LLM-powered application.
4. **No-Coding Demo with Langflow**: Highlights the rapid prototyping capabilities of Langflow for LLM-powered applications.

### Setup Instructions
1. Clone the repository:
    ```sh
    git clone https://github.com/difli/wearedevelopers-2024.git
    cd wearedevelopers-2024
    ```
2. Install the required dependencies:
    ```sh
    pip install -r ./coding/requirements.txt
    ```
3. Make a copy of the [`secrets.toml.example`](./coding/.streamlit/secrets.toml.example) and name the file `secrets.toml`.
    ```sh
    cp ./coding/.streamlit/secrets.toml.example ./coding/.streamlit/secrets.toml
    ```
4. Ensure you have a vector-capable Astra database (get one for free at [astra.datastax.com](https://astra.datastax.com)) on AWS in Region us-east-2. You will need to provide the **API Endpoint**, which can be found in the right pane under *Database details*. Ensure you have an **Application Token** for your database, which can be created in the right pane under *Database details*. Configure your connection details `ASTRA_API_ENDPOINT` and `ASTRA_TOKEN` in the `secrets.toml` file.
![Astra DB](./assets/astra.png)
5. Create an [OpenAI account](https://platform.openai.com/signup) or [sign in](https://platform.openai.com/login). Navigate to the [API key page](https://platform.openai.com/account/api-keys) and create a new **Secret Key**, optionally naming the key. Configure your `OPENAI_API_KEY` in the `secrets.toml` file.
![OpenAI](./assets/openai.png)
6. Execute the [loader.py](./coding/loader.py) script to create the `bicycle_catalog` collection in your Astra DB database and to populate the collection with the bicycle catalog data. Ensure you are within the `coding` folder.
    ```sh
    streamlit run loader.py
    ```

Let's have fun with the demos now!

### 1. Without vs. with RAG
#### Description
This demo shows the impact of Retrieval-Augmented Generation (RAG) on the relevance of responses for LLM-powered applications.

#### Flow of the Demo
1. **Without RAG**
    - Uncheck `Enable Retrieval Augmented Generation (RAG)`
    ![without](./assets/without.jpg)
    - The bicycle recommendations are `generic` without RAG. The listed bicycles are not from our bicycle catalog. The LLM was trained on a vast amount of public data, but not with our private data. Therefore, it does not know about our catalog and cannot recommend any of our specific bikes that we have in our store and want to sell.

2. **With RAG**
    - Check `Enable Retrieval Augmented Generation (RAG)`
    ![with](./assets/with.jpg)
    - The bicycle recommendations are `relevant` with RAG. The listed bicycles are contextually relevant and are from our bicycle catalog. While the LLM is still not trained on our data, a semantic search with Astra DB over our bicycle catalog data retrieves the relevant bikes and provides them as context to the LLM. Now, the LLM can make relevant recommendations based on the bikes we have in our store and want to sell.
### 2. Vectorize the Easy Path
#### Description
This demo illustrates the ease of vectorizing data using [Astra DB vectorize](https://docs.datastax.com/en/astra-db-serverless/databases/embedding-generation.html).

#### Flow of the Demo
1. Create a vector-enabled collection via the Astra DB ui. Choose as vector creation method NVIDIA. This service is hosted on the Astra DB platform side by side with your data. This ensures fastest performance and low cost to vectoraize data when it is loaded.
![create-collection](./assets/create-collection.jpg)
2. Load the bicycles catalog data into your collection. Load [bicycle_catalog_100.json](./vectorize/bicycle_catalog_100.json) and select the field `product_description` as the field to vectorize.
![load-data](./assets/load-data.jpg)
3. Execute a semantic search. Insert `I need a bike that I can take with me when traveling by train` into the vector search field and hit Apply. On top of the Collection data you see the bicycle from the bicycle catalog with its description that is most similar to the vector search text: `Compact Rider 100`. This Bike is from our private context the bicycle catalog and we will see it over the course of the other demos. This is how we retrieve our context that we later pass to the LLM to get a response that is relevant.
![semantic-search](./assets/semantic-search.jpg)


### 3. Coding Demo with RAGStack
#### Description
This coding demo showcases the use of RAGStack for an LLM-powered application.
But also is used to contrast the coding with the no-coding approach.

#### Flow of the Demo
1. Open [requirements.txt](./coding/requirements.txt). `ragstack-ai` provides a curated list of dependencies, tested and maintained by DataStax. RAGStack provides all dependencies that are required to implement any kind of generative ai application with dependency version that are tested to work well together. This is what enterprises need for applications in production.
2. Open the [app.py](./coding/app.py) file see the import statements for modules and classes that come with ragstack-ai.
3. Follow the comments and instructions in the script to understand the implementation. Quite a few of them. The developer need to know about their usage. 
4. Even this is a simple application there is quite some code that needs to be implemented. This takes a while and is errorprone.
5. Run [app.py](./coding/app.py) to see RAG based bicycle recommendation service build with RAGstack in action. Insert `I need a bike that I can take with me when traveling by train` into the vector search field and hit Apply. The recommendation you get is from the bicycle catalog with its description that is most similar to what was inserted in the input field. Again `Compact Rider 100`. This Bike is from our private context the bicycle catalog and we will see it over the course of the other demos. No chance for the LLM to hallucinate as we retrieved the most similar bicycle products based on their description with Astra DB vector search and passed this context to the LLM to generate a response based on this. Ensure you are within the `coding` folder.
    ```sh
    streamlit run app.py
    ```

### 4. No-Coding Demo with Langflow
#### Description
This no-coding demo highlights the rapid development capabilities of Langflow for LLM-powered applications.

#### Flow of the Demo
1. In Astra ui switch to Langflow
![langflow](./assets/langflow.jpg)
2. Hit create `New Project`. Select the `Vector Store RAG` template.
![langflow-new-project](./assets/langflow-new-project.jpg)
3. All demos use Astra vectorize to generate embeddings. To be consistent delete the OpenAI Embeddings component. 
![langflow-delete-open-ai](./assets/langflow-delete-open-ai.jpg)
4. Drag and drop the Astra vectorize component under the embeddings menu into the canvas. Choose `NVIDIA` as provider and insert `NV-Embed-QA` as model. Connect the Astra Vectorize with the Astra DB component.
![langflow-vectorize](./assets/langflow-vectorize.jpg)
5. Select the `bicycle_catalog` in Collection Name for the Astra DB component
![langflow-astra-db](./assets/langflow-astra-db.jpg)
6. Change the template field of the `Parse Data` component to `{data}`. This ensures all data of the retrieved documents from Astra DB goes into the context of the prompt.
![langflow-parse-data](./assets/langflow-parse-data.jpg)
7. Change the prompt template to what is used as prompt in app.py. The prompt is where the programing of our gen ai application happens in english language.
   ```python
   You’re a helpful AI assistant tasked with helping users find the perfect bicycle based on their preferences and needs. You're friendly and provide extensive answers. Use bullet points to summarize your suggestions. Here's how you can assist:
   
   After gathering the user's preferences, provide at least two bicycle products that match their criteria.
   Use bullet points to summarize each suggestion, including key features, benefits, and price.
   Example:
   "Mountain Bike: Trailblazer 300
   Durable frame with advanced suspension system
   Excellent traction for rugged terrain
   Price: $1500"
   "Road Bike: Speedster 200
   Lightweight aerodynamic design
   High-performance tires for speed
   Price: $800"
   
   Encourage Further Questions and Offer Additional Assistance:
   
   "Feel free to ask any more questions or provide additional details if needed. I'm here to help you find the best bicycle for your needs!"
   
   CONTEXT:
   {context}
   
   QUESTION:
   {question}
   
   YOUR ANSWER:
   ```
8. Provide a `OpenAI API Key` for the OpenAI component
![langflow-openai](./assets/langflow-openai.jpg)
9. Execute the flow by hitting `Playground`
![langflow-playground](./assets/langflow-playground.jpg)
10. But that is not all. A flow can be integrated into an application. Let's do that. First [install and run Langflow](https://github.com/langflow-ai/langflow?tab=readme-ov-file#-get-started) local. Import the flow [WeAreDevelopers.json](./no-coding/WeAreDevelopers.json) in your local Langflow instance. Ensure all credentials and fields like above are populated. Hit button `API`. Copy the URL from the `RUN cURL` tab
![langflow-api](./assets/langflow-api.jpg)
11. Paste the URL you have just copied into [app_langflow.py](./coding/app_langflow.py). There is no gen ai related code aka no langchain modules and classes in the code. The code is just about the ui and the integration with langflow where the gen ai flow will be executed. 
![langflow-code](./assets/langflow-code.jpg)
12. Execute your adapted [app_langflow.py](./coding/app_langflow.py) application. Ensure you are within the `coding` folder.
    ```sh
    streamlit run app_langflow.py
    ```
13. This time we get a langflow powered bicycle recommendation service but still the same recommendation based on our bicycle catalog
![langflow-app](./assets/langflow-app.jpg)

## Resources
- [Astra DB Documentation](https://docs.astradb.com)
- [Astra Vectorize](https://docs.datastax.com/en/astra-db-serverless/databases/embedding-generation.html)
- [Langflow Documentation](https://docs.datastax.com/en/ragstack/langflow/index.html)
- [WeAreDevelopers Conference](https://www.wearedevelopers.com/)

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
