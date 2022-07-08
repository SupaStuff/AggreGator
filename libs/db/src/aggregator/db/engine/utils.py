import re
from operator import itemgetter

from typing import TypedDict
from sqlalchemy import engine_from_config

class DbCredentials(TypedDict):
  username: str
  password: str
  host: str
  port: str

def getDotEnv() -> dict[str, str]:
  with open('.env') as dotenv:
    lines = (line.strip() for line in dotenv if line.strip())
    pairs = (re.split('\s*=\s*', line, 1) for line in lines)
    return { k:v for k,v in pairs}

def getDbConfig(credentials: DbCredentials):
  username,password,host,port = itemgetter("username","password","host","port")(credentials)
  return {
      "sqlalchemy.url": f"postgresql://{username}:{password}@{host}:{port}/aggregator",
      "sqlalchemy.echo": True,
  }

def getDbEngine():
  dotenv = getDotEnv()
  config = getDbConfig(dotenv)
  return engine_from_config(config)
