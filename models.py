# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 21:26:29 2025

@author: Parnia
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Repo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str    
    clone_url: str         
    created_at: datetime = Field(default_factory=datetime.utcnow)
class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    repo_id: int = Field(foreign_key="repo.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    complexity_score: float  
