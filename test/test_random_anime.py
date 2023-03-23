from returns.io import IO, IOSuccess, Success, IOFailure, Failure
from unittest.mock import patch, MagicMock
from requests import Session
from requests.exceptions import HTTPError
from random_anime import random_anime


@patch.object(Session, 'get')
def test_get_page_success(mock_get):
    mock_resp = mock_get.return_value = MagicMock()
    mock_resp.content = b"<head/>"
    match random_anime.get_page():
        case IOSuccess(Success(value)): 
            assert value == "<head/>"
        case IOFailure(_):
            assert False


@patch.object(Session, 'get')
def test_get_page_failure(mock_get):
    mock_resp = mock_get.return_value = MagicMock()
    mock_resp.raise_for_status.side_effect = [HTTPError("error")]
    match random_anime.get_page():
        case IOSuccess(_): 
            assert False 
        case IOFailure(Failure(value)):
            assert isinstance(value, HTTPError)


def test_get_titles():
    with open("test/mock_page.html") as f:
        page = f.read()
    with open("test/expected_titles.txt") as f:
        expected_titles = f.read().splitlines()
    assert random_anime.get_titles(page) == expected_titles


def test_get_random_title():
    with open("test/expected_titles.txt") as f:
        titles = f.read().splitlines()
    match random_anime.get_random_title(titles):
        case IO(val):
            assert isinstance(val, str)
