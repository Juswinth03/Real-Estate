from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class MongoBaseModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    model_config = ConfigDict(populate_by_name=True)

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserResponse(MongoBaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str
    id: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class PropertyCreate(BaseModel):
    title: str
    location: str
    type: str
    price: float
    bedrooms: int
    bathrooms: int
    area: float
    description: str
    image: Optional[str] = None

class PropertyResponse(MongoBaseModel, PropertyCreate):
    seller_id: str
    seller_name: str
    status: str
    badge: str
    created_at: datetime

class ProjectCreate(BaseModel):
    name: str
    location: str
    units: int
    completion: str
    description: str
    image: Optional[str] = None

class ProjectResponse(MongoBaseModel, ProjectCreate):
    builder_id: str
    builder_name: str
    created_at: datetime

class ReviewCreate(BaseModel):
    target_id: str
    target_type: str
    rating: int
    comment: str

class ReviewResponse(MongoBaseModel, ReviewCreate):
    reviewer_id: str
    reviewer_name: str
    created_at: datetime
