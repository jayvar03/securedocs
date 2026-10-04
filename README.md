# SecureDocs

SecureDocs is a multi-tenant AI document assistant with built-in Role-Based Access Control (RBAC). 

Companies upload internal documents, and employees can ask questions and chat with them. The AI strictly answers using **only the documents the user is allowed to see**. Permissions are enforced directly inside PostgreSQL queries, ensuring sensitive documents are never leaked to unauthorized roles or other companies.

---

## Features

- 🏢 **Strict Multi-Tenancy**: Complete company isolation. Organization data is strictly separated at the database level.
- 🔐 **Role-Based Access Control (RBAC)**: Fine-grained permissions (`Admin` > `Manager` > `Employee`). Users can only query documents matching or below their access tier.
- 🛡️ **Zero-Leak Database Filtering**: Permissions are checked in PostgreSQL queries *before* results reach the LLM. If a user lacks access, zero context is sent to the AI.
- 🔍 **Hybrid Search (Dense + Sparse)**: Combines semantic vector search (`pgvector` cosine similarity) and keyword search (`tsvector`) fused using Reciprocal Rank Fusion (RRF).
- ⚡ **Blazing Fast Local Embeddings**: Powered by FastEmbed ONNX (`BAAI/bge-small-en-v1.5`), generating 384-dimensional embeddings locally with zero GPU or PyTorch overhead.
- 🤖 **High-Speed Inference**: Powered by Groq's LPU running `openai/gpt-oss-120b` for near-instant, grounded answers with interactive source citations (`[1]`, `[2]`).
- 📄 **Sentence-Aware Chunker**: Automatically slices multi-page PDFs and text files into ~800-character passages with 150-character overlap while keeping full sentences intact.
- 🧪 **Verified Security Evals**: Built-in automated penetration suite testing 78 adversarial cross-tenant and cross-role queries to verify 0% data leakage.

---

## Architecture

A simple overview of how a user's question is securely processed from start to finish:

```mermaid
flowchart LR

    User[User in Browser]
    Frontend[Frontend<br/>React + Vite + Tailwind CSS]
    Backend[Backend API<br/>FastAPI]
    Embedder[Embedder Engine<br/>FastEmbed ONNX]
    Database[(Database<br/>PostgreSQL + pgvector Neon<br/>Tenant and Role Isolation)]
    GroqLLM[LLM Inference<br/>Groq - openai/gpt-oss-120b]

    User -->|1. Types question| Frontend
    Frontend -->|2. Question + Bearer JWT| Backend
    Backend -->|3. Convert question to vector| Embedder
    Embedder -->|4. 384d embedding vector| Backend
    Backend -->|5. SQL search + Tenant + Role filters| Database
    Database -->|6. Authorized document chunks| Backend
    Backend -->|7. Context + question| GroqLLM
    GroqLLM -->|8. Answer + citations| Backend
    Backend -->|9. Verified answer + sources| Frontend
    Frontend -->|10. Display answer + citations| User
```

---

## How It Works

### 1. Hard Database-Level Filtering
Unlike basic RAG setups that fetch all documents and ask the LLM to "only use what the user is allowed to see" (which can be bypassed by prompt injection), SecureDocs applies access control directly in SQL:
```sql
WHERE tenant_id = :current_user_tenant_id 
  AND roles && :current_user_allowed_roles
```
If an employee asks about executive salaries, the query returns **0 rows**. The LLM never even sees the sensitive data.

### 2. Role Hierarchy
Permissions flow top-down:
- **Admin**: Has access to all company documents (`admin`, `manager`, `employee`).
- **Manager**: Has access to department and general documents (`manager`, `employee`).
- **Employee**: Can only access general employee documents (`employee`).

---

## Demo Accounts

All accounts use the password: **`Passw0rd!demo`**

| Company | Email | Role | Accessible Documents |
| :--- | :--- | :--- | :--- |
| **Acme Corp** | `admin@acme.example` | Admin | Handbook, Q4 Sales Plan, CEO Compensation, Board Minutes |
| **Acme Corp** | `manager@acme.example` | Manager | Handbook, Q4 Sales Plan |
| **Acme Corp** | `employee@acme.example` | Employee | Handbook only |
| **Globex Ind** | `admin@globex.example` | Admin | Handbook, Product Roadmap, Executive Compensation |
| **Globex Ind** | `manager@globex.example` | Manager | Handbook, Product Roadmap |
| **Globex Ind** | `employee@globex.example` | Employee | Handbook only |

### Try The Permission Test:
1. Log in as an **Acme Employee** (`employee@acme.example`) and ask:
   > *"What is the CEO's salary?"*
   >
   > **Result**: *"I could not find this in the documents you have access to."* (0 chunks returned by database).
2. Log in as the **Acme Admin** (`admin@acme.example`) and ask the same question:
   > *"What is the CEO's salary?"*
   >
   > **Result**: *"The CEO's base salary for the fiscal year is $1,850,000 [1]."* with citation linked to the compensation report.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons |
| **Backend** | Python 3.11+, FastAPI, Pydantic, SlowAPI |
| **Database** | PostgreSQL 16 (Neon Serverless) + `pgvector` & `tsvector` |
| **Embeddings** | FastEmbed (`BAAI/bge-small-en-v1.5`, 384-dimensional ONNX) |
| **LLM** | Groq Cloud API (`openai/gpt-oss-120b`) |
| **Auth** | JWT (HS256) with salted bcrypt password hashing |

---

## Quick Start (Run Locally)

### 1. Database
Create a free database on [Neon](https://neon.tech) and copy your connection string.

### 2. Backend
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate       # Linux/macOS: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env        # Linux/macOS: cp .env.example .env
```

Fill in your variables in `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@ep-xyz.neon.tech/neondb?sslmode=require
JWT_SECRET=your-random-secret-key
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Run migrations and seed the multi-page corporate data:
```bash
# Run schema migrations (creates tables & indexes)
python -m scripts.migrate

# Seed demo tenants, users, and multi-page documents
python -m scripts.seed --reset

# Start FastAPI server
uvicorn app.main:app --reload
```
Backend API will run at `http://localhost:8000` (Interactive docs at `/docs`).

### 3. Frontend
In a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## Testing & Evaluations

Run all verification scripts from the `backend/` directory:

```bash
# 1. Run unit tests (auth, chunker, retriever, extractors, roles)
pytest

# 2. Run security penetration test (checks 78 adversarial prompts across roles)
python -m eval.leak_test --no-llm

# 3. Run retrieval accuracy test (hit-rate & similarity threshold sweep)
python -m eval.run_eval
```

---

## Project Structure

```
securedocs/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application & middleware
│   │   ├── config.py        # Environment settings (Pydantic)
│   │   ├── db.py            # Psycopg connection pool
│   │   ├── deps.py          # Auth middleware & user caching
│   │   ├── roles.py         # Role hierarchy definitions
│   │   ├── schema.sql       # PostgreSQL DDL, HNSW & FTS indexes
│   │   ├── routers/         # auth, chat, documents, health
│   │   └── services/        # chunker, embedder, extract, ingest, llm, retriever
│   ├── scripts/             # migrate, seed, download_model
│   ├── tests/               # Pytest unit tests
│   └── eval/                # Security penetration & retrieval evals
├── frontend/
│   ├── src/
│   │   ├── pages/           # Login, Chat, and Documents
│   │   ├── components/      # Nav bar & Layout wrappers
│   │   ├── api.js           # API client
│   │   └── auth.jsx         # Auth context & state
│   └── package.json
├── render.yaml              # Cloud deployment blueprint
└── README.md                # Project documentation
```

---

## Production Deployment

- **Database**: PostgreSQL with `pgvector` hosted on [Neon](https://neon.tech).
- **Backend**: Hosted on [Render](https://render.com) using the included `render.yaml`.
- **Frontend**: Hosted on [Vercel](https://vercel.com) or [Netlify](https://netlify.com) (`npm run build`, publish directory: `dist`).
