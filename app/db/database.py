from sqlmodel import SQLModel, create_engine, Session
import streamlit as st
from urllib.parse import quote_plus

password = quote_plus(st.secrets["DB_PASSWORD"])

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{st.secrets['DB_USER']}:{password}@"
    f"{st.secrets['DB_HOST']}:"
    f"{st.secrets['DB_PORT']}/"
    f"{st.secrets['DB_NAME']}"
    "?sslmode=require"
)

engine = create_engine(
    DATABASE_URL,
    pool_size=1,
    max_overflow=2,
    pool_pre_ping=True,
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
