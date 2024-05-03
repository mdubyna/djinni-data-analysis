import asyncio

from scraping.parse import parse_djinni
from tecnologies.filtering import get_filtered_data
from analysis.djinni_analysis import (
    get_most_common_technologies,
    get_correlation_matrix
)


async def main(path_to_raw_csv: str, path_to_filtered_csv: str) -> None:
    await parse_djinni(path_to_raw_csv)
    get_filtered_data(path_to_raw_csv, path_to_filtered_csv)
    get_correlation_matrix(path_to_filtered_csv)
    get_most_common_technologies(path_to_filtered_csv)


if __name__ == "__main__":
    asyncio.run(main("raw_data.csv", "filtered_data.csv"))
