import asyncio

import pandas as pd

from log import get_logger
from raboter import Rabota

logger = get_logger("Main")


async def main():
    print("=" * 40)
    logger.info("loading parser for RABOTA.BY")
    print("=" * 40)
    
    async with Rabota(headless=False) as parser:
        vacancies = await parser.parse_vacancies()
        
        if not vacancies:
            logger.warning(" data could not be found!")
            return
        
        logger.info(f"Found vakancies: {len(vacancies)}")
        
        
        df = pd.DataFrame(vacancies)
        logger.info(f"Created TABLE: {df.shape[0]} rows, {df.shape[1]} cols")
        
        df = df.drop_duplicates(subset=['link'])
        logger.info(f"Deleted doubles: {len(df)} rows")

        columns_to_drop = ['link', 'description', 'salary']
        df = df.drop(columns=columns_to_drop)
        
        df.to_csv('vacancies.csv', index=False, encoding='utf-8-sig')
        logger.info("Table saved to vacancies.csv")
        

        logger.info(f"\n{df.head()}")
    
    logger.info("Program seccesefuly stoped")


if __name__ == "__main__":
    asyncio.run(main())