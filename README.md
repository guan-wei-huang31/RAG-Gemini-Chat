# RAG-Gemini-Chat

## Overview

RAG-Gemini-Chat is an AI-powered assistant that leverages **Retrieval-Augmented Generation (RAG)** using **Gemini AI**, **ChromaDB**, and **SQLite** to answer product-related queries. The backend is built with **Flask (Python)** for AI processing and **Express.js (Node.js)** for API routing, while the frontend is developed using **React.js**.

## 🚀Features

- **Retrieval-Augmented Generation (RAG)** for accurate AI-driven responses
- **Vector-based search with ChromaDB** for efficient query handling
- **Gemini AI embeddings** to process and retrieve relevant product information
- **SQLite database integration** for structured product details
- **React.js frontend (powered by Vite)** for a simple and user-friendly UI
- **Express.js middleware** to connect frontend and backend APIs
- **Flask API** for AI model execution and query handling

  <img src="figure/AdvanceRAG.png" alt="Advance RAG flow" width="800" height="auto"/>

## 📚Tech Stack

### **Backend**

- Python (Flask)
- Gemini AI (Embeddings + Content Generation)
- ChromaDB for vector-based search
- SQLite for structured data
- SQLAlchemy for database operations

### **Frontend**

- React.js
- Axios (API calls to backend)

### **Middleware/API Gateway**

- Node.js (Express.js)
- Axios (Proxy requests to Flask API)

## ⚙️Installation & Setup

### **1️⃣ Clone the Repository**

```
git clone https://github.com/guan-wei-huang31/RAG-Gemini-Chat.git
cd RAG-Gemini-Chat
```

### **2️⃣ Backend Setup**

```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Set up environment variables:

```
echo "GOOGLE_API_KEY=your-api-key" > .env
```


Run the Flask API:

```
python rag_api.py
```


### **3️⃣ Frontend Setup**

```
cd frontend
npm install
npm run dev
```


### **4️⃣ Middleware/API Gateway Setup**

```
cd backend
node server.js
```


## 💻Usage

1. Open the frontend at `http://127.0.0.1:5173`
2. Ask product-related questions in the input box
3. The system retrieves structured data from SQLite or performs vector search with ChromaDB
4. AI-generated responses are displayed  

<img src="figure/demo.png" alt="demo screenshot" width="800" height="auto"/>

## 📂Folder Structure

```
RAGQueryAI/
│── backend/
│   ├── flask-api
│       ├── db/              (SQLite database & ChromaDB files)
│       ├── rag_api.py       (Flask API with RAG processing)
│       ├── requirements.txt (Python dependencies)
│   ├── node-server
│       ├── server.js        (Express.js middleware)
│       ├── package.json     (Node.js dependencies)
│── frontend/
│   ├── src/             (React components)
│       ├── App.jsx      (Main React component)
│   ├── public/          (Static assets)
│   ├── indext.html      (Main entry component)
│   ├── package.json     (React dependencies)
│── .gitignore
│── README.md
```

## License

This project is licensed under the MIT License.

## Contributors

- **Guan-Wei Huang**  
For questions or suggestions, feel free to contact:  
Email: gwhuang24@gmail.com
