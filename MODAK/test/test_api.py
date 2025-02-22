import json
import pathlib
from typing import AsyncIterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from MODAK import db
from MODAK.app import app, authentication_token, get_db_session
from MODAK.model import Script, ScriptIn
from MODAK.model.infrastructure import InfrastructureIn
from MODAK.model.scaling import ApplicationScalingModelIn

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


engine = create_async_engine("sqlite+aiosqlite:///", future=True)
TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def override_get_db_session() -> AsyncIterator[AsyncSession]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db_session


@app.on_event("startup")
async def startup_event():
    """Create the database structure in the empty test database"""
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_optimise(client):
    req_content = json.loads(SCRIPT_DIR.joinpath("input/mpi_test.json").read_text())
    assert "job_script" not in req_content["job"]
    assert "build_script" not in req_content["job"]
    response = client.post("/optimise", json=req_content)
    assert response.status_code == 200
    assert response.json()["job"]["job_script"]
    assert response.json()["job"]["build_script"]


def test_get_image(client):
    req_content = json.loads(SCRIPT_DIR.joinpath("input/mpi_test.json").read_text())
    assert "container_runtime" not in req_content["job"]["application"]
    response = client.post("/get_image", json=req_content)
    assert response.status_code == 200
    assert "container_runtime" in response.json()["job"]["application"]


def test_get_build(client):
    req_content = json.loads(SCRIPT_DIR.joinpath("input/mpi_test.json").read_text())
    assert "build_script" not in req_content["job"]
    response = client.post("/get_build", json=req_content)
    assert response.status_code == 200
    assert response.json()["job"]["build_script"]


def test_get_optimise(client):
    req_content = json.loads(SCRIPT_DIR.joinpath("input/mpi_test.json").read_text())
    response = client.post("/get_optimisation", json=req_content)
    assert response.status_code == 200
    assert response.json()["job"]["job_content"]


def test_create_and_get_script_roundtrip(client):
    desc = "test"
    script = ScriptIn(description=desc, conditions={}, data={"stage": "pre"})

    response = client.post(
        "/scripts",
        json=script.dict(),
        headers={"Authorization": f"Bearer {authentication_token.api_key}"},
    )
    assert response.status_code == 201

    script_list = Script.parse_obj(response.json())

    assert script_list
    assert script_list.description == desc

    response = client.get(f"/scripts/{script_list.id}")
    assert response.status_code == 200
    script = Script.parse_obj(response.json())

    assert script.id == script_list.id
    assert script.description == desc


def test_create_script_invalid_conditions(client):
    script = ScriptIn(
        conditions={"infrastructure": {"name": "missing-infra"}}, data={"stage": "pre"}
    )
    response = client.post(
        "/scripts",
        json=script.dict(),
        headers={"Authorization": f"Bearer {authentication_token.api_key}"},
    )
    assert response.status_code == 409

    infra = InfrastructureIn(name="fictitious-infra", configuration={})
    response = client.post(
        "/infrastructures",
        json=infra.dict(),
        headers={"Authorization": f"Bearer {authentication_token.api_key}"},
    )
    response.raise_for_status()

    script = ScriptIn(
        conditions={
            "infrastructure": {
                "name": "fictitious-infra",
                "storage_class": "default-foobar",
            }
        },
        data={"stage": "pre"},
    )
    response = client.post(
        "/scripts",
        json=script.dict(),
        headers={"Authorization": f"Bearer {authentication_token.api_key}"},
    )
    assert response.status_code == 409


def test_create_script_valid_storage(client):
    infra = InfrastructureIn(
        name="less-fictitious-infra",
        configuration={
            "storage": {
                "file:///scratch": {
                    "storage_class": "default-high",
                },
                "file:///data": {
                    "storage_class": "default-common",
                },
            },
        },
    )
    response = client.post(
        "/infrastructures",
        json=infra.dict(),
        headers={"Authorization": f"Bearer {authentication_token.api_key}"},
    )
    response.raise_for_status()

    script = ScriptIn(
        conditions={
            "infrastructure": {
                "name": "less-fictitious-infra",
                "storage_class": "default-common",
            }
        },
        data={"stage": "pre"},
    )
    response = client.post(
        "/scripts",
        json=script.dict(),
        headers={"Authorization": f"Bearer {authentication_token.api_key}"},
    )
    assert response.status_code == 201


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_create_scaling_model(client):
    async with engine.begin() as conn:
        await conn.execute(
            insert(db.Optimisation).values(
                opt_dsl_code="test-code-01", app_name="test-app-01"
            )
        )

    smodel = ApplicationScalingModelIn(
        opt_dsl_code="test-code-01", model={"name": "noop"}
    )
    response = client.post(
        "/scaling_models",
        json=smodel.dict(),
        headers={"Authorization": f"Bearer {authentication_token.api_key}"},
    )
    assert response.status_code == 201
