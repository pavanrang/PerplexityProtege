# PerplexityProtege
A mini clone or simplified version of the Perplexity AI search assistant.

PerplexityProtege is a mini clone or simplified version of the Perplexity AI search assistant. It is a web application that utilizes the Serper API for search, `llama2-70b-4096` model using Groq API for generating responses. It allows users to input questions, fetch related contexts, generate answers, and display related questions.

## Workflow


1. **User Input**: 
   - Users interact with the Streamlit web interface by entering their questions into the text input field provided.

2. **Search with Serper**:
   - When the user clicks the "Get Answer" button, the application initiates a search using the Serper API based on the user's question.
   - The Serper API fetches relevant contexts, which include snippets of information from various sources such as web pages, articles, and knowledge graphs.

3. **Generate Answer with Groq**:
   - The fetched contexts are then used as input to the Groq API along with the user's question.
   - The application utilizes the `llama2-70b-4096` model provided by Groq for AI completion.
   - Groq generates an answer to the user's question by considering the provided contexts and the question itself.
   - The generated answer is then returned to the application.

4. **Display Answer and Related Questions**:
   - The application displays the generated answer to the user, allowing them to view the response.
   - Additionally, the application uses Groq to generate related questions based on the original question and the fetched contexts.
   - The related questions are displayed to the user, providing additional information or topics related to their query.

5. **Sources Display**:
   - Optionally, the application can display the sources from which the fetched contexts were obtained.
   - This allows users to access the original sources for further reading or verification.

6. **User Interaction**:
   - Users can interact further by exploring related questions, accessing the provided sources, or entering new queries for more information.

7. **Feedback and Improvement**:
   - Users can provide feedback or suggestions for improvement, which can be used to enhance the application's functionality and user experience in future iterations.
  
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/PerplexityProtege.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up API keys:
    - Obtain API keys for Serper API and Groq API.
    - Replace `SERPER_API` and `GROQ_API` constants in the code with your API keys.

## Usage

1. Run the application:

    ```bash
    streamlit run app.py
    ```

2. Access the application in your browser at `http://localhost:8501`.

3. Enter your question in the text input field and click "Get Answer" to fetch the answer and related questions.

   

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.
