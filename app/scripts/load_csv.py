import pandas as pd
from langchain_community.tools.playwright.utils import run_async

from app.scripts.ingest_data import mapping_column
from app.core.embeddings import EmbeddingService
from app.db.models import Recipe
from app.db.processor import DataProcessor, run_async_translation
from app.db.session import session


def translate_dataframe(df):
    print("Начинаем перевод колонок...")
    # Переводим всё асинхронно
    df['title_ru'] = run_async_translation(df['title'].tolist())
    df['ingredients_ru'] = run_async_translation(df['ingredients'].tolist())
    df['description_ru'] = run_async_translation(df['description'].tolist())
    df['content_ru'] = run_async_translation(df['content'].tolist())

    # Собираем финальный текст для нейронки (уже на русском!)
    df['combined_text_ru'] = (
            df['title_ru'] + " " +
            df['ingredients_ru'] + " " +
            df['description_ru'] + " " +
            df['content_ru']
    )
    return df


def save_to_db(df, vectors):
    db = session()
    try:
        records = df.to_dict('records')
        recipes_to_db = []

        for row, vector in zip(records, vectors):
            # ВНИМАНИЕ: Берем уже переведенные поля!
            new_recipe = Recipe(
                title=row['title_ru'],
                description=row['description_ru'],
                ingredients=row['ingredients_ru'],
                content=row['content_ru'],
                meta_info=row['meta_info'],
                embedding=vector
            )
            recipes_to_db.append(new_recipe)

        db.add_all(recipes_to_db)
        db.commit()
        print(f"Успешно сохранено рецептов: {len(recipes_to_db)}")
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    raw_df = pd.read_csv('C:/Users/bimka/Downloads/Food_Recipe.csv')
    df = mapping_column(raw_df)

    df = translate_dataframe(df)

    service = EmbeddingService()
    vectors = service.get_embedding(df['combined_text_ru'].tolist())

    # 4. Сохранение
    save_to_db(df, vectors)