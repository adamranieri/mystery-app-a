
from pydantic import BaseModel

class Message(BaseModel):
    content: str


class Note(BaseModel):
    index: int
    content: str 


class Document(BaseModel):
    docId: str
    content: str


class Person(BaseModel):
    fname: str 
    lname: str 
    age: int 


class Coordinate(BaseModel):
    lattitude: float 
    longitude: float
    nsHemisphere: str
    ewHemisphere: str

class DocumentInfo(BaseModel):
    docId: str