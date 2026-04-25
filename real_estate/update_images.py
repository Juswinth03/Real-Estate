import asyncio
from database.connection import get_database

async def update():
    db = get_database()
    updates = {
        "Skyline Apartments": "assets/luxury_apartment_sea_view_1777136596545.png",
        "Green Villa Estate": "assets/green_villa_estate_1777136612583.png",
        "Urban Nest 2BHK": "assets/urban_nest_2bhk_1777136628414.png",
        "Sunrise Plot": "assets/sunrise_plot_1777136649404.png",
        "Palm Grove House": "assets/palm_grove_house_1777136668756.png",
        "Elite Studio": "assets/elite_studio_1777136686838.png"
    }
    
    for title, img_path in updates.items():
        await db["properties"].update_one(
            {"title": title},
            {"$set": {"image": img_path}}
        )
    print("Database updated!")

if __name__ == "__main__":
    asyncio.run(update())
