import asyncio
import random

from patchright.async_api import async_playwright

from log import get_logger
from rab_link import linkin_park as site_l

logger = get_logger(__name__)


class Rabota:
    def __init__(self , headless = True , link : str = site_l):
        self.link = link
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self.cookies_accepted = False

#================================FUNCSforWITH======
    async def __aenter__(self):
        await self.browser_launch()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser_stop()

# ===============================START&STOP=====
    async def browser_launch(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless
            )
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        logger.info("Browser is LAUNCHED...")
    
    async def browser_stop(self):
        if self.browser:
            await self.browser.close()
            logger.info("Browser is CLOSED")

        if self.playwright:
            await self.playwright.stop()
            logger.info("Playwright is STOPED")

#================================================================COOKIES=====
    async def close_cookie_banner(self):
        try:
            if self.page:
                cookie_button = await self.page.query_selector('.magritte-button__label___zplmt_7-3-9_xhh')
            
            if cookie_button and self.page:
                logger.info("banner of cockie is detected, closing...")
                await cookie_button.click()
                await self.page.wait_for_timeout(random.randint(1000 , 2000))  
                logger.info("cockie banner is closed")
            else:
                logger.info("coockie banner is undetected")
                
        except Exception as e:
            
            logger.warning(f"coockiebanner could not be closed.: {e}")
    
    async def close_chat_widget(self):
        try:
            if self.page:
                close_button = await self.page.query_selector('.uxs-p1vJ1sVpZM.uxs-1sl65nu')
            
            if close_button and self.page:
                logger.info("Найден виджет помощника, закрываю...")
                await close_button.click()
                await self.page.wait_for_timeout(random.randint(1000 , 2000))
                logger.info("Виджет помощника закрыт")
            else:
                logger.info("Виджет помощника не найден, продолжаю работу")
                
        except Exception as e:
            logger.warning(f"Не удалось закрыть виджет помощника: {e}")

#================================================UNIVERSAL_CLICK=====
    async def click_if_exists(self, selector: str, name: str) -> bool:
        
        try:
            if self.page:
                element = await self.page.query_selector(selector)
            
            if element and self.page:
                logger.info(f"{name}: обнаружен, нажимаю...")
                await element.click()
                await self.page.wait_for_timeout(random.randint(800, 1500))
                logger.info(f"{name}: нажат")
                return True
            
            logger.info(f"{name}: отсутствует на странице")
            return False
            
        except Exception as e:
            logger.warning(f"{name}: не удалось нажать. Причина: {e}")
            return False

    async def click_all_if_exists(self, selector: str, name: str, max_clicks: int = 5) -> int:

        clicked = 0
        
        for _ in range(max_clicks):
            try:
                if self.page:
                    element = await self.page.query_selector(selector)
                
                    if not element:
                        break 
                    
                    await element.click()
                    clicked += 1
                    logger.info(f"{name}: выполнен клик №{clicked}")
                    await self.page.wait_for_timeout(random.randint(500, 1000))
                
            except Exception as e:
                logger.warning(f"{name}: клик не удался. Причина: {e}")
                break
        
        if clicked == 0:
            logger.info(f"{name}: не найдено на странице")
        else:
            logger.info(f"{name}: всего закрыто плашек: {clicked}")
        
        return clicked  
    
    async def close_popups(self):
        
        await self.click_if_exists(
            '[data-qa="region-clarification-submit-button"]',
            "Плашка региона (Да, верно)"
        )
        

        if not self.cookies_accepted and self.page:
            url_before = self.page.url
            clicked = await self.click_if_exists(
                '.magritte-button__label___zplmt_7-3-9_xhh',
                "Баннер куки"
            )
            if clicked:
                
                if self.page.url != url_before:
                    logger.warning("Клик увёл со страницы - возвращаюсь назад!")
                    await self.page.go_back()
                    await self.page.wait_for_timeout(1000)
              
                await self.page.keyboard.press("Escape")
                self.cookies_accepted = True
        

        await self.click_all_if_exists(
            'button.uxs-p1vJ1sVpZM.uxs-1sl65nu',
            "Крестик uxs-плашки"
        )
#===   
           
#=====================================================MAIN_FUNCTIONAL====
    async def get_max_pages(self):
        logger.info('search max count of pages...')

        try:
            if self.page:
                page = 1
                first_url = f"{self.link}{page}"
                await self.page.goto(first_url , wait_until='domcontentloaded')
                await self.page.wait_for_timeout(random.randint(1000 , 2000))

                await self.close_popups()

                page_buttons = await self.page.query_selector_all('[data-qa="pager-page"]')

                if not page_buttons:
                    logger.info("page buttons is not detected")
                    return 1

                logger.info(f"detected {len(page_buttons)} buttons")

                max_pages = 1
                for button in page_buttons:
                    try:
                        text = await button.inner_text()
                        text = text.strip()

                        if text.isdigit():
                            num = int(text)
                            if num > max_pages:
                                max_pages = num
                                logger.info(f"Page number {num} is detected")

                    except Exception as e:
                        logger.info(f'page number could not be read. cause{e}')
                        continue

                logger.info(f"found max page by number{max_pages}")
                return max_pages

        except Exception as e:
            logger.info(f"could not found max number of pages {e}")
            return 1
                        
    async def go_to_page(self):
        logger.info('try to open link')
        if self.page:
            logger.info(f'navigation to {self.link}')
            await self.page.goto(self.link , wait_until="domcontentloaded")
            await self.page.wait_for_timeout(random.randint(1000 , 2000))
            await self.close_popups()
            logger.info("page is loaded")

    async def parse_vacancy_details(self, vacancy_url: str) -> dict:
        details = {
            'description': '',
            'key_skills': [],
            'rating': None
        }
        
        try:
            logger.info(f"Переход на страницу вакансии: {vacancy_url}")
            
            if self.page:
                await self.page.goto(vacancy_url, wait_until="domcontentloaded")
                await self.page.wait_for_timeout(random.randint(2000, 3000))
            
            if self.page:
                description_el = await self.page.query_selector('[data-qa="vacancy-description"]')
            
            if not description_el and self.page:
                description_el = await self.page.query_selector('.vacancy-description')
            
            if description_el:
                description = await description_el.inner_text()
                details['description'] = description.strip()
                logger.info(f"📝 Описание получено ({len(details['description'])} символов)")
            else:
                logger.warning("Описание не найдено")

            if self.page:
                skills_container = await self.page.query_selector('[class*="vacancy-skill-list"]')
            
            if skills_container:
                
                skill_elements = await skills_container.query_selector_all('li, [data-qa="skills-element"]')
                
                skills = []
                for skill_el in skill_elements:
                    skill_text = await skill_el.inner_text()
                    skill_text = skill_text.strip()
                    if skill_text:
                        skills.append(skill_text)
                
                details['key_skills'] = skills
                logger.info(f"Навыки найдены: {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''}")
            else:
                if self.page:
                    skill_elements = await self.page.query_selector_all('[data-qa="skills-element"]')
                    if skill_elements:
                        skills = []
                        for skill_el in skill_elements:
                            skill_text = await skill_el.inner_text()
                            skills.append(skill_text.strip())
                        details['key_skills'] = skills
                        logger.info(f"Навыки найдены (фоллбэк): {', '.join(skills[:5])}")
                    else:
                        logger.warning("Навыки не найдены")
            
            if self.page:
                rating_el = await self.page.query_selector('[data-qa="employer-review-small-widget-total-rating"]')
            
            if rating_el:
                rating_text = await rating_el.inner_text()
                rating_text = rating_text.strip()
                
                try:
                    rating_text = rating_text.replace(',', '.')
                    rating_value = float(rating_text)
                    details['rating'] = rating_value
                    logger.info(f"Рейтинг компании: {rating_value}")
                except ValueError:
                    logger.warning(f"Не удалось преобразовать рейтинг: '{rating_text}'")
            else:
                logger.info("Рейтинг компании не указан (нет отзывов)")
            
            return details
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге деталей вакансии: {e}")
            return details

    async def extract_basic_info(self, card):
        try:
            
            title_el = await card.query_selector('a[data-qa="vacancy-serp__vacancy-title"]')
            if not title_el:
                title_el = await card.query_selector('a[href*="/vacancy/"]')
            
            if not title_el:
                return None
            
            title = await title_el.inner_text()
            link = await title_el.get_attribute('href') or ""
            
            if link and not link.startswith('http'):
                link = f"https://rabota.by{link}"

          
            company_el = await card.query_selector('[data-qa="vacancy-serp__vacancy-employer"]')
            company = await company_el.inner_text() if company_el else "Не указана"

           
            salary_el = await card.query_selector('[data-qa="vacancy-serp__vacancy-compensation"]')
            salary = await salary_el.inner_text() if salary_el else "Не указана"

          
            city_el = await card.query_selector('[data-qa="vacancy-serp__vacancy-address"]')
            city = await city_el.inner_text() if city_el else "Не указан"

            return {
                'title': title.strip(),
                'company': company.strip(),
                'salary': salary.strip(),
                'city': city.strip(),
                'link': link
            }
            
        except Exception as e:
            logger.error(f"Ошибка извлечения базовой информации: {e}")
            return None

    async def parse_vacancies(self, pages_to_parse: int = 3):
    
        all_vacancies = []

        total_pages = await self.get_max_pages()
        
        logger.info(f"count pages to parse: {pages_to_parse} from {total_pages}")


        logger.info("=" * 60)
        logger.info("ЭТАП 1: Сбор карточек со страниц поиска")
        logger.info("=" * 60)
        
        all_cards_info = []  
        
        for page_num in range(1, pages_to_parse + 1):
            page_url = f"{self.link}&page={page_num}"
            logger.info(f"go to page number {page_num}")
            if self.page:
                await self.page.goto(page_url, wait_until="domcontentloaded")
                await self.page.wait_for_timeout(random.randint(1500, 2500))
                await self.close_popups()

            if self.page:
                cards = await self.page.query_selector_all('[data-qa="vacancy-serp__vacancy"]')
                if not cards:
                    cards = await self.page.query_selector_all('a[href*="/vacancy/"]')

            logger.info(f"cards found: {len(cards)}")

            for card_index, card in enumerate(cards, 1):
                try:
                    vacancy_data = await self.extract_basic_info(card)
                    
                    if not vacancy_data or not vacancy_data.get('link'):
                        logger.warning(f"Не удалось извлечь данные из карточки {card_index}")
                        continue
                    
                    
                    vacancy_data['page_num'] = page_num
                    all_cards_info.append(vacancy_data)
                    
                except Exception as e:
                    logger.error(f"Ошибка извлечения карточки {card_index}: {e}")
                    continue
            
            
            if page_num < pages_to_parse and self.page:
                delay = random.randint(2000, 4000)
                logger.info(f"Пауза {delay} мс перед следующей страницей...")
                await self.page.wait_for_timeout(delay)

        logger.info(f"\nЭТАП 1 завершён. Собрано карточек: {len(all_cards_info)}")

        
        logger.info("\n" + "=" * 60)
        logger.info("ЭТАП 2: Сбор деталей по каждой вакансии")
        logger.info("=" * 60)

        for vacancy_index, vacancy_data in enumerate(all_cards_info, 1):
            try:
                logger.info(f"\n Вакансия {vacancy_index}/{len(all_cards_info)}: {vacancy_data['title']}")
                
                vacancy_details = await self.parse_vacancy_details(vacancy_data['link'])
                
                vacancy_data.update(vacancy_details)
                
                vacancy_data.pop('page_num', None)
                
                all_vacancies.append(vacancy_data)
                logger.info(f"Вакансия собрана")
                
                #
                if vacancy_index < len(all_cards_info) and self.page:
                    delay = random.randint(1500, 3000)
                    logger.info(f"Пауза {delay} мс...")
                    await self.page.wait_for_timeout(delay)
                    
            except Exception as e:
                logger.error(f"Ошибка при обработке вакансии {vacancy_index}: {e}")
                continue

        logger.info(f"\n{'='*60}")
        logger.info(f"Парсинг завершён. Всего собрано: {len(all_vacancies)} вакансий")
        logger.info(f"{'='*60}\n")
        return all_vacancies
        

        

        
