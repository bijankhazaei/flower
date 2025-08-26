from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.Containers.Flow.Models.FlowTemplate import FlowTemplate

class FlowTemplateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: Dict[str, Any]) -> FlowTemplate:
        template = FlowTemplate(**data)
        self.session.add(template)
        await self.session.commit()
        await self.session.refresh(template)
        return template
    
    async def find_by_id(self, template_id: int) -> Optional[FlowTemplate]:
        result = await self.session.execute(select(FlowTemplate).where(FlowTemplate.id == template_id))
        return result.scalar_one_or_none()
    
    async def find_all(self) -> List[FlowTemplate]:
        result = await self.session.execute(select(FlowTemplate))
        return result.scalars().all()
    
    async def find_by_category(self, category: str) -> List[FlowTemplate]:
        result = await self.session.execute(select(FlowTemplate).where(FlowTemplate.category == category))
        return result.scalars().all()
    
    async def find_public_templates(self) -> List[FlowTemplate]:
        result = await self.session.execute(select(FlowTemplate).where(FlowTemplate.is_public == True))
        return result.scalars().all()
    
    async def find_by_user(self, user_id: int) -> List[FlowTemplate]:
        result = await self.session.execute(select(FlowTemplate).where(FlowTemplate.created_by == user_id))
        return result.scalars().all()
    
    async def update(self, template: FlowTemplate) -> FlowTemplate:
        await self.session.commit()
        await self.session.refresh(template)
        return template
    
    async def delete(self, template: FlowTemplate) -> None:
        await self.session.delete(template)
        await self.session.commit()