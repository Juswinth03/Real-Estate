from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from database.connection import get_database
from schemas.schemas import ProjectCreate, ProjectResponse
from utils.dependencies import get_current_user, RoleChecker
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db=Depends(get_database), current_user=Depends(RoleChecker(["builder"]))):
    proj_dict = project.model_dump()
    proj_dict["builder_id"] = str(current_user["_id"])
    proj_dict["builder_name"] = current_user["name"]
    proj_dict["created_at"] = datetime.utcnow()
    
    result = await db["projects"].insert_one(proj_dict)
    proj_dict["_id"] = str(result.inserted_id)
    return proj_dict

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(db=Depends(get_database)):
    cursor = db["projects"].find({})
    projects = []
    async for proj in cursor:
        proj["_id"] = str(proj["_id"])
        projects.append(proj)
    return projects
