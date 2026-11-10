# DrukAI – Dzongkha AI Chatbot 🇧🇹

DrukAI is an AI-powered chatbot developed to explore the use of Generative AI and Natural Language Processing (NLP) for the Dzongkha language. The project focuses on making AI-based question answering more accessible to Dzongkha users by combining a general-purpose language model with a specialized Dzongkha-English translation model.

The chatbot allows users to ask questions in English or Dzongkha and receive responses in Dzongkha. It also provides basic document support, allowing users to upload PDF and Word documents and ask questions based on their extracted content.

This project is developed using Python and open-source AI technologies, with the language model running locally through Ollama.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Project Objectives](#-project-objectives)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [System Architecture](#-system-architecture)
- [How DrukAI Works](#-how-drukai-works)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Running the Application](#-running-the-application)
- [Models Used](#-models-used)
- [Current Limitations](#-current-limitations)
- [Future Improvements](#-future-improvements)
- [Learning Outcomes](#-learning-outcomes)
- [Acknowledgements](#-acknowledgements)

---

## 📖 Project Overview

Dzongkha is the national language of Bhutan. However, developing AI applications that can understand and communicate effectively in Dzongkha remains challenging because fewer language resources and specialized AI models are available compared with widely used languages such as English.

DrukAI was developed to explore how existing open-source AI models can be combined to build a chatbot that supports Dzongkha communication.

Instead of depending on a single model to perform every task, DrukAI uses a hybrid approach:

- **Qwen2.5:** Handles question understanding and answer generation.
- **NLLB-200:** Handles translation between English and Dzongkha.
- **Ollama:** Runs the language model locally.
- **Streamlit:** Provides the web-based chatbot interface.
- **Document Processor:** Extracts text from uploaded PDF and DOCX files.

The main idea is to use the strengths of different models and combine them into one application.

## 🎯 Project Objectives

The main objectives of this project are:

1. To develop a chatbot that supports interaction in Dzongkha.
2. To explore the application of Generative AI in supporting Bhutan's national language.
3. To integrate a general-purpose language model with a Dzongkha translation model.
4. To implement English-to-Dzongkha and Dzongkha-to-English translation.
5. To develop a chatbot that can answer general and educational questions.
6. To maintain conversation history during chatbot interaction.
7. To allow users to upload PDF and Word documents and ask questions about their content.
8. To gain practical experience in NLP, Generative AI, prompt engineering, and AI application development.

## ✨ Features

### 1. Dzongkha AI Chatbot

Users can enter questions in English or Dzongkha. The chatbot processes the input and provides a response in Dzongkha.

### 2. English-to-Dzongkha Translation

English questions and generated answers are translated into Dzongkha using the NLLB translation model.

### 3. Dzongkha-to-English Translation

When a user enters a question in Dzongkha, the system translates it into English before sending it to the language model.

### 4. AI-Based Question Answering

Qwen2.5 is used to understand questions and generate answers. Users can ask general questions, request explanations, and explore educational topics.

### 5. Conversation History

The application maintains conversation history during an active session, allowing users to continue a conversation with related questions.

### 6. PDF and Word Document Processing

Users can upload PDF and DOCX files. The system extracts readable text from these documents and provides the extracted content as context when answering questions.

### 7. Local AI Model

The main language model runs locally through Ollama, reducing dependence on paid external LLM APIs.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application and chatbot interface |
| Ollama | Running the language model locally |
| Qwen2.5 1.5B | Question understanding and answer generation |
| Hugging Face Transformers | Loading and using the translation model |
| NLLB-200 600M | English-Dzongkha translation |
| PyTorch | Deep learning framework |
| Requests | Communicating with the Ollama API |
| PyMuPDF | Extracting text from PDF documents |
| python-docx | Extracting text from Word documents |
| SentencePiece | Tokenization support for the translation model |

---

## 🏗️ System Architecture

DrukAI follows a hybrid AI architecture where a language model and a translation model work together to generate Dzongkha responses.

### Architecture Diagram

```text
                  USER
                    |
                    v
          Streamlit Chat Interface
                    |
                    v
          Input Language Detection
                    |
             +------+------+
             |             |
             v             v
          English       Dzongkha
             |             |
             |             v
             |       NLLB Translation
             |       Dzongkha to English
             |             |
             +------+------+
                    |
                    v
              Ollama API
                    |
                    v
              Qwen2.5 1.5B
                    |
                    v
              English Answer
                    |
                    v
           NLLB Translation Model
            English to Dzongkha
                    |
                    v
          Dzongkha Chatbot Response
                    |
                    v
                   USER
```

For document-related questions, extracted PDF or DOCX content is also passed to the language model as additional context.

## ⚙️ How DrukAI Works

### A. When the user enters an English question

1. The user enters a question in English through the chatbot interface.
2. The system identifies the input language.
3. The question is sent to Qwen2.5 through the Ollama API.
4. Qwen2.5 generates an answer in English.
5. The NLLB model translates the generated answer into Dzongkha.
6. The final Dzongkha response is displayed in the chatbot.

### B. When the user enters a Dzongkha question

1. The user enters a question in Dzongkha.
2. The system detects the Tibetan script used in Dzongkha.
3. The NLLB model translates the question into English.
4. The translated question is sent to Qwen2.5.
5. Qwen2.5 generates an answer in English.
6. The answer is translated into Dzongkha.
7. The translated response is displayed to the user.

### C. When the user uploads a document

1. The user uploads a PDF or DOCX file.
2. The document processor extracts the readable text.
3. The extracted content is stored as document context.
4. The user asks a question related to the uploaded document.
5. The chatbot uses the question and available document context to generate an answer.
6. The answer is translated into Dzongkha before being displayed.

---

## 📁 Project Structure

The project is organised into different files and folders to separate the chatbot interface, translation functionality, document processing, and chatbot logic.

```text
DrukAI-Dzongkha-AI-Chatbot/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
├── assets/
│
├── data/
│
├── documents/
│
├── models/
│
├── src/
│   ├── chat_engine.py
│   ├── document_processor.py
│   └── translator.py
│
├── tests/
│
├── test_chat.py
│
├── test_document.py
│
└── .venv/
```

### Description of Main Files

| File | Description |
|---|---|
| `app.py` | Main application file that runs the Streamlit chatbot interface. |
| `requirements.txt` | Contains the Python libraries required to run the project. |
| `src/chat_engine.py` | Handles chatbot logic, connects to Ollama, and combines question answering with translation. |
| `src/translator.py` | Loads the NLLB translation model and provides English-Dzongkha translation functions. |
| `src/document_processor.py` | Extracts text from PDF and DOCX documents. |
| `test_chat.py` | Used to test chatbot functionality. |
| `test_document.py` | Used to test document text extraction. |
| `assets/` | Stores images and other application resources. |
| `data/` | Reserved for project datasets and related data. |
| `documents/` | Used for sample documents and document testing. |
| `models/` | Reserved for additional model-related files. |
| `tests/` | Reserved for additional testing files. |

The `.venv/` folder contains the local Python virtual environment and should not be uploaded to GitHub.

---

## 💻 Installation and Setup

Follow these steps to run DrukAI on a Windows computer.

### 1. Clone the Repository

Open PowerShell or the VS Code terminal and run:

```powershell
git clone https://github.com/Jigme2003/DrukAI-Dzongkha-AI-Chatbot.git
```

Move into the project directory:

```powershell
cd DrukAI-Dzongkha-AI-Chatbot
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

Install the required packages using the requirements file:

```powershell
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama from its official website:

https://ollama.com/download

Check whether Ollama is installed:

```powershell
ollama --version
```

### 5. Download the Qwen2.5 Model

Run the following command:

```powershell
ollama pull qwen2.5:1.5b
```

Check the installed model:

```powershell
ollama list
```

Make sure `qwen2.5:1.5b` appears in the list.

### 6. Translation Model Setup

The NLLB translation model is loaded through Hugging Face Transformers.

The model used in this project is:

`kinleyrabgay/nllb-200-600M-dzo-eng-300k`

The model files are downloaded automatically when the translation model is loaded for the first time. An internet connection is therefore required during the initial download.

After downloading, the model can use its locally cached files.

---

## 🚀 Running the Application

After completing the installation, make sure the virtual environment is activated and Ollama is available.

Run the following command from the main project directory:

```powershell
streamlit run app.py
```

Streamlit will display a local address in the terminal, usually:

```text
http://localhost:8501
```

Open the address in a web browser to access the DrukAI chatbot.

---

## 🤖 Models Used

### 1. Qwen2.5 1.5B

Qwen2.5 1.5B is used as the main language model in this project. It is responsible for understanding questions and generating answers in English.

DrukAI runs this model locally using Ollama.

- Model: Qwen2.5 1.5B
- Platform: Ollama
- Model link: https://ollama.com/library/qwen2.5

### 2. NLLB-200 600M Dzongkha-English

DrukAI uses a fine-tuned NLLB-200 model to translate between English and Dzongkha.

It is used for both translating user questions and converting generated English answers into Dzongkha.

- Model: NLLB-200 600M Dzongkha-English
- Platform: Hugging Face
- Model link: https://huggingface.co/kinleyrabgay/nllb-200-600M-dzo-eng-300k

**Licence note:** The model card identifies the model licence as CC BY-NC 4.0. Its attribution and non-commercial conditions should be followed when using or distributing the model.

---

## ⚠️ Current Limitations

DrukAI is an academic project and is still under development. Some limitations of the current implementation include:

- Dzongkha translation quality may vary depending on the sentence and context.
- The chatbot relies on translation to process Dzongkha questions and generate Dzongkha responses.
- Qwen2.5 is primarily used for English question answering rather than native Dzongkha generation.
- Translation errors may affect the meaning of questions and answers.
- Scanned PDFs and image-based documents are not supported by the current text extraction system.
- The current document processor supports PDF and DOCX files, not older DOC files.
- Large documents may exceed the amount of context that can be passed to the language model.
- The accuracy of generated answers is not guaranteed and important information should be verified.

These limitations provide opportunities for further improvement and development.

---

## 🔮 Future Improvements

The following features can be explored in future versions of DrukAI:

1. **Improved Dzongkha Translation:** Explore better translation models and evaluate their performance using Dzongkha examples.
2. **Dzongkha-Specific Language Model:** Investigate models trained or fine-tuned specifically for Dzongkha.
3. **Image Upload Support:** Allow users to upload images and extract text using Optical Character Recognition (OCR).
4. **Better Document Understanding:** Implement Retrieval-Augmented Generation (RAG) to improve question answering from large documents.
5. **Improved Conversation Memory:** Develop better context management for longer conversations.
6. **Voice Interaction:** Explore Dzongkha speech recognition and text-to-speech functionality.
7. **Chatbot Interface:** Continue improving the user interface and overall user experience.
8. **Performance Evaluation:** Test the chatbot with different Dzongkha questions and collect feedback from fluent Dzongkha speakers.

---

## 📚 Learning Outcomes

Developing DrukAI has helped me gain practical experience in Generative AI, Natural Language Processing, and Python application development.

Some of the key areas I explored during this project include:

- Understanding how large language models work in chatbot applications.
- Running local language models using Ollama.
- Using Hugging Face Transformers for machine translation.
- Integrating different AI models into a single application.
- Working with English and Dzongkha text processing.
- Developing chatbot interfaces using Streamlit.
- Extracting text from PDF and Word documents.
- Connecting Python applications with local AI model APIs.
- Managing Python packages and virtual environments.
- Testing and debugging an AI-based application.

This project also helped me understand the challenges of developing AI applications for languages with fewer digital resources.

---

## 🙏 Acknowledgements

I would like to acknowledge the developers and open-source communities whose tools and models made this project possible.

- [Ollama](https://ollama.com/) – For providing a platform to run language models locally.
- [Qwen](https://github.com/QwenLM/Qwen2.5) – For the Qwen2.5 language model.
- [Hugging Face](https://huggingface.co/) – For providing access to pretrained models and Transformers.
- [Meta AI NLLB](https://github.com/facebookresearch/fairseq/tree/nllb) – For the No Language Left Behind multilingual translation project.
- [Streamlit](https://streamlit.io/) – For building the chatbot web interface.
- [PyTorch](https://pytorch.org/) – For deep learning support.

---

## 📌 Project Information

| Details | Information |
|---|---|
| Project Name | DrukAI – Dzongkha AI Chatbot |
| Project Type | Academic Project |
| Programming Language | Python |
| Interface | Streamlit |
| Language Model | Qwen2.5 1.5B |
| Translation Model | NLLB-200 600M |
| Model Runtime | Ollama |
| Repository | [DrukAI on GitHub](https://github.com/Jigme2003/DrukAI-Dzongkha-AI-Chatbot) |
| Development Status | Under Development |

---

**DrukAI – Exploring Artificial Intelligence for the Dzongkha Language.**

*Developed as part of my Generative AI and Prompt Engineering project.*
