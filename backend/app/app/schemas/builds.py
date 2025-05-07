from typing import Optional
from typing_extensions import Self
from app.core.runners import AVAILABLE_RUNNERS
from pydantic import BaseModel, Field, model_validator


class BuildData(BaseModel):
    runner: AVAILABLE_RUNNERS = Field(default="tuxsuite", description="Runner that will run the build")
    toolchain: str = Field(description="Toolchain to be used for the build", examples=["gcc-12"])
    tree: str = Field(description="Tree to build", examples=["https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git"])
    branch: str = Field(description="Git repository branch", examples=["master"])
    kconfig: Optional[str] = Field(default=None, description="URL to a kconfig file or predefined configuration", examples=["defconfig"])
    fragments: Optional[list[str]] = Field(default=[], description="", examples=[["CONFIG_KASAN=y"]])

    @model_validator(mode="after")
    def check_config(self) -> Self:
        """
        Validator that checks that we have either a kconfig or some fragments.
        We don't allow building with no configuration.
        """
        if self.kconfig is None and len(self.fragments) == 0:
            raise ValueError("At least one configuration source muste be given!")
        return self
