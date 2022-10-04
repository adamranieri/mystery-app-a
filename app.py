import random
import uuid
from fastapi import FastAPI
from models import Coordinate, Document, Message, SavedMessage

app = FastAPI()

contents: list[str] = []


@app.get("/")
def hello() -> str:
    return "hello"

@app.post("/messages")
def add_message(message: Message) -> SavedMessage:
    contents.append(message.content)
    index = len(contents) - 1
    return SavedMessage(index= index, content=message.content )

@app.post("/messages/{index}")
def add_message_by_index(index: int, message: Message) -> SavedMessage:
    contents.insert(index, message.content)
    return SavedMessage(index=index, content=message.content)

@app.get("/messages")
def get_all_messages() -> list[str]:
    return contents

@app.get("/messages/{index}")
def get_message_by_index(index: int) -> str:
    return contents[index]

@app.put("/messages/{index}")
def replace_message(index:int, message: Message) -> SavedMessage:
    contents.insert(index,message.content)
    contents.pop(index +1)
    return SavedMessage(index=index, content=message.content)

@app.delete("/messages/{index}")
def delete_message(index: int) -> str:
    contents.pop(index)
    return "Message set to null"

@app.post("/documents")
def save_document(message: Message) -> str:
    docId = str(uuid.uuid4())
    with open(f"{docId}.txt", "w") as f:
        f.write(message.content)
    return docId

@app.get("/documents/{docId}")
def get_document(docId: str) -> Document:

    with open(f"{docId}.txt", "r") as f:
        content = "".join(f.readlines())

    return Document(docId=docId,content=content)

@app.get("/math/{num1}/{num2}/{amount}")
def multiply(num1:float, num2:float, amount:int) -> str:

    for _ in range(amount):
        num1*num2

    return "Done"

@app.get("/random/coordinates/{amount}")
def create_random_geopoints(amount:int) -> list[Coordinate]:

    coordiantes:list[Coordinate] = []

    for _ in range(amount):
        lattitide = random.uniform(-90,90)
        longitude = random.uniform(-180,180)
        nsHemisphere = "North" if lattitide <= 0 else "South"
        ewHemisphere = "West" if longitude <= 0 else "East"
        coordiantes.append(Coordinate(lattitude=lattitide, longitude=longitude, nsHemisphere=nsHemisphere, ewHemisphere=ewHemisphere))

    return coordiantes

factorial_memo = {}

@app.get("/factorial/{num}")
def factorial(num: int) -> int:

    if product:= factorial_memo.get(num):
        return product
    
    product = 1

    for x in range(1,num+1):
        product*=x

    factorial_memo.update({num:product})
    
    return product
    