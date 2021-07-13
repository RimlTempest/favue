from typing import List
from app.api.dependencies.database import get_repository
from app.db.repositories.holo_member import HoloMemberRepository
from app.models.holo_member import (
    HoloMemberCreate,
    HoloMemberPublic,
    HoloMemberUpdate
)
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

router = APIRouter()

# @router.get("/")
# async def get_all_3rd_holomember() -> List[dict]:
#     holo_3rd_list = [
#         {"id": 1, "type": "3", "name": "兎田ぺこら",
#           "twitter": "https://twitter.com/usadapekora", "age": 111},
#         {"id": 2, "type": "3", "name": "潤羽るしあ",
#           "twitter": "https://twitter.com/uruharushia", "age": 1600},
#         {"id": 3, "type": "3", "name": "不知火フレア", "twitter":
#           "https://twitter.com/shiranuiflare", "age": 221},
#         {"id": 4, "type": "3", "name": "白銀ノエル", "twitter":
#           "https://twitter.com/shiroganenoel", "age": 18},
#         {"id": 5, "type": "3", "name": "宝鐘マリン", "twitter":
#           "https://twitter.com/houshoumarine", "age": 17},
#     ]

#     return holo_3rd_list

# get 全取得


@router.get('/',
            response_model=List[HoloMemberPublic],
            name='holo_member:get-all-holo_member')
async def get_all_holo_member(
    holo_member_repo: HoloMemberRepository = Depends(
        get_repository(HoloMemberRepository))
) -> List[HoloMemberPublic]:
    return await holo_member_repo.get_all_holo_member()

# post リクエストを受け取る


@router.post(
    "/",
    response_model=HoloMemberPublic,
    name="holo_member:create-holo_member",
    status_code=HTTP_201_CREATED
)
async def create_new_holo_member(
    new_holo_member: HoloMemberCreate = Body(..., embed=True),
    holo_member_repo: HoloMemberRepository = Depends(
        get_repository(HoloMemberRepository)),
) -> HoloMemberPublic:
    created_holo_member = await holo_member_repo.create_holo_member(
        new_holo_member=new_holo_member
    )
    return created_holo_member

# get idを元に取得


@router.get(
    '/{id}/',
    response_model=HoloMemberPublic,
    name="holo_member:get-holo_member-by-id"
)
async def get_holo_member_by_id(
    id: int, holo_member_repo: HoloMemberRepository = Depends(
        get_repository(HoloMemberRepository)
    )
) -> HoloMemberPublic:
    holo_member = await holo_member_repo.get_holo_member_by_id(id=id)
    if not holo_member:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="指定されたidのホロライブメンバーは見つかりませんでした")
    return holo_member

# put idを元に更新


@router.put(
    '/{id}/',
    response_model=HoloMemberPublic,
    name='holo_member:update-holo_member-by-id'
)
async def update_holo_member_by_id(
    id: int = Path(..., ge=1, title='The ID of the holo_member to update.'),
    holo_member_update: HoloMemberUpdate = Body(..., embed=True),
    holo_member_repo: HoloMemberRepository = Depends(
        get_repository(HoloMemberRepository)),
) -> HoloMemberPublic:

    updated_holo_member = await holo_member_repo.update_holo_member(
        id=id,
        holo_member_update=holo_member_update)
    if not updated_holo_member:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No holo_member found with that id.')
    return updated_holo_member

# delete idを元に削除


@router.delete(
    '/{id}/',
    response_model=int,
    name='holo_member:delete-holo_member-by-id'
)
async def delete_holo_member_by_id(
    id: int = Path(..., ge=1, title='The ID of the holo_member to delete.'),
    holo_member_repo: HoloMemberRepository = Depends(
        get_repository(HoloMemberRepository))
) -> int:
    deleted_id = await holo_member_repo.delete_holo_member_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No holo_member found with that id.')
    return deleted_id
