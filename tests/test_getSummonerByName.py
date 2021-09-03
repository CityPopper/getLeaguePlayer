import os
from unittest import mock
from src.main import getSummonerByName
import pytest


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    envs = {"RIOT_API_KEY": "WOWSUCHAGREATAPIKEYBRO"}
    with mock.patch.dict(os.environ, envs):
        yield


def test_no_api_key():
    os.environ["RIOT_API_KEY"] = ""
    with pytest.raises(SystemExit) as exitcode:
        getSummonerByName("Beast Machine", "na1")
    assert exitcode.type == SystemExit
    assert "API Key is missing!" in exitcode.value.args


def test_empty_region():
    with pytest.raises(SystemExit) as exitcode:
        getSummonerByName("Beast Machine", "")
    assert exitcode.type == SystemExit
    assert "Invalid region: " in exitcode.value.args


def test_invalid_region():
    with pytest.raises(SystemExit) as exitcode:
        getSummonerByName("Beast Machine", "moon")
    assert exitcode.type == SystemExit
    assert "Invalid region: moon" in exitcode.value.args


def test_empty_summonerName():
    with pytest.raises(SystemExit) as exitcode:
        getSummonerByName("", "na1")
    assert exitcode.type == SystemExit
    assert "Summoner Name is empty!" in exitcode.value.args
