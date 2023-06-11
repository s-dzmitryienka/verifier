from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    _exclude_fields: set = None
    _include_props: set = None

    def validated_dict(self, exclude_unset=False, extra_kwargs: Optional[dict] = None) -> dict:
        object_dict = self.dict(
            exclude_unset=exclude_unset,
            exclude=self._exclude_fields or set(),
        )
        if self._include_props:
            for prop_name in self._include_props:
                prop_value = getattr(self, prop_name, None)
                object_dict[prop_name] = prop_value

        if extra_kwargs:
            object_dict.update(extra_kwargs)
        return object_dict
