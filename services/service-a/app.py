from fastapi import FastAPI
import random
import time
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Service A running"}
@app.get("/health")
def health():
    rand = random.random()
    if rand < 0.2:
        time.sleep(2)
    if rand < 0.1:
        return {"status": "error"}
    if rand < 0.05:
        raise Exception("Service crashed!")
    return {"status": "ok"}