# Run Instructions

This repository contains a Python backend (FastAPI) and a Next.js web frontend. The frontend does not require the backend to run (it evaluates candidates locally), but the backend can be run separately for API access.

**Prerequisites**
- Python 3.10+ (recommended 3.11)
- Node.js 18+ (Node 20 recommended)
- npm or yarn
- git (optional)

**Backend (Python / FastAPI)**

1. Change to the backend directory and create a virtual environment:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
# or: pip install .
```

3. Run the development server (reload on change):

```bash
uvicorn leadership_ai.api:app --reload --port 8000
```

4. Health and example endpoints:
- Health: `GET http://localhost:8000/health`
- Sample assessment: `GET http://localhost:8000/sample`
- Synthetic workforce: `GET http://localhost:8000/synthetic-workforce?size=25&seed=7`
- Assess (POST): `POST http://localhost:8000/assess` with JSON body matching the `EmployeeProfile` shape

**Web (Next.js)**

1. Change to the web directory and install Node dependencies:

```bash
cd web
npm install
# or: yarn
```

2. Run the dev server:

```bash
npm run dev
```

The site runs at `http://localhost:3000` by default.

3. Build and start for production:

```bash
npm run build
npm run start
```

Notes:
- The frontend includes an API route at `/api/assessment` that evaluates candidates locally using the code in `src/lib/assessment.ts`.
- If you want the frontend to call the Python backend (not required by default), set an environment variable in your frontend code or proxy requests to `http://localhost:8000`.

**Running both services**
- Open two terminals: one for the backend (`cd backend` + start uvicorn) and one for the frontend (`cd web` + `npm run dev`).

**Useful commands**

```bash
# Backend
cd backend
source .venv/bin/activate
pip install -r requirements.txt
uvicorn leadership_ai.api:app --reload

# Web
cd web
npm install
npm run dev
```

**Troubleshooting**
- If port 8000 or 3000 is in use, stop the conflicting service or change the port (`--port` for uvicorn, `PORT` env var for Next).
- For Python dependency issues, ensure your virtualenv is activated and `pip` points to the venv `pip`.

If you want, I can also add a `docker-compose.yml` to run both services in containers—should I add that? 
