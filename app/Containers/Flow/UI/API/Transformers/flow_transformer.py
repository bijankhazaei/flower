from typing import Dict, Any
from app.Containers.Flow.Models.flow import Flow

class FlowTransformer:
    @staticmethod
    def transform(flow: Flow) -> Dict[str, Any]:
        return {
            "id": flow.id,
            "name": flow.name,
            "description": flow.description,
            "definition": flow.definition,
            "status": flow.status.value,
            "version": flow.version,
            "created_at": flow.created_at.isoformat(),
            "updated_at": flow.updated_at.isoformat()
        }