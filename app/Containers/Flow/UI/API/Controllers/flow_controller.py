from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.Containers.Flow.Actions.create_flow_action import CreateFlowAction
from app.Containers.Flow.Actions.GetFlowAction import GetFlowAction
from app.Containers.Flow.Actions.GetFlowsAction import GetFlowsAction
from app.Containers.Flow.Actions.UpdateFlowAction import UpdateFlowAction
from app.Containers.Flow.Actions.DeleteFlowAction import DeleteFlowAction
from app.Containers.Flow.UI.API.Requests.flow_request import CreateFlowRequest, UpdateFlowRequest
from app.Containers.Flow.UI.API.Transformers.flow_transformer import FlowTransformer

class FlowController:
    def __init__(self):
        self.router = APIRouter(prefix="/flows", tags=["Flow Management"])
        self.setup_routes()
    
    def setup_routes(self):
        self.router.add_api_route("/", self.create_flow, methods=["POST"])
        self.router.add_api_route("/", self.get_flows, methods=["GET"])
        self.router.add_api_route("/{flow_id}", self.get_flow, methods=["GET"])
        self.router.add_api_route("/{flow_id}", self.update_flow, methods=["PUT"])
        self.router.add_api_route("/{flow_id}", self.delete_flow, methods=["DELETE"])
    
    async def create_flow(self, request: CreateFlowRequest):
        # TODO: Implement proper dependency injection
        action = CreateFlowAction(None)
        flow = await action.run(request)
        return FlowTransformer.transform(flow)
    
    async def get_flows(self, user_id: Optional[int] = Query(None)):
        # TODO: Implement proper dependency injection
        action = GetFlowsAction(None)
        flows = await action.run(user_id)
        return [FlowTransformer.transform(flow) for flow in flows]
    
    async def get_flow(self, flow_id: int):
        # TODO: Implement proper dependency injection
        action = GetFlowAction(None)
        flow = await action.run(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail="Flow not found")
        return FlowTransformer.transform(flow)
    
    async def update_flow(self, flow_id: int, request: UpdateFlowRequest):
        # TODO: Implement proper dependency injection
        action = UpdateFlowAction(None)
        flow = await action.run(flow_id, request.dict(exclude_unset=True))
        if not flow:
            raise HTTPException(status_code=404, detail="Flow not found")
        return FlowTransformer.transform(flow)
    
    async def delete_flow(self, flow_id: int):
        # TODO: Implement proper dependency injection
        action = DeleteFlowAction(None)
        success = await action.run(flow_id)
        if not success:
            raise HTTPException(status_code=404, detail="Flow not found")
        return {"message": "Flow deleted successfully"}