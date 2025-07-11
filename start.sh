#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 8001 &
sleep 2
streamlit run frontend.py --server.port 8000 --server.address 0.0.0.0
