from fastapi import FastAPI

app = FastAPI(title="Hello Service", version="1.0.0")

@app.get("/hello")
async def hello():
    return "Hello World"

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "hello-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)