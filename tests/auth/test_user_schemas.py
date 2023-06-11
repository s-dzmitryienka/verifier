from auth.schemas import UserCreateSchema, UserUpdateSchema


def test_user_create_schema():
    user = UserCreateSchema(
        email='test@test.com',
        name='TestUser',
        password='qwerty123',
    )
    assert user
    assert user.hashed_password

    # check dict on create
    dict_on_create = user.validated_dict()
    assert dict_on_create.keys() == {'email', 'name', 'hashed_password'}

    # check dict on update
    user_update = UserUpdateSchema(
        name='TestUser',
    )
    dict_on_update = user_update.validated_dict(exclude_unset=True)
    assert dict_on_update.keys() == {'name', }
