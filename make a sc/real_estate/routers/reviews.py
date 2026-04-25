from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from database.connection import get_database
from schemas.schemas import ReviewCreate, ReviewResponse
from utils.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, db=Depends(get_database), current_user=Depends(get_current_user)):
    rev_dict = review.model_dump()
    rev_dict["reviewer_id"] = str(current_user["_id"])
    rev_dict["reviewer_name"] = current_user["name"]
    rev_dict["created_at"] = datetime.utcnow()
    
    result = await db["reviews"].insert_one(rev_dict)
    rev_dict["_id"] = str(result.inserted_id)
    return rev_dict

@router.get("/target/{target_id}", response_model=List[ReviewResponse])
async def get_reviews(target_id: str, db=Depends(get_database)):
    cursor = db["reviews"].find({"target_id": target_id})
    reviews = []
    async for rev in cursor:
        rev["_id"] = str(rev["_id"])
        reviews.append(rev)
    return reviews

@router.get("/", response_model=List[ReviewResponse])
async def get_all_reviews(db=Depends(get_database)):
    cursor = db["reviews"].find({})
    reviews = []
    async for rev in cursor:
        rev["_id"] = str(rev["_id"])
        reviews.append(rev)
    return reviews
