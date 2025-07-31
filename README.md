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
<summary>Clone &amp; setup</summary>

## Backend
```bash
git clone https://github.com/parniayzdin/code-dashboard.git

cd code-dashboard

# Create & activate Conda environment (Python 3.11)
conda create -n code-dashboard python=3.11 -y
conda activate code-dashboard

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Prepare your .env file
cp .env.example .env      # macOS / Linux
copy .env.example .env    # Windows CMD/PowerShell

uvicorn src.main:app --reload
```
## Frontend
```bash
cd code-dashboard
cd frontend
npm install
npm start
```
### Run the app
> **UI (React/Vite)**
  UI must be available at: http://localhost:5173
> 
> **API (FastAPI)**
  Open the interactive docs at: http://localhost:8000/docs
</details>

## ⚙️ Configuration
Your .env file must look like this:
- GITHUB_CLIENT_ID=YOUR_CLIENT_ID
- GITHUB_CLIENT_SECRET=YOUR_CLIENT_SECRET

## ⚠️ Error
- ModuleNotFoundError → use uvicorn src.main:app, not main:app.
- High Absorbance / CORS → double‑check .env & allow_origins.

## 🤝 Contributing
Contributions welcome! Feel free to:
- Open an issue
- Submit a pull request
- Propose new features
<div align="center"> Made with ❤️ by Parnia Yazdinia </div>
