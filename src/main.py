import os #allows us to interact with file systems
from datetime import datetime
from dotenv import load_dotenv #loads secret keys (like API keys) from a .env file

#imports related to backend
from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware #allows frontend to communicate with backend
from starlette.middleware.sessions import SessionMiddleware #manage user login

from sqlmodel import Session, SQLModel, delete, select
from pydantic import BaseModel #Helps define what data we send back to frontend
from typing import List

from starlette.config import Config
from authlib.integrations.starlette_client import OAuth #lets user login with github without creating new login system

from database import engine, init_db, get_session
from models import Analysis, Repo #my database table structures (repos and their complexity)

import git #to clone or pull repositories 
from analysis import compute_repo_complexity #custom function to calculate complexity


# Load environment
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
config = Config(".env")  #This loads the .env file

# OAuth setup (unchanged)
oauth = OAuth(config)
oauth.register(
    name="github",
    client_id=config("GITHUB_CLIENT_ID"), #gets the info
    client_secret=config("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "repo"},
)

init_db()
app = FastAPI()

app.add_middleware( #Allow frontend to call our backend
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_methods=["*"], #HTTP method                 
    allow_headers=["*"],                      
    allow_credentials=True, #allow cookies and login info
)

#delete old complexity results
@app.delete("/analyses", status_code=204) #When someone sends a DELETE request to /analyses, run this functio and after it finishes respond with status code 204, which means no content
def clear_analyses():
    with Session(engine) as session:
        session.exec(delete(Analysis)) #Delete all rows in the "Analysis" table
        session.commit() #saves the changes
    
@app.get("/login") 
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback") #redirect them to auth, this allowes us to knwo that the user logged successfully
    return await oauth.github.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback") #github calls this after user logs
async def auth_callback(request: Request):
    token = await oauth.github.authorize_access_token(request) #github gives us a token, a special key proving that the user has logged in
    user = await oauth.github.get("user", token=token) #we use the token to ask GitHub who is the suer
    username = user.json()["login"] #we grab the users info
    return RedirectResponse(f"http://localhost:5173/?user={username}") #We send them back to your React frontend and attach their name in the URL

#sends push events to webhook
@app.post("/webhook")
def github_webhook(
    x_github_event: str = Header(...), #read event, like push 
    payload: dict = None,
    session=Depends(get_session),
):
    if x_github_event != "push":
        raise HTTPException(400, "Unsupported event type")

    #get repo
    repo_info = payload["repository"]
    full_name = repo_info["full_name"]
    clone_url = repo_info["clone_url"]

    #Ensure Repo record exists
    repo = session.exec(
        select(Repo).where(Repo.full_name == full_name)
    ).first()
    if not repo:
        repo = Repo(full_name=full_name, clone_url=clone_url)
        session.add(repo)
        session.commit()

    # Clone or pull
    target_dir = os.path.join("repos", full_name.replace("/", "_"))
    if not os.path.isdir(target_dir): #if folder doesnt exist...
        git.Repo.clone_from(clone_url, target_dir) #download the repo from the beginning
    else:
        git.Repo(target_dir).remotes.origin.pull() #pull new changes if it already exists

    # Compute complexity
    avg_cc = compute_repo_complexity(target_dir) #calculate the average CC

    # Store Analysis
    analysis = Analysis(repo_id=repo.id, complexity_score=avg_cc)
    session.add(analysis)
    session.commit()

class AnalysisOut(BaseModel):
    repo_full_name: str #the full name of the Github repo
    complexity_score: float
    timestamp: datetime #the time and date this analysis was done


#sending back complexity
@app.get("/analyses", response_model=List[AnalysisOut])
def list_analyses(session=Depends(get_session)):
    rows = session.exec(
        select(Analysis, Repo).join(Repo, Analysis.repo_id == Repo.id)
    ).all()
    #frontend info
    return [
        AnalysisOut(
            repo_full_name=repo.full_name,
            complexity_score=analysis.complexity_score,
            timestamp=analysis.timestamp,
        )
        for analysis, repo in rows
    ]

#[ User clicks "Log in with GitHub" ]
        #↓
#Frontend sends them to: http://localhost:8000/login
        #↓
#Your server sends them to GitHub login
        #↓
#User logs into GitHub
        #↓
#GitHub redirects to /auth/callback
        #↓
#You get the user's name and redirect them to frontend with info
