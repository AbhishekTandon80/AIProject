# AI Agent Application

## Overview
This project is an AI-powered chat bot that integrates with both OpenAI and Mistral large language models (LLMs). It supports function calling and can interact with a MongoDB database for dynamic information retrieval.

---

## Features
- Chat with OpenAI or Mistral LLMs
- Function calling for dynamic data (e.g., fetch address or ID by name)
- MongoDB integration for persistent data
- Streamlit-based interactive web UI

---

## Getting Started

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) (recommended)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (for MongoDB)
- [MongoDB](https://www.mongodb.com/try/download/community) (can use Docker)

### Installation

1. **Clone the repository**
    ```sh
    git clone <your-repo-url>
    cd PythonProject
    ```

2. **Create and activate a virtual environment**
    ```sh
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    - Create a `.env` file in the project root with the following content:
      ```
      OPENAI_API_KEY=your_openai_api_key
      MISTRAL_API_KEY=your_mistral_api_key
      ```

5. **Start MongoDB**
    - Using Docker:
      ```sh
      docker run -d -p 27017:27017 --name mongo mongo
      ```
    - Or start your local MongoDB server.

---

## Running the Application

```sh
streamlit run main.py
```

Open the provided local URL in your browser to interact with the chat bot.

---

## Project Structure

```
PythonProject/
│
├── at/
│   ├── mistral/
│   │   └── api_caller.py
│   ├── openai/
│   │   └── api_caller.py
│   └── mongo/
│       └── mongo_util.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## Notes

- Ensure your API keys are kept secret and **never** committed to version control.
- For development and testing, see the `tests/` directory (if present) for unit tests.

---

## License

This project is licensed under the MIT License.