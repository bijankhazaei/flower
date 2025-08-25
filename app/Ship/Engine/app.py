from fastapi import FastAPI
from app.Containers.Documentation.UI.API.Controllers.DocumentationController import router as docs_router
from app.Containers.User.UI.API.Controllers.UserController import router as user_router
from app.Containers.Flow.UI.API.Routes.compiler_routes import router as compiler_router
from app.Ship.Engine.database import engine
from app.Ship.Parents.model import Base
from app.Ship.Engine.seeder import run_seeders
from app.Containers.Node.Engine.NodeBootstrap import bootstrap_nodes

def create_app() -> FastAPI:
    app = FastAPI(
        title="Flower - Visual Flow Builder",
        description="A next-generation visual flow builder with Porto architecture",
        version="1.0.0"
    )
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Run seeders
    run_seeders()
    
    # Bootstrap node system
    bootstrap_nodes()
    
    # Include routes
    app.include_router(docs_router)
    app.include_router(user_router, prefix="/api")
    app.include_router(compiler_router, prefix="/api")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "flower"}
    
    return app