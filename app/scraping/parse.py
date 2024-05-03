import csv
import logging
import sys
from dataclasses import dataclass
import asyncio

import httpx
from bs4 import BeautifulSoup, Tag


@dataclass
class Vacancy:
    name: str
    description: str
    experience: int
    views: int
    applications: int


BASE_URL = "https://djinni.co/"
JOBS_URL = BASE_URL + "jobs/"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


async def parse_single_vacancy(vacancy_soup: Tag) -> Vacancy:
    name = vacancy_soup.select_one(
        "header > div.job-list-item__title"
        "> div > a.job-list-item__link"
    ).text.strip()
    description = vacancy_soup.select_one(
        ".job-list-item__description > span"
    )["data-original-text"]
    job_info = [
        info.text
        for info in vacancy_soup.select(
            "header > div.job-list-item__job-info > span"
        )
        if "experience" in info.text
    ]
    if "No experience" in job_info[0]:
        experience = 0
    else:
        experience = int(job_info[0].strip().split()[1])
    views = int(vacancy_soup.select("div.job-list-item__counts > span"
                                    " > span.nobr > span.mr-2")[0]["title"].split()[0])
    applications = int(vacancy_soup.select("div.job-list-item__counts > span"
                                           " > span.nobr > span.mr-2")[1]["title"].split()[0])
    return Vacancy(
        name=name,
        description=description,
        experience=experience,
        views=views,
        applications=applications
    )


async def get_python_djinni_vacancies(page: int, client: httpx.AsyncClient, url: str = JOBS_URL) -> list[Vacancy]:
    response = await client.get(url, params={
        "primary_keyword": "Python",
        "page": page
    })
    soup = BeautifulSoup(response.content, "html.parser")
    vacancies = soup.select("main > ul.list-jobs > li")

    return [await parse_single_vacancy(vacancy_soup) for vacancy_soup in vacancies]


async def get_num_pages(client: httpx.AsyncClient, url: str = JOBS_URL) -> int:
    response = await client.get(url, params={
        "primary_keyword": "Python",
    })
    soup = BeautifulSoup(response.content, "html.parser")
    return int(
        soup.select(
            "div.page-content > div.container"
            " > div.row > div"
            " > main > ul.pagination"
            " > li"
        )[-2].text.strip()
    )


async def get_vacancies_data() -> list[Vacancy]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }
    async with httpx.AsyncClient(headers=headers) as client:
        pages = await get_num_pages(client, JOBS_URL)
        tasks = []
        for page in range(1, pages + 1):
            logging.info(f"Start parsing page {page}")
            tasks.append(get_python_djinni_vacancies(page, client, JOBS_URL))

        results = await asyncio.gather(*tasks)
    all_vacancies = []
    for page_vacancies in results:
        all_vacancies.extend(page_vacancies)
    return all_vacancies


async def parse_djinni(output_csv_path: str) -> None:
    vacancies = await get_vacancies_data()

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(vacancies[0].__annotations__.keys())
        for instance in vacancies:
            writer.writerow(instance.__dict__.values())


if __name__ == "__main__":
    asyncio.run(parse_djinni("../vacancies.csv"))
