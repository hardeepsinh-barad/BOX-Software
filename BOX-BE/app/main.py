from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.routers import organization, users, reason, device_reason_log, device_log, auth, mqtt_sender, device
from app.database import engine, get_db
from app import models, crud, schemas

app = FastAPI(title="My Web App")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(organization.router)
app.include_router(users.router)
app.include_router(reason.router)
app.include_router(device_reason_log.router)
app.include_router(device_log.router)
app.include_router(auth.router)
app.include_router(mqtt_sender.router, prefix="/api")
app.include_router(device.router)

# Create tables on startup (for development; use migrations in production)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    print("Tables created!")

    # Create super admin organization and user
    async for db in get_db():
        try:
            super_admin_org = await crud.get_organization_by_name(db, "Cracky")
            if not super_admin_org:
                super_admin_org = await crud.create_organization(db, schemas.OrganizationCreate(name="Cracky", email="admin@cracky.com"))
            
            super_admin = await crud.get_user_by_email(db, "admin@cracky.com")
            if not super_admin:
                await crud.create_user(db, schemas.UserCreate(
                    org_id=super_admin_org.id,
                    name="Super Admin",
                    contact_number="9874563210",
                    email="admin@cracky.com",
                    password="Admin@123",
                    role_id=1  
                ))
        finally:
            await db.close()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My Machine Tracker App",
        version="1.0.0",
        description="APIs for machine tracker",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    return {"message": "Welcome to the web app!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="192.168.1.5", port=8080, reload=True)
