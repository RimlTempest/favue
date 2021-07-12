import os
import subprocess
import uuid
import warnings

import alembic
import docker as pydocker
import pytest
from alembic.config import Config
from app.db.repositories.holo_member import HoloMemberRepository
from app.models.holo_member import HoloMemberCreate, HoloMemberInDB
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient


from tests.utility import ping_postgres

config = Config("alembic.ini")


@pytest.fixture(scope="session")
def docker() -> pydocker.APIClient:
    # base url is the unix socket we use to communicate with docker
    return pydocker.APIClient(base_url="unix://var/run/docker.sock", version="auto")

# テストで使用するPostgreSQLコンテナを立ち上げるフィクスチャ
# autouse=True をデコレータで指定することでテストに対して前後処理として追加することができる
@pytest.fixture(scope="session", autouse=True)
def postgres_container(docker: pydocker.APIClient) -> None:
    """
    Use docker to spin up a postgres container for the duration of the testing session.
    Kill it as soon as all tests are run.
    DB actions persist across the entirety of the testing session.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    image = "postgres:12.1-alpine"
    docker.pull(image)

    # create the new container using
    # the same image used by our database
    command = """head -1 /proc/self/cgroup|cut -d/ -f3"""
    bin_own_container_id = subprocess.check_output(['sh', '-c', command])
    own_container_id = bin_own_container_id.decode().replace('\n', '')
    inspection = docker.inspect_container(own_container_id)

    network = list(inspection["NetworkSettings"]["Networks"].keys())[0]
    networking_config = docker.create_networking_config({
        network: docker.create_endpoint_config()
    })

    container_name = f"test-postgres-{uuid.uuid4()}"
    container = docker.create_container(
        image=image,
        name=container_name,
        detach=True,
        networking_config=networking_config
    )

    # FastAPIコンテナが稼働しているネットワーク上にDocker SDKを使用して新しいPostgreSQLコンテナを立ち上げ、上述した接続確認を行ってからDSNを CONTAINER_DSN という環境変数にセット
    docker.start(container=container["Id"])

    inspection = docker.inspect_container(container["Id"])
    ip_address = inspection['NetworkSettings']['Networks'][network]['IPAddress']
    dsn = f"postgresql://postgres:postgres@{ip_address}/postgres"

    try:
        ping_postgres(dsn)
        os.environ['CONTAINER_DSN'] = dsn
        alembic.command.upgrade(config, "head")
        yield container
    finally:
        docker.kill(container["Id"])
        docker.remove_container(container["Id"])


# それぞれFastAPIインスタンスを作成し必要に応じてデータベース接続の参照を取得する
@pytest.fixture
def app() -> FastAPI:
    from app.api.server import get_application
    return get_application()


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# 実行中のアプリケーションにリクエストを送信できる、クリーンなテストクライアントを用意するために LifespanManager と AsyncClient を使用
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client

@pytest.fixture
async def test_holo_member(db: Database) -> HoloMemberInDB:
    holo_member_repo = HoloMemberRepository(db)
    new_holo_member = HoloMemberCreate(
        name="fake holo_member name",
        description="fake description",
        age=2.2,
        type="3",
        twitter="fake"
    )
    return await holo_member_repo.create_holo_member(new_holo_member=new_holo_member)