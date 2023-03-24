import argparse
import random
from bs4 import BeautifulSoup
from returns.io import IO, impure_safe
from returns.pipeline import flow
import requests
from typing import Any, List


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


def get_links(page: str) -> List[str]:
    soup = BeautifulSoup(page, "html.parser")
    ddmcc = soup.select_one('div[class="ddmcc"]')
    return [
        f"https://www.wcostream.net{tag['href'].strip()}"
        for tag in ddmcc.select('a[href]')
    ]


def get_random_item(items: List[Any]) -> IO[Any]:
    return random.choice(items)


def main():
    parser = argparse.ArgumentParser(description='Get a random anime from wcostream.')
    parser.add_argument(
        '-t',
        action='store_true',
        help='get the title instead of the link'
    )
    args = parser.parse_args()

    IO.do(
        flow(
            page,
            get_titles if args.t else get_links,
            get_random_item,
            print
        )
        for page in get_page()
    )


if __name__ == "__main__":
    main()
