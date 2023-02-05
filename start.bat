@ECHO OFF
start python -m uvicorn server_python:app 

start streamlit run Dashboard.py --theme.base dark --server.headless true

explorer "http://localhost:8000/Home"