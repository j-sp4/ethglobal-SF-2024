from fastapi import FastAPI, Form, UploadFile, File

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}