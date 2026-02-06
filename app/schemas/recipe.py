from pydantic import BaseModel
from pydantic import ConfigDict
#схемы - описывают как они должны выглядеть у пользователя

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: str
    content: str
    meta_info: dict
    model_config = ConfigDict(from_attributes=True)

class RecipeCreate(RecipeBase):
    pass
class RecipeOut(RecipeBase):
    id: int
    class Config:
        from_attributes = True


class RecipeShort(RecipeBase):
    id: int

    # Поля embedding здесь НЕТ

    class Config:
        from_attributes = True