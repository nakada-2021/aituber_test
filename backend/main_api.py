
from fastapi import FastAPI
from pydantic import BaseModel
from router_chain import route_query

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/chat")
def chat(query: Query):
    result = route_query(query.text)
    return {"response": result}
