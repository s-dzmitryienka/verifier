from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
            },
        )


class UserCreateSchema(CreateUpdateDictModel):
    email: EmailStr
    name: str

    class Config:
        orm_mode = True


class UserSchema(UserCreateSchema):
    id: UUID
    is_active: bool
