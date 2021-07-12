from typing import List
from app.db.repositories.base import BaseRepository
from app.models.holo_member import HoloMemberCreate, HoloMemberInDB, HoloMemberUpdate
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.holo_member as query


class HoloMemberRepository(BaseRepository):

    # 作成
    async def create_holo_member(self, *, new_holo_member: HoloMemberCreate) -> HoloMemberInDB:
        query_values = new_holo_member.dict()
        holo_member = await self.db.fetch_one(
            query=query.CREATE_HOLO_MEMBER_QUERY,
            values=query_values
        )

        return HoloMemberInDB(**holo_member)

    # id を元に取得
    async def get_holo_member_by_id(self, *, id: int) -> HoloMemberInDB:
        holo_member = await self.db.fetch_one(
            query=query.GET_HOLO_MEMBER_BY_ID_QUERY,
            values={"id": id}
        )

        if not holo_member:
            return None

        return HoloMemberInDB(**holo_member)
    
    # 全取得
    async def get_all_holo_member(self) -> List[HoloMemberInDB]:
        holo_member_records = await self.db.fetch_all(
            query=query.GET_ALL_HOLO_MEMBER_QUERY
        )
        return [HoloMemberInDB(**item) for item in holo_member_records]

    # 更新
    async def update_holo_member(
        self, *, id: int, holo_member_update: HoloMemberUpdate
    ) -> HoloMemberInDB:
        holo_member = await self.get_holo_member_by_id(id=id)

        if not holo_member:
            return None
        
        holo_member_update_params = holo_member.copy(
            update=holo_member_update.dict(exclude_unset=True)
        )
        if holo_member_update_params.type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid color type. Cannot be None.')

        try:
            updated_holo_member = await self.db.fetch_one(
                query=query.UPDATE_HOLO_MEMBER_BY_ID_QUERY,
                values=holo_member_update_params.dict()
            )
            return HoloMemberInDB(**updated_holo_member)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid update params.')

    # 削除
    async def delete_holo_member_by_id(self, *, id: int) -> int:
        holo_member = await self.get_holo_member_by_id(id=id)

        if not holo_member:
            return None

        deleted_id = await self.db.execute(
            query=query.DELETE_HOLO_MEMBER_BY_ID_QUERY, values={'id': id})
        return deleted_id