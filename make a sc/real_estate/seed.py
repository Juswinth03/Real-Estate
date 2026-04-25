import asyncio
from database.connection import get_database
from utils.hash import get_password_hash
from datetime import datetime

async def seed_db():
    db = get_database()
    
    # Check if seeded
    count = await db["users"].count_documents({})
    if count > 0:
        print("Database already seeded.")
        return

    # Seed users
    users = [
        {"name": "John Buyer", "email": "buyer@test.com", "password": get_password_hash("123456"), "role": "buyer", "is_active": True},
        {"name": "Priya Seller", "email": "seller@test.com", "password": get_password_hash("123456"), "role": "seller", "is_active": True},
        {"name": "Prestige Builder", "email": "builder@test.com", "password": get_password_hash("123456"), "role": "builder", "is_active": True},
        {"name": "Admin User", "email": "admin@test.com", "password": get_password_hash("123456"), "role": "admin", "is_active": True}
    ]
    await db["users"].insert_many(users)
    seller = await db["users"].find_one({"email": "seller@test.com"})
    builder = await db["users"].find_one({"email": "builder@test.com"})

    # Seed properties
    properties = [
        {"title":"Skyline Apartments", "location":"Chennai", "type":"apartment", "price":4500000, "bedrooms":3, "bathrooms":2, "area":1450, "status":"available", "badge":"New", "description":"Luxury apartment with sea view.", "seller_id": str(seller["_id"]), "seller_name": seller["name"], "created_at": datetime.utcnow()},
        {"title":"Green Villa Estate", "location":"Bangalore", "type":"villa", "price":12000000, "bedrooms":5, "bathrooms":4, "area":3200, "status":"available", "badge":"Hot", "description":"Spacious villa in gated community.", "seller_id": str(seller["_id"]), "seller_name": seller["name"], "created_at": datetime.utcnow()},
        {"title":"Urban Nest 2BHK", "location":"Mumbai", "type":"apartment", "price":8500000, "bedrooms":2, "bathrooms":2, "area":980, "status":"available", "badge":"Available", "description":"Modern 2BHK in city heart.", "seller_id": str(seller["_id"]), "seller_name": seller["name"], "created_at": datetime.utcnow()},
        {"title":"Sunrise Plot", "location":"Hyderabad", "type":"plot", "price":2200000, "bedrooms":0, "bathrooms":0, "area":2400, "status":"available", "badge":"New", "description":"Prime plot.", "seller_id": str(seller["_id"]), "seller_name": seller["name"], "created_at": datetime.utcnow()},
        {"title":"Palm Grove House", "location":"Pune", "type":"house", "price":6800000, "bedrooms":4, "bathrooms":3, "area":2100, "status":"available", "badge":"Hot", "description":"Independent house.", "seller_id": str(seller["_id"]), "seller_name": seller["name"], "created_at": datetime.utcnow()},
        {"title":"Elite Studio", "location":"Chennai", "type":"apartment", "price":3200000, "bedrooms":1, "bathrooms":1, "area":620, "status":"available", "badge":"Available", "description":"Compact studio.", "seller_id": str(seller["_id"]), "seller_name": seller["name"], "created_at": datetime.utcnow()}
    ]
    await db["properties"].insert_many(properties)

    # Seed projects
    projects = [
        {"name":"Horizon Heights", "builder_id": str(builder["_id"]), "builder_name": builder["name"], "location":"Chennai", "units":240, "completion":"Dec 2026", "description":"Premium residential towers.", "created_at": datetime.utcnow()},
        {"name":"Eco Gardens", "builder_id": str(builder["_id"]), "builder_name": builder["name"], "location":"Bangalore", "units":120, "completion":"Mar 2025", "description":"Sustainable living.", "created_at": datetime.utcnow()},
        {"name":"Marina Bay Towers", "builder_id": str(builder["_id"]), "builder_name": builder["name"], "location":"Mumbai", "units":450, "completion":"Jan 2027", "description":"Sea-facing apartments.", "created_at": datetime.utcnow()}
    ]
    await db["projects"].insert_many(projects)

    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_db())
