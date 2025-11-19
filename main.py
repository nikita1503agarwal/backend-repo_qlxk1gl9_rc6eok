import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Artwork, Poem, Product, ContactMessage, Order, OrderItem

app = FastAPI(title="THE LAZY VIRTUOSO API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "THE LAZY VIRTUOSO backend is alive"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "Unknown"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# Utility to serialize MongoDB documents
class MongoJSON(BaseModel):
    id: str


def serialize(doc):
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    # convert datetime to isoformat if present
    for k, v in list(d.items()):
        try:
            import datetime
            if isinstance(v, (datetime.datetime, datetime.date)):
                d[k] = v.isoformat()
        except Exception:
            pass
    return d


# Content Endpoints
@app.get("/api/artworks")
def list_artworks(limit: Optional[int] = 50, tag: Optional[str] = None):
    filt = {}
    if tag:
        filt = {"tags": {"$in": [tag]}}
    docs = get_documents("artwork", filt, limit)
    return [serialize(x) for x in docs]


@app.post("/api/artworks")
def create_artwork(payload: Artwork):
    inserted_id = create_document("artwork", payload)
    return {"id": inserted_id}


@app.get("/api/poems")
def list_poems(limit: Optional[int] = 50, tag: Optional[str] = None):
    filt = {}
    if tag:
        filt = {"tags": {"$in": [tag]}}
    docs = get_documents("poem", filt, limit)
    return [serialize(x) for x in docs]


@app.post("/api/poems")
def create_poem(payload: Poem):
    inserted_id = create_document("poem", payload)
    return {"id": inserted_id}


@app.get("/api/products")
def list_products(category: Optional[str] = None, limit: Optional[int] = 50):
    filt = {"category": category} if category else {}
    docs = get_documents("product", filt, limit)
    return [serialize(x) for x in docs]


@app.post("/api/products")
def create_product(payload: Product):
    inserted_id = create_document("product", payload)
    return {"id": inserted_id}


@app.post("/api/contact")
def submit_contact(payload: ContactMessage):
    inserted_id = create_document("contactmessage", payload)
    return {"id": inserted_id, "status": "received"}


# Orders (simple placeholder flow; payment integration to be added later)
@app.post("/api/orders")
def create_order(order: Order):
    inserted_id = create_document("order", order)
    return {"id": inserted_id, "status": "pending"}
