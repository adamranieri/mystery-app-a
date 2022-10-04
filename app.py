import random
import uuid
from fastapi import FastAPI
from models import Coordinate, Document, DocumentInfo, Message, Note


description = """
An application with several different implemenations. 
They all do the same things. 
But the language, framework and personal optimizations may change the performance

## Notes

Messages sent to a Notes route are kept in an array in-memory. The exact implemenation of this array can vary.

## Documents

Messages sent to a documents route are saved to local file. Each message's content is stored in it's own file. The name of a file is a UUID.

## math/factorial/coordinates

Routes that are used to more explcilty tax the server.

"""

app = FastAPI(
    title="Mystery App",
    description=description,
    version="?.?.?",

)

contents: list[str] = []


@app.get("/")
def hello() -> str:
    return "hello"

@app.post("/notes", response_model=Note)
def add_note(message: Message) -> Note:
    contents.append(message.content)
    index = len(contents) - 1
    return Note(index= index, content=message.content )

@app.post("/notes/{index}", response_model=Note)
def add_note_by_index(index: int, message: Message) -> Note:
    contents.insert(index, message.content)
    return Note(index=index, content=message.content)

@app.get("/notes", response_model=list[str])
def get_all_notes() -> list[str]:
    return contents

@app.get("/notes/{index}", response_model=Note)
def get_note_by_index(index: int) -> Note:
    return Note(index=index, content=contents[index])

@app.put("/notes/{index}", response_model=Note)
def replace_note(index:int, message: Message) -> Note:
    contents.insert(index,message.content)
    contents.pop(index +1)
    return Note(index=index, content=message.content)

@app.delete("/notes/{index}", status_code=204)
def delete_note(index: int) -> None:
    contents.pop(index)
    return None

@app.post("/documents", response_model=DocumentInfo)
def save_document(message: Message) -> DocumentInfo:
    docId = str(uuid.uuid4())
    with open(f"{docId}.txt", "w") as f:
        f.write(message.content)
    return DocumentInfo(docId = docId)

@app.get("/documents/{docId}", response_model=Document)
def get_document(docId: str) -> Document:

    with open(f"{docId}.txt", "r") as f:
        content = "".join(f.readlines())

    return Document(docId=docId,content=content)

@app.get("/math/{num1}/{num2}/{amount}", summary="A taxing mathematical operation", description="Multiples the first two numbers together in a for loop the amount of times specified by the third parameter")
def multiply(num1:float, num2:float, amount:int) -> str:

    for _ in range(amount):
        num1*num2

    return "Done"

@app.get("/coordinates/{amount}", summary="Returns a list of randomly generated geo coordiantes")
def create_random_geopoints(amount:int) -> list[Coordinate]:

    coordiantes:list[Coordinate] = []

    for _ in range(amount):
        lattitide = random.uniform(-90,90)
        longitude = random.uniform(-180,180)
        nsHemisphere = "North" if lattitide <= 0 else "South"
        ewHemisphere = "West" if longitude <= 0 else "East"
        coordiantes.append(Coordinate(lattitude=lattitide, longitude=longitude, nsHemisphere=nsHemisphere, ewHemisphere=ewHemisphere))

    return coordiantes



@app.get("/factorial/{num}", summary="Returns the factorial of the number")
def factorial(num: int, memo = {}) -> int:

    if product:= memo.get(num):
        return product
    
    product = 1

    for x in range(1,num+1):
        product*=x

    memo.update({num:product})
    
    return product
    