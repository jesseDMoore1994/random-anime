import random
from bs4 import BeautifulSoup
from returns.io import IO, impure_safe
from returns.pipeline import flow
import requests
from typing import List


@impure_safe
def get_page() -> str:
    session = requests.Session()
    res = session.get(
        "https://www.wcostream.net/subbed-anime-list",
        headers={
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            )
        }

    )
    res.raise_for_status()
    return res.content.decode("utf-8")


def get_titles(page: str) -> List[str]:
    soup = BeautifulSoup(page, "html.parser")
    ddmcc = soup.select_one('div[class="ddmcc"]')
    return [tag.text.strip() for tag in ddmcc.select('a[href]')]


def get_random_title(titles: List[str]) -> IO[str]:
    return random.choice(titles)


def main():
    IO.do(
        flow(
            page,
            get_titles,
            get_random_title,
            print
        )
        for page in get_page()
    )


if __name__ == "__main__":
    main()
