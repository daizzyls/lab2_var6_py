import asyncio

import pandas as pd

from log import get_logger
from raboter import Rabota

logger = get_logger("Main")


async def main():
    logger.info("=" * 60)
    logger.info("ЗАПУСК ПАРСЕРА ВАКАНСИЙ RABOTA.BY")
    logger.info("=" * 60)
    
    async with Rabota(headless=False) as parser:
        vacancies = await parser.parse_vacancies()
        
        if not vacancies:
            logger.warning(" Не удалось собрать вакансии!")
            return
        
        logger.info(f"Собрано вакансий: {len(vacancies)}")
        
       
        df = pd.DataFrame(vacancies)
        logger.info(f"Создана таблица: {df.shape[0]} строк, {df.shape[1]} столбцов")
        
        df = df.drop_duplicates(subset=['link'])
        logger.info(f"После удаления дубликатов: {len(df)} строк")
        
        df.to_csv('vacancies.csv', index=False, encoding='utf-8-sig')
        logger.info("✅ Таблица сохранена в vacancies.csv")
        

        logger.info(f"\n{df.head()}")
    
    logger.info("ПРОГРАММА УСПЕШНО ЗАВЕРШЕНА")


if __name__ == "__main__":
    asyncio.run(main())