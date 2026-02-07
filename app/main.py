from platform import processor

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy import delete, cast
from sqlalchemy.orm import Session
from .db.models import Recipe
from .db.session import get_db, session
from .schemas.recipe import  RecipeOut, RecipeCreate, RecipeShort
from .core.embeddings import EmbeddingService
from sqlalchemy import Integer
from .db.processor import DataProcessor
app = FastAPI()
model = EmbeddingService()
@app.get("/")
async def read_root():
    return {"message": "RAG API is working"}


@app.post("/recipe/", response_model=RecipeOut)
async def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    translated_title = DataProcessor.TranslateText(recipe.title)
    translated_desc = DataProcessor.TranslateText(recipe.description)
    translated_ingr = DataProcessor.TranslateText(recipe.ingredients)
    translated_cont = DataProcessor.TranslateText(recipe.content)

    text_for_ai = (
        f"Название: {translated_title}. "
        f"Описание: {translated_desc}. "
        f"Ингредиенты: {translated_ingr}. "
        f"Инструкция: {translated_cont}"
    )

    vector = model.get_embedding(text_for_ai)
    new_recipe = Recipe(
        title=translated_title,
        description=translated_desc,
        ingredients=translated_ingr,
        content=translated_cont,
        meta_info=recipe.meta_info,
        embedding=vector
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe
@app.post("/recipe/bulk/", status_code=status.HTTP_201_CREATED)
async def create_recipe_bulk(recipes: list[RecipeCreate], db: Session = Depends(get_db)):
    new_recipes = []
    for recipe in recipes:
        text = f"{recipe.title}. Описание блюда: {recipe.description}. Ингредиенты: {recipe.ingredients}. Инструкция: {recipe.content}"
        vector = model.get_embedding(text)
        new_recipe = Recipe(title=DataProcessor.TranslateText(recipe.title),
                            description=DataProcessor.TranslateText(recipe.description),
                            ingredients=DataProcessor.TranslateText(recipe.ingredients),
                            content=DataProcessor.TranslateText(recipe.content),
                            meta_info=recipe.meta_info, embedding=vector)
        new_recipes.append(new_recipe)
    db.add_all(new_recipes)
    db.commit()

@app.get("/recipe/", response_model=list[RecipeOut])
async def read_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).limit(50).all()
@app.get("/recipe/search/", response_model=list[RecipeShort])
async def search_recipes(query: str, db: Session = Depends(get_db), max_time: int = None):
    results = db.query(Recipe)

    if max_time is not None:
        results = results.filter(
            cast(Recipe.meta_info['cooking_time'].astext, Integer) <= max_time
        )
    # Вектор запроса всё еще нужен для расчетов внутри базы
    query_vector = model.get_embedding(query)

    # База сравнивает векторы, находит топ-5, но возвращает нам объекты Recipe.
    # FastAPI видит response_model=list[RecipeShort] и удаляет embedding из ответа.
    results = results.order_by(
        Recipe.embedding.cosine_distance(query_vector)
    ).limit(25).all()

    return results
@app.delete("/recipe/all", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_all(db: Session = Depends(get_db)):
    db.query(Recipe).delete()
    db.commit()
    return None
@app.delete("/recipe/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return None

