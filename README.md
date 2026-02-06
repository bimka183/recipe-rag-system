# Recipe RAG Assistant

Интеллектуальный помощник по рецептам, использующий технологии **RAG** (Retrieval-Augmented Generation) для семантического поиска.


## Особенности проекта
* **Vector Search:** Поиск рецептов на основе векторных эмбеддингов (модель `multilingual-e5-base`).
* **PostgreSQL + pgvector:** Хранилище для векторных данных прямо внутри БД.
* **FastAPI:** Быстрый API (Swagger/OpenAPI).
* **Dockerized:** Полная изоляция приложения и базы данных для запуска одной командой.

## Стек технологий
* **Backend:** Python 3.11, FastAPI, SQLAlchemy
* **AI/ML:** Sentence-Transformers (Hugging Face)
* **Database:** PostgreSQL + pgvector extension
* **DevOps:** Docker, Docker Compose
