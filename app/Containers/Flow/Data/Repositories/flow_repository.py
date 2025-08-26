from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.Containers.Flow.Models.flow import Flow

class FlowRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: Dict[str, Any]) -> Flow:
        flow = Flow(**data)
        self.session.add(flow)
        await self.session.commit()
        await self.session.refresh(flow)
        return flow
    
    async def find_by_id(self, flow_id: int) -> Optional[Flow]:
        result = await self.session.execute(select(Flow).where(Flow.id == flow_id))
        return result.scalar_one_or_none()
    
    async def find_all(self) -> List[Flow]:
        result = await self.session.execute(select(Flow))
        return result.scalars().all()
    
    async def find_by_user_id(self, user_id: int) -> List[Flow]:
        result = await self.session.execute(select(Flow).where(Flow.user_id == user_id))
        return result.scalars().all()
    
    async def update(self, flow: Flow) -> Flow:
        await self.session.commit()
        await self.session.refresh(flow)
        return flow
    
    async def delete(self, flow: Flow) -> None:
        await self.session.delete(flow)
        await self.session.commit()