import pkgutil
from sqlalchemy import engine_from_config
from sqlalchemy_utils import database_exists, create_database, drop_database

import aggregator.db.models
from aggregator.db.models.base import Base
# TODO (#2): fix config
from helpers.config import config


def create_db(engine):
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")


def import_models():
    loader = pkgutil.get_loader(models)
    modules = []
    for submodule in pkgutil.iter_modules(['/'.join(loader.path.split('/')[0:-1])]):
        finder, submodule_name, _ = submodule
        module = finder \
            .find_module(submodule_name) \
            .load_module(submodule_name)
        modules.append(module)
    return modules


def create_hypertables(engine, modules):
    with engine.connect() as conn:
        txn = conn.begin()
        for module in modules:
            try:
                hype = getattr(module, 'hypertable')
                conn.execute(hype)
            except:
                pass
        txn.commit()


if __name__ == "__main__":
    engine = engine_from_config(config)
    create_db(engine)
    model_list = import_models()
    Base.metadata.create_all(engine)
    create_hypertables(engine, model_list)
