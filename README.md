# 🎛️ Code Complexity Dashboard

A retro‑styled web app that measures and visualizes the cyclomatic complexity of any public GitHub repo in **real time**.  
Log in with GitHub, enter a repo/username, hit **Analyze**, and watch your project’s complexity scores roll in.

## 🧰 Prerequisites

- **Python 3.10+**  
- **Node.js 18+** & **npm**  
- A GitHub OAuth App (to get `GITHUB_CLIENT_ID` & `GITHUB_CLIENT_SECRET`)  
- `pip` and `npm` installed on your PATH

## ⚡ Quick Setup
<details>
<summary>1. Clone &amp; setup</summary>

## Backend
```bash
git clone https://github.com/parniayzdin/code-dashboard.git
cd code-dashboard

python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Prepare your .env file
cp .env.example .env      # macOS / Linux
copy .env.example .env    # Windows CMD/PowerShell
```
## Frontend
```bash
cd frontend
npm install
cd ..
```
### Run the app
> Make sure you’re in the **project root** (`code-dashboard/`).

- **API (FastAPI)**  
  ```bash
  # From code-dashboard/ (not inside frontend/)
  uvicorn src.main:app --reload
  Open the interactive docs at: http://localhost:8000/docs
- **UI (React/Vite)**
    ```bash
  cd frontend
  npm run dev
  UI must be available at: http://localhost:5173
</details>

## ⚙️ Configuration
- GITHUB_CLIENT_ID=YOUR_CLIENT_ID
- GITHUB_CLIENT_SECRET=YOUR_CLIENT_SECRET

## ⚠️ Error
- ModuleNotFoundError → use uvicorn src.main:app, not main:app.
- High Absorbance / CORS → double‑check .env & allow_origins.
- Missing Files → git add . && git commit -m "Add files" && git push.

