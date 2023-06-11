
class BaseCreateUpdateModelMixin:
    exclude = None

    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
            },
        )