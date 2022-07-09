import pytest
from unittest import mock
from sqlalchemy.engine.url import URL

from aggregator.db.engine.engine_utils import isIncludable, getDotEnv, getDbConfig, getDbEngine


@pytest.mark.parametrize("line", [
    "a",
    "  a   ",
    "a=b",
    " a=b ",
    "doesn't really matter",
])
def test_isIncludable(line):
  assert isIncludable(line)


@pytest.mark.parametrize("line", [
    "# commented=out",
    "  # commented=out   ",
    "",
    "  ",
    "\n",
])
def test_not_isIncludable(line):
  assert not isIncludable(line)


@pytest.fixture
def dotEnvFile():
  return """
  # username=sandyCrocodile
  username=a11yGator
    # password=drowssap
  password=12345678
  host=db.server.lan
  port=5432

  """


@pytest.fixture
def dotEnvDict():
  return {
      "username": "a11yGator",
      "password": "12345678",
      "host": "db.server.lan",
      "port": "5432",
  }


def test_getDotEnv(dotEnvFile, dotEnvDict):
  with mock.patch("builtins.open", mock.mock_open(read_data=dotEnvFile)):
    assert getDotEnv() == dotEnvDict


def test_getDbConfig(dotEnvDict):
  assert getDbConfig(dotEnvDict) == {
      "sqlalchemy.url": "postgresql://a11yGator:12345678@db.server.lan:5432/aggregator",
      "sqlalchemy.echo": True,
  }


def test_getDbConfig_invalid():
  with pytest.raises(KeyError):
    getDbConfig({})


def test_getDbEngine(dotEnvFile):
  with mock.patch("builtins.open", mock.mock_open(read_data=dotEnvFile)):
    assert getDbEngine().url == URL.create("postgresql", "a11yGator",
                                           "12345678", "db.server.lan", "5432", "aggregator")
