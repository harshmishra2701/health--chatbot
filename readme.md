# 🏥 AI Health Assistant Chatbot

An AI-powered healthcare chatbot built with **FastAPI**, **MongoDB**, and **Google Gemini API**, featuring real-time conversational health guidance and **emergency hospital locator** using Google Maps Places API.

---

## ✨ Features

- 🤖 Conversational AI powered by **Google Gemini** (`gemini-1.5-flash`)
- 💬 Persistent chat history stored in **MongoDB**
- 🚨 Automatic **emergency detection** based on symptom severity
- 🏥 **Nearby hospital finder** using Google Maps Places API (with map links)
- 📍 Browser geolocation support
- 🎨 Clean dashboard-style UI (HTML/CSS/JS, served via Jinja2 templates)
- ⚙️ Built with FastAPI + Poetry for dependency management

---

## 🗂️ Project Structure

```
health-chatbot/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Environment config / settings
│   ├── routers/
│   │   └── chat.py              # /chat endpoint
│   ├── models/
│   │   └── chat_model.py        # Pydantic request/response models
│   ├── services/
│   │   ├── gemini_service.py    # Gemini API integration
│   │   └── maps_service.py      # Google Maps Places API integration
│   ├── database/
│   │   ├── mongodb.py           # MongoDB connection
│   │   └── crud.py              # Save/fetch chat history
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       └── index.html
├── .env                          # Environment variables (not committed)
├── pyproject.toml                # Poetry dependencies
└── README.md
```

---

## ✅ Prerequisites

- **Python 3.10+**
- **Poetry** (dependency manager) → [Install Poetry](https://python-poetry.org/docs/#installation)
- **MongoDB** (local instance or [MongoDB Atlas](https://www.mongodb.com/atlas) free cluster)
- **Google Gemini API Key** → [Get it from Google AI Studio](https://aistudio.google.com/app/apikey)
- **Google Maps API Key** with **Places API** enabled → [Google Cloud Console](https://console.cloud.google.com/)

---

## ⚙️ Environment Setup

### 1. Clone the project
```bash
git clone <your-repo-url>
cd health-chatbot
```

### 2. Install dependencies with Poetry
```bash
poetry install
```

If you're adding new dependencies (Gemini + HTTP client):
```bash
poetry add google-generativeai httpx motor pydantic python-dotenv fastapi uvicorn jinja2
```

### 3. Activate the virtual environment
```bash
poetry shell
```

---

## 🔑 Configure Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=health_chatbot

# App
APP_ENV=development
MAX_HISTORY_MESSAGES=10

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Google Maps API (Places API enabled)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

---

## 🗄️ MongoDB Setup

### Option A: Local MongoDB
Install and start MongoDB locally:
```bash
# Ubuntu/WSL
sudo systemctl start mongod
```
Use this URI:
```
MONGODB_URI=mongodb://localhost:27017
```

### Option B: MongoDB Atlas (cloud, free tier)
1. Create a free cluster at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Create a database user and whitelist your IP
3. Copy the connection string into `.env`:
```
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
```

---

## 🔐 Getting API Keys

### Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key into `.env` as `GEMINI_API_KEY`

### Google Maps API Key (Places API)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable **Places API** under "APIs & Services > Library"
4. Go to "Credentials" → **Create API Key**
5. (Recommended) Restrict the key to **Places API** only
6. Copy the key into `.env` as `GOOGLE_MAPS_API_KEY`

> 💳 Google Cloud requires billing to be enabled, but Places API has a generous free monthly quota.

---

## ▶️ Running the App

```bash
poetry run uvicorn app.main:app --reload
```

The app will be available at:
```
http://127.0.0.1:8000
```

Health check endpoint:
```
http://127.0.0.1:8000/health
```

---

## 💬 How It Works

1. User describes symptoms in the chat UI.
2. Message + recent chat history is sent to **Gemini API** for a contextual response.
3. If Gemini detects emergency symptoms (chest pain, breathing issues, etc.), it tags the response with `[EMERGENCY]`.
4. On emergency detection, the app uses the browser's **geolocation** + **Google Maps Places API** to fetch and display the **nearest hospitals** with ratings and map links.
5. All conversations are stored in MongoDB per `session_id` for context-aware replies.

---

## ⚠️ Disclaimer

This chatbot provides **general health information only** and is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare provider for medical concerns. In case of a real emergency, call your local emergency number immediately.

---

## 🛠️ Tech Stack

| Component       | Technology              |
|------------------|--------------------------|
| Backend          | FastAPI                  |
| Database         | MongoDB (Motor async)    |
| AI Model         | Google Gemini (1.5 Flash)|
| Maps/Hospitals   | Google Maps Places API   |
| Frontend         | HTML, CSS, JavaScript    |
| Dependency Mgmt  | Poetry                   |

---

## 📌 Troubleshooting

- **`TemplateNotFound: index.html`** → Ensure you run `uvicorn` from the project root directory, not from inside `app/`.
- **`uvicorn: command not found`** → Check spelling (`uvicorn`, not `uvicron`) and ensure you're inside `poetry shell` or using `poetry run`.
- **Gemini errors** → Verify `GEMINI_API_KEY` is valid and not rate-limited.
- **No hospitals shown** → Ensure browser location permission is granted and `GOOGLE_MAPS_API_KEY` has Places API enabled with billing active.

---

## 📄 License

This project is for educational purposes. Customize and use as needed.
