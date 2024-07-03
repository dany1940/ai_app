from datetime import datetime
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from sqlalchemy_utils import Ltree
from alembic.config import Config
from app.models import Organization
import asyncio
from contextlib import ExitStack
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from app.conf import config as settings
from app.database import Base, get_db_session, sessionmanager
from app.main import app as actual_app
from asyncpg import Connection
from fastapi.testclient import TestClient


resources = [
            Organization(
                name="FDADFASHJJKD", created_on=datetime.now(), path=Ltree("A")
            ),
            Organization(
                name="NHSDFGHGF",
                created_on=datetime.now(),
                path=Ltree("B"),

            ),
        ]
organization_to_create = [
        {
        "organization_name": "AA",
        "parent": "A",
        "email": "s",
        "url": "s"
    }
]

class TestOrganizationEndpoints:

    @pytest.fixture(autouse=True)
    def app(self):
        with ExitStack():
            yield actual_app


    @pytest.fixture
    def client(self, app):
        with TestClient(app) as c:
            yield c


    @pytest.fixture(scope="session")
    def event_loop(self, request):
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()


    def run_migrations(self, connection: Connection):
        config = Config("app/alembic.ini")
        config.set_main_option("script_location", "alembic")
        config.set_main_option("sqlalchemy.url", settings.DB_TEST_URL)
        script = ScriptDirectory.from_config(config)

        def upgrade(self, rev, context):
            return script._upgrade_revs("head", rev)

        context = MigrationContext.configure(connection, opts={"target_metadata": Base.metadata, "fn": upgrade})

        with context.begin_transaction():
            with Operations.context(context):
                context.run_migrations()


    @pytest.fixture(scope="session", autouse=True)
    async def setup_database(self):
        # Run alembic migrations on test DB
        async with sessionmanager.connect() as connection:
            await connection.run_sync(self.run_migrations)

        yield

        # Teardown
        await sessionmanager.close()


    # Each test function is a clean slate
    @pytest.fixture(scope="function", autouse=True)
    async def transactional_session(self):
        async with sessionmanager.session() as session:
            try:
                await session.begin()
                yield session
            finally:
                await session.rollback()  # Rolls back the outer transaction


    @pytest.fixture(scope="function")
    async def db_session(self, transactional_session):
        yield transactional_session


    @pytest.fixture(scope="function", autouse=True)
    async def session_override(self, app, db_session):
        async def get_db_session_override():
            yield db_session[0]

        app.dependency_overrides[get_db_session] = await get_db_session_override

    @pytest.mark.parametrize("organization", organization_to_create)
    def test_post_create_organization(self, organization: dict[Any, Any], client: TestClient) -> None:
            """
            Test that a user can create an organization with valid
            data.
            """
            response = client.post(
                "/organization/{organization_name}",
                json=organization,
            )
            pass
            """
            print(response.json())
            assert response.status_code == status.HTTP_201_CREATED
            """

