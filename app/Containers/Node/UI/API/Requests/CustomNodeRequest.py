from pydantic import BaseModel

class UploadCustomNodeRequest(BaseModel):
    node_name: str
    node_code: str