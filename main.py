import os
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from sqlmodel import select
from pydantic import BaseModel
from typing import List

from database import init_db, get_session
from models import Repo, Analysis
import git
from analysis import compute_repo_complexity

# Load environment
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
config = Config(".env")

# OAuth setup (unchanged)
oauth = OAuth(config)
oauth.register(
    name="github",
    client_id=config("GITHUB_CLIENT_ID"),
    client_secret=config("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "repo"},
)

# Init DB and app
init_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,                   
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user = await oauth.github.get("user", token=token)
    username = user.json()["login"]
    return RedirectResponse(f"http://localhost:5173/?user={username}")


@app.post("/webhook")
def github_webhook(
    x_github_event: str = Header(...),
    payload: dict = None,
    session=Depends(get_session),
):
    if x_github_event != "push":
        raise HTTPException(400, "Unsupported event type")

    repo_info = payload["repository"]
    full_name = repo_info["full_name"]
    clone_url = repo_info["clone_url"]

    # Ensure Repo record exists
    repo = session.exec(
        select(Repo).where(Repo.full_name == full_name)
    ).first()
    if not repo:
        repo = Repo(full_name=full_name, clone_url=clone_url)
        session.add(repo)
        session.commit()

    # Clone or pull
    target_dir = os.path.join("repos", full_name.replace("/", "_"))
    if not os.path.isdir(target_dir):
        git.Repo.clone_from(clone_url, target_dir)
    else:
        git.Repo(target_dir).remotes.origin.pull()

    # Compute complexity
    avg_cc = compute_repo_complexity(target_dir)

    # Store Analysis
    analysis = Analysis(repo_id=repo.id, complexity_score=avg_cc)
    session.add(analysis)
    session.commit()

    return {
        "status": "analyzed",
        "repo": full_name,
        "avg_complexity": avg_cc
    }


# New Pydantic model for cleaner output
class AnalysisOut(BaseModel):
    repo_full_name: str
    complexity_score: float
    timestamp: datetime


@app.get("/analyses", response_model=List[AnalysisOut])
def list_analyses(session=Depends(get_session)):
    # join Analysis -> Repo
    rows = session.exec(
        select(Analysis, Repo).join(Repo, Analysis.repo_id == Repo.id)
    ).all()
    return [
        AnalysisOut(
            repo_full_name=repo.full_name,
            complexity_score=analysis.complexity_score,
            timestamp=analysis.timestamp,
        )
        for analysis, repo in rows
    ]
