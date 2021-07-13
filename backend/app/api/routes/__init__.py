'''routes

__init__.py

* APIのRoutingを行うモジュール
* RESTfulAPI設計なので基本的に1RouterにつきCRUD操作が可能


モジュール検索のためのマーカー。
存在するディレクトリ名を名前とする名前空間の初期化を行う。
同、名前空間におけるワイルドカード import の対象を定義する (__all__ の定義) 。
同じディレクトリにある他のモジュールの名前空間を定義する。

'''

from fastapi import APIRouter
from app.api.routes.holo_member import router as holo_router


router = APIRouter()
router.include_router(holo_router, prefix="/holo_member", tags=["holo_member"])
