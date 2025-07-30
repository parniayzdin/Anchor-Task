# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 22:00:06 2025

@author: Parnia
"""

from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///code_dashboard.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
