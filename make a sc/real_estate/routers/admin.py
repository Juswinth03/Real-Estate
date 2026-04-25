from fastapi import APIRouter, Depends, HTTPException
from typing import List
from database.connection import get_database
from schemas.schemas import UserResponse
from utils.dependencies import RoleChecker
from bson import ObjectId

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(db=Depends(get_database), current_user=Depends(RoleChecker(["admin"]))):
    cursor = db["users"].find({})
    users = []
    async for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@router.put("/users/{user_id}/status")
async def toggle_user_status(user_id: str, is_active: bool, db=Depends(get_database), current_user=Depends(RoleChecker(["admin"]))):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": is_active}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or status already set")
    return {"message": "User status updated"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db=Depends(get_database), current_user=Depends(RoleChecker(["admin"]))):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
