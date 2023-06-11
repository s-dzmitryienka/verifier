from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import expression

from core.constants import StatusEnum
from core.exceptions import ObjectDoesNotExist


class CRUDMixin:
    table = None
    create_scheme = None
    update_scheme = None

    async def _execute_commit(self, query: expression, session: AsyncSession):
        await session.execute(query)
        await session.commit()

    async def create(self, input_data: create_scheme, session: AsyncSession):
        """ Create db instance """
        obj = self.table(**input_data.validated_dict())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    def get_pk_attr(self):
        """ Get PK attribute of table """
        return getattr(self.table.__table__.c, self.table.pk_name())

    @staticmethod
    def _check_object(obj: table) -> True or HTTPException:  # todo: fix to real exception!!!
        """ Check if object exist """
        if not obj:
            raise ObjectDoesNotExist()
        return True

    async def list(self, session: AsyncSession) -> table:
        """ Get list of filtered objects """
        query = select(self.table)
        objects = await session.execute(query)
        return objects.scalars().all()

    async def retrieve(self, pk: UUID, session: AsyncSession) -> table or HTTPException:  # todo: fix to real exception!!!
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
        query = update(self.table).where(self.get_pk_attr() == pk).values(**input_data.validated_dict(
            exclude_unset=partial))
        await self._execute_commit(query, session)
        return retrieved_obj

    async def delete(self, pk: int, session: AsyncSession) -> dict or HTTPException:  # todo: fix to real exception!!!
        """ Delete object by specified primary key """
        await self.retrieve(pk, session)
        query = delete(self.table).where(self.get_pk_attr() == pk)
        await self._execute_commit(query, session)
        return {'status': StatusEnum.success.value}
