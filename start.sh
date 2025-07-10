#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000 &
sleep 2
streamlit run frontend.py --server.port 8501 --server.address localhost
