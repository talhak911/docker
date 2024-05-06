from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_students():
    return [{"name":"talha kg"}]