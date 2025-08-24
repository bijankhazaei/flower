from fastapi import FastAPI
from app.Containers.Documentation.UI.API.Controllers.DocumentationController import router as docs_router
from app.Containers.User.UI.API.Controllers.UserController import router as user_router
from app.Ship.Engine.database import engine
from app.Ship.Parents.model import Base

def create_app() -> FastAPI:
    app = FastAPI(
        title="Flower - Visual Flow Builder",
        description="A next-generation visual flow builder with Porto architecture",
        version="1.0.0"
    )
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Include routes
    app.include_router(docs_router)
    app.include_router(user_router, prefix="/api")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "flower"}
    
    return app