import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from typing import List

from app.models.holo_member import (
    HoloMemberCreate, 
    HoloMemberInDB
)

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND, 
    HTTP_422_UNPROCESSABLE_ENTITY,
)

# これを定義することによって@pytest.mark.asyncioとデコレータを定義しなくてよくなる
pytestmark = pytest.mark.asyncio

@pytest.fixture
def new_holo_member():
    return HoloMemberCreate(
        type="3",
        name="テスト潤羽るしあ",
        description="るしあはいいぞ",
        age=1600.0,
        twitter="https://twitter.com/uruharushia",
    )

# Routing Test
class TestHoloMemberRoutes:
    # デコレータを付与することで非同期にテストを処理
    # app と clientはconftest.pyファイルで定義したフィクスチャ
    async def test_routes_exist(
        self,
        app: FastAPI,
        client: AsyncClient
    ) -> None:
        # URL反転を備えているためフルパスを書かずにルートを指定することができる
        res = await client.post(
            app.url_path_for(
                "holo_member:create-holo_member"
            ), json={}
        )
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient
    ) -> None:
        res = await client.post(
            app.url_path_for(
                "holo_member:create-holo_member"
            ), json={}
        )
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

# Create Test
class TestCreateHoloMember:
    async def test_valid_input_creates_holo_member(
        self, 
        app: FastAPI,
        client: AsyncClient,
        new_holo_member: HoloMemberCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("holo_member:create-holo_member"),
            json={"new_holo_member": new_holo_member.dict()}
        )
        assert res.status_code == HTTP_201_CREATED
        created_holo_member = HoloMemberCreate(**res.json())
        assert created_holo_member == new_holo_member
    
    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"name": "test_name"}, 422),
            ({"age": 2}, 422),
            ({"name": "test_name", "description": "test"}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        invalid_payload: dict,
        status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("holo_member:create-holo_member"),
            json={"new_holo_member": invalid_payload}
        )
        assert res.status_code == status_code

# Get Test
class TestGetHoloMember:
    async def test_get_holo_member_by_id(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_holo_member: HoloMemberInDB
    ) -> None:
        res = await client.get(app.url_path_for(
            "holo_member:get-holo_member-by-id",
            id=test_holo_member.id
        ))
        assert res.status_code == HTTP_200_OK
        holo_member = HoloMemberInDB(**res.json())
        assert holo_member == test_holo_member
    
    @pytest.mark.parametrize(
        "id, status_code",
        (
            (500, 404),
            (-1, 404),
            (None, 422),
        ),
    )
    async def test_wrong_id_returns_error(
        self, 
        app: FastAPI, 
        client: AsyncClient, 
        id: int, 
        status_code: int
    ) -> None:
        res = await client.get(
            app.url_path_for(
                "holo_member:get-holo_member-by-id", 
                id=id
            )
        )
        assert res.status_code == status_code

    async def test_get_all_holo_member_returns_valid_response(
        self, 
        app: FastAPI, 
        client: AsyncClient, 
        test_holo_member: HoloMemberInDB
    ) -> None:
        res = await client.get(
            app.url_path_for(
                'holo_member:get-all-holo_member'
            )
        )
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        holo_member = [HoloMemberInDB(**item) for item in res.json()]
        assert test_holo_member in holo_member

# FIXME: Updateのテストが通るように修正
# Update Test
class TestUpdateHoloMember:
    @pytest.mark.parametrize('attrs_to_change, values',
        (
            (
                ['type'],
                ['3']
            ),
            (
                ['name'],
                ['new fake holo_member name']
            ),
            (
                ['description'],
                ['new fake holo_member description']
            ),
            (
                ['age'],
                [3.14]
            ),
            (
                ['twitter'],
                ['https://twitter.com']
            ),
            (
                ['name', 'description'],
                [  
                    'extra new fake holo_member name',
                    'extra new fake holo_member description'
                ]
            ),
            (
                ['type', 'name', 'description', 'age', 'twitter'],
                ['3', 'test', 'testttttttt', 2.00, 'https://aaa']
            ),
        ),
    )
    async def test_update_holo_member_with_valid_input(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_holo_member: HoloMemberInDB,
        attrs_to_change: List[str],
        values: List[str],
    ) -> None:
        holo_member_update = {
            'holo_member_update': {
                attrs_to_change[i]: values[i] for i in range(
                    len(attrs_to_change)
                )
            }
        }
        res = await client.put(
            app.url_path_for(
                'holo_member:update-holo_member-by-id', 
                id=test_holo_member.id
            ),
            json=holo_member_update
        )
        assert res.status_code == HTTP_200_OK
        updated_holo_member = HoloMemberInDB(**res.json())
        assert updated_holo_member.id == test_holo_member.id

        for i, item in enumerate(attrs_to_change):
            assert getattr(
                updated_holo_member,
                attrs_to_change[i]
                ) != getattr(
                    test_holo_member,
                    attrs_to_change[i]
                )
            assert getattr(
                updated_holo_member, 
                attrs_to_change[i]
            ) == values[i]

        for attr, value in updated_holo_member.dict().items():
            if attr not in attrs_to_change:
                assert getattr(test_holo_member, attr) == value

    @pytest.mark.parametrize(
        'id, payload, status_code',
        (
            (-1, {'name': 'test'}, 422),
            (0, {'name': 'test2'}, 422),
            (500, {'name': 'test3'}, 404),
            (1, None, 422),
            (1, {'type': 'invalid color type'}, 422),
            (1, {'type': None}, 400),
        ),
    )
    async def test_update_holo_member_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        id: int,
        payload: dict,
        status_code: int,
    ) -> None:
        holo_member_update = {
            'holo_member_update': payload
        }
        res = await client.put(
            app.url_path_for('holo_member:update-holo_member-by-id', id=id),
            json=holo_member_update
        )
        assert res.status_code == status_code

# Delete Test
class TestDeleteHoloMember:
    async def test_can_delete_holo_member_successfully(
        self, 
        app: FastAPI, 
        client: AsyncClient, 
        test_holo_member: HoloMemberInDB
    ) -> None:
        res = await client.delete(
            app.url_path_for(
                'holo_member:delete-holo_member-by-id', 
                id=test_holo_member.id
            )
        )
        assert res.status_code == HTTP_200_OK

        res = await client.get(
            app.url_path_for(
                'holo_member:get-holo_member-by-id', 
                id=test_holo_member.id
            )
        )
        assert res.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        'id, status_code',
        (
            (500, 404),
            (0, 422),
            (-1, 422),
            (None, 422),
        ),
    )
    async def test_delete_invalid_input_throws_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        id: int,
        status_code: int
    ) -> None:
        res = await client.delete(
            app.url_path_for(
                'holo_member:delete-holo_member-by-id', 
                id=id
            )
        )
        assert res.status_code == status_code