from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Containers.Flow.UI.API.Routes.flow_routes import router as flow_router
from app.Containers.Node.UI.API.Routes.node_routes import router as node_router
from app.Containers.Execution.UI.API.Routes.execution_routes import router as execution_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Flower - Visual Flow Builder",
        description="A scalable visual flow builder with Porto architecture",
        version="1.0.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(flow_router, prefix="/api/v1/flows", tags=["flows"])
    app.include_router(node_router, prefix="/api/v1/nodes", tags=["nodes"])
    app.include_router(execution_router, prefix="/api/v1/executions", tags=["executions"])
    
    return app