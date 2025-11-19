"""
Database Schemas for THE LAZY VIRTUOSO

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name.
"""
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class Artwork(BaseModel):
    title: str = Field(..., description="Artwork title")
    image_url: HttpUrl | str = Field(..., description="URL to the artwork image")
    description: Optional[str] = Field(None, description="Short description of the piece")
    poem_snippet: Optional[str] = Field(None, description="Short related poem line")
    sound_url: Optional[HttpUrl | str] = Field(None, description="Optional ambient sound for the piece")
    tags: List[str] = Field(default_factory=list, description="Keywords for filtering")

class Poem(BaseModel):
    title: str
    content: str
    author: Optional[str] = Field(None, description="Author name")
    tags: List[str] = Field(default_factory=list)

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str = Field(..., description="Art | Poetry | NFT | Clothing")
    image_url: HttpUrl | str
    in_stock: bool = True

class ContactMessage(BaseModel):
    name: str
    email: str
    inquiry_type: str = Field(..., description="Art | Collaboration | Commissions | General")
    message: str

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=1)

class Order(BaseModel):
    items: List[OrderItem]
    email: str
    total: float = Field(..., ge=0)
    status: str = Field("pending", description="pending|paid|shipped|cancelled")
