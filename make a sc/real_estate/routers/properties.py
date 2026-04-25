from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from database.connection import get_database
from schemas.schemas import PropertyCreate, PropertyResponse
from utils.dependencies import get_current_user, RoleChecker
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=PropertyResponse)
async def create_property(property: PropertyCreate, db=Depends(get_database), current_user=Depends(RoleChecker(["seller"]))):
    prop_dict = property.model_dump()
    prop_dict["seller_id"] = str(current_user["_id"])
    prop_dict["seller_name"] = current_user["name"]
    prop_dict["status"] = "available"
    prop_dict["badge"] = "New"
    prop_dict["created_at"] = datetime.utcnow()
    
    result = await db["properties"].insert_one(prop_dict)
    prop_dict["_id"] = str(result.inserted_id)
    return prop_dict

@router.get("/", response_model=List[PropertyResponse])
async def get_properties(
    location: Optional[str] = None,
    type: Optional[str] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    db=Depends(get_database)
):
    query = {}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if type:
        query["type"] = type
    if max_price is not None:
        query["price"] = {"$lte": max_price}
    if bedrooms is not None:
        if bedrooms >= 4:
            query["bedrooms"] = {"$gte": 4}
        else:
            query["bedrooms"] = bedrooms

    cursor = db["properties"].find(query)
    properties = []
    async for prop in cursor:
        prop["_id"] = str(prop["_id"])
        properties.append(prop)
    return properties

@router.get("/{id}", response_model=PropertyResponse)
async def get_property(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    prop = await db["properties"].find_one({"_id": ObjectId(id)})
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop["_id"] = str(prop["_id"])
    return prop
