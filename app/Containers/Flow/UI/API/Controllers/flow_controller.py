from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.Containers.Flow.Actions.create_flow_action import CreateFlowAction
from app.Containers.Flow.UI.API.Requests.flow_request import CreateFlowRequest, UpdateFlowRequest
from app.Containers.Flow.UI.API.Transformers.flow_transformer import FlowTransformer

class FlowController:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()
    
    def setup_routes(self):
        self.router.add_api_route("/", self.create_flow, methods=["POST"])
        self.router.add_api_route("/", self.get_flows, methods=["GET"])
        self.router.add_api_route("/{flow_id}", self.get_flow, methods=["GET"])
        self.router.add_api_route("/{flow_id}", self.update_flow, methods=["PUT"])
        self.router.add_api_route("/{flow_id}", self.delete_flow, methods=["DELETE"])
    
    async def create_flow(self, request: CreateFlowRequest):
        # Dependency injection would be handled here
        action = CreateFlowAction(None)  # TODO: Inject dependencies
        flow = await action.run(request)
        return FlowTransformer.transform(flow)
    
    async def get_flows(self):
        # TODO: Implement get all flows
        return []
    
    async def get_flow(self, flow_id: int):
        # TODO: Implement get single flow
        return {}
    
    async def update_flow(self, flow_id: int, request: UpdateFlowRequest):
        # TODO: Implement update flow
        return {}
    
    async def delete_flow(self, flow_id: int):
        # TODO: Implement delete flow
        return {"message": "Flow deleted"}