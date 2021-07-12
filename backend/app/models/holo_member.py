from enum import Enum
from typing import Optional

from app.models.core import CoreModel, IDModelMixin


class GenerationType(str, Enum):
    _0thGen = "0"
    _1stGen = "1"
    _2ndGen = "2"
    _3rdGen = "3"
    _4thGen = "4"
    _5thGen = "5"
    _EN = "EN"
    _ID = "ID"
    _Gamers = "Gamers"

# 全リソースで共有する属性
class HoloMemberBase(CoreModel):
    type: Optional[GenerationType]
    name: Optional[str]
    description: Optional[str]
    age: Optional[float]
    twitter: Optional[str]

# 新しいリソースを作成する際に必須の属性
class HoloMemberCreate(HoloMemberBase):
    name: str
    type: GenerationType

# 更新することが可能な属性
class HoloMemberUpdate(HoloMemberBase):
    type: GenerationType

# データベースから取得するリソースに存在する属性
class HoloMemberInDB(IDModelMixin, HoloMemberBase):
    type: GenerationType
    name: str
    description: str
    age: float
    twitter: str

# GET, POST, PUTリクエストで返されるデータに存在する属性
class HoloMemberPublic(IDModelMixin, HoloMemberBase):
    pass