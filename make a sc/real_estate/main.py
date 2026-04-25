from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, properties, builder, reviews, admin

app = FastAPI(title="Real Estate Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(properties.router, prefix="/api/properties", tags=["Properties"])
app.include_router(builder.router, prefix="/api/builder", tags=["Builder"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to Real Estate Portal API"}
