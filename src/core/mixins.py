from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import expression

from core.constants import StatusEnum


class CRUDMixin:
    table = None
    create_scheme = None
    update_scheme = None

    async def _execute_commit(self, query: expression, session: AsyncSession):
        await session.execute(query)
        await session.commit()

    async def create(self, input_data: create_scheme, session: AsyncSession):
        """ Create db instance """
        obj = self.table(**input_data.dict())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    def get_pk_attr(self):
        """ Get PK attribute of table """
        return getattr(self.table.__table__.c, self.table.pk_name())

    @staticmethod
    def _check_object(obj: table) -> True or HTTPException:
        """ Check if object exist """
        if not obj:
            raise HTTPException(status_code=404, detail=f'Object not found: {obj}')
        return True

    async def list(self, session: AsyncSession) -> table:
        """ Get list of filtered objects """
        query = select(self.table)
        objects = await session.execute(query)
        return objects.scalars().all()

    async def retrieve(self, pk: int, session: AsyncSession) -> table or HTTPException:
        """ Get object by primary key """
        query = select(self.table).where(self.get_pk_attr() == pk)
        res = await session.execute(query)
        obj = res.scalars().first()
        self._check_object(obj)
        return obj

    async def update(
            self, pk: int, input_data: update_scheme, session: AsyncSession, partial: bool = False
    ) -> table or HTTPException:
        """ Update object by specified primary key """
        retrieved_obj = await self.retrieve(pk, session)
        query = update(self.table).where(self.get_pk_attr() == pk).values(**input_data.dict(exclude_unset=partial))
        await self._execute_commit(query, session)
        return retrieved_obj

    async def delete(self, pk: int, session: AsyncSession) -> dict or HTTPException:
        """ Delete object by specified primary key """
        await self.retrieve(pk, session)
        query = delete(self.table).where(self.get_pk_attr() == pk)
        await self._execute_commit(query, session)
        return {'status': StatusEnum.success.value}
