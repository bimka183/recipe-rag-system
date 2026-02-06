from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Text
from sqlalchemy.orm  import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
import pgvector.sqlalchemy
#модель - буквально то, как данные хранятся в базе данных

Base = declarative_base()
class Recipe(Base):
    __tablename__ = 'recipe'

    __table_args__ = {}
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False) #название блюда
    description = Column(Text, nullable=False) #опиание самого блюда
    ingredients = Column(Text, nullable=False) #ингредиенты блюда
    content = Column(Text, nullable=False) #текст файла
    meta_info = Column(JSONB) #сложность, время и МБ фотография блюда
    embedding = Column(Vector(768))
