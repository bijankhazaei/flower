from app.Ship.Parents.Actions.Action import Action
from app.Containers.Node.Tasks.UploadCustomNodeTask import UploadCustomNodeTask

class UploadCustomNodeAction(Action):
    def __init__(self, upload_task: UploadCustomNodeTask):
        self.upload_task = upload_task
    
    async def run(self, node_code: str, node_name: str):
        """Upload a custom node"""
        return await self.upload_task.run(node_code, node_name)