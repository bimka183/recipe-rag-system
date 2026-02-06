import asyncio
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

class DataProcessor:
    @staticmethod
    def TranslateText(text: str):
        if not text or not isinstance(text, str):
            return ""
        translator = GoogleTranslator(source='auto', target='ru')
        return translator.translate(text)

    @classmethod
    async def translate_batch(cls, texts):
        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            tasks = []

            for text in texts:
                task = loop.run_in_executor(executor, cls.TranslateText, text)
                tasks.append(task)
                await asyncio.sleep(0.1)

                # Собираем результаты всех запущенных задач
            return await asyncio.gather(*tasks)

# Функция-запускатор, которую ты спрашивал
def run_async_translation(texts):
    return asyncio.run(DataProcessor.translate_batch(texts))