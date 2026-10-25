import asyncio

from log import get_logger
from raboter import Rabota

logger = get_logger("Main")


async def main():
   
    logger.info("=" * 60)
    logger.info("ЗАПУСК ПАРСЕРА ВАКАНСИЙ RABOTA.BY")
    logger.info("=" * 60)
    
    async with Rabota(headless=False) as parser:
        
        vacancies = await parser.parse_vacancies(pages_to_parse=1)
     
        if not vacancies:
            logger.warning(" Не удалось собрать вакансии!")
            return
        
      
        logger.info("\n" + "=" * 70)
        logger.info(f"ИТОГО СОБРАНО ВАКАНСИЙ: {len(vacancies)}")
        logger.info("=" * 70)
        
        for i, vac in enumerate(vacancies[:3], 1):
            logger.info(f"\n{'─' * 70}")
            logger.info(f"ВАКАНСИЯ №{i}")
            logger.info(f"{'─' * 70}")
            logger.info(f" Название:    {vac['title']}")
            logger.info(f" Компания:    {vac['company']}")
            logger.info(f"Зарплата:    {vac['salary']}")
            logger.info(f" Город:       {vac['city']}")
            logger.info(f" Рейтинг:     {vac['rating'] if vac['rating'] else 'нет данных'}")
            
           
            skills_display = ', '.join(vac['key_skills'][:7])
            if len(vac['key_skills']) > 7:
                skills_display += f"... (всего {len(vac['key_skills'])})"
            logger.info(f" Навыки:      {skills_display if skills_display else 'не указаны'}")
            
            
            desc_preview = vac['description'][:200]
            if len(vac['description']) > 200:
                desc_preview += "..."
            logger.info(f" Описание:    {desc_preview if desc_preview else 'не указано'}")
            logger.info(f"Ссылка:      {vac['link']}")
        
        
        if len(vacancies) > 3:
            logger.info(f"\n{'─' * 70}")
            logger.info(f"ОСТАЛЬНЫЕ {len(vacancies) - 3} ВАКАНСИЙ:")
            logger.info(f"{'─' * 70}")
            for i, vac in enumerate(vacancies[3:], 4):
                logger.info(f"{i}. {vac['title']} | {vac['company']} | {vac['salary']}")
        
        logger.info("\n" + "=" * 70)
        logger.info("ПАРСИНГ УСПЕШНО ЗАВЕРШЁН")
        logger.info("=" * 70)
        
       
        return vacancies


if __name__ == "__main__":
  
    asyncio.run(main())