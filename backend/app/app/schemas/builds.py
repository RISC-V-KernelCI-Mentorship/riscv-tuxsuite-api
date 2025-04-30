from typing import Optional
from typing_extensions import Self
from pydantic import BaseModel, model_validator


class BuildData(BaseModel):
    toolchain: str
    tree: str
    branch: str
    kconfig: Optional[str] = None
    fragments: Optional[list[str]] = []

    @model_validator(mode="after")
    def check_config(self) -> Self:
        if self.kconfig is None and len(self.fragments) == 0:
            raise ValueError("At least one configuration source muste be given!")
        return self
