from fastapi import FastAPI
#from app.routes import chat

app = FastAPI()

#app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "API running"}


@app.post("/chat")
def chat():
    return {"answer": "Hello from your backend"}

@app.post("/health")
def process():
    return {"answer": "Backend says gets working API ok"}

@app.post("/recommendation")
def process():
    return {"answer": "Backend says respond and request"}

