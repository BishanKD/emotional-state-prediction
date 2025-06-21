# Start FastAPI backend in the background
uvicorn src.predict_api:app --host 0.0.0.0 --port 8000 &

sleep 2

# Start Streamlit frontend in the foreground
streamlit run app.py --server.port 8501
