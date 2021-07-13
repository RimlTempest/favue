from enum import Enum
from typing import Optional

from app.models.core import CoreModel, IDModelMixin


class GenerationType(str, Enum):
    """GenerationType

    何期生、またはどこに所属するかの列挙型

    Attributes:
        _nxxGen str: 0~5期生まで
        _EN str: HololiveEnglish
        _ID str: HololiveIndonesia
        _Gamers str: ホロライブゲーマーズ

    """
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
    """HoloMemberBase

    HoloMemberモデルのベースとなるクラス\n
    HoloMemberモデルの操作をする場合はこれを継承する

    Attributes:
        type Optional[GenerationType]: どこに所属するか
        name Optional[str]: ライバーの名前
        description Optional[str]: ライバーの詳細
        age Optional[float]: ライバーの年齢
        twitter Optional[str]: ライバーのTwitterアカウント

    """
    type: Optional[GenerationType]
    name: Optional[str]
    description: Optional[str]
    age: Optional[float]
    twitter: Optional[str]

# 新しいリソースを作成する際に必須の属性


class HoloMemberCreate(HoloMemberBase):
    """HoloMemberCreate

    Create\n
    新しいリソースを作成する際に必須の属性

    Attributes:
        type GenerationType: どこに所属するか
        name str: ライバーの名前

    """
    type: GenerationType
    name: str

# 更新することが可能な属性


class HoloMemberUpdate(HoloMemberBase):
    """HoloMemberUpdate

    Update\n
    更新することが可能な属性

    Attributes:
        type GenerationType: どこに所属するか
        name str: ライバーの名前
        description str: ライバーの詳細
        age float: ライバーの年齢
        twitter str: ライバーのTwitterアカウント

    """
    type: GenerationType
    name: str
    description: str
    age: float
    twitter: str

# データベースから取得するリソースに存在する属性


class HoloMemberInDB(IDModelMixin, HoloMemberBase):
    """HoloMemberInDB

    Select\n
    リソースを更新する際に必須の属性

    Attributes:
        type GenerationType: どこに所属するか
        name str: ライバーの名前
        description str: ライバーの詳細
        age float: ライバーの年齢
        twitter str: ライバーのTwitterアカウント

    """
    type: GenerationType
    name: str
    description: str
    age: float
    twitter: str

# GET, POST, PUTリクエストで返されるデータに存在する属性


class HoloMemberPublic(IDModelMixin, HoloMemberBase):
    """HoloMemberPublic

    GET, POST, PUTリクエストで返されるデータに存在する属性

    Attributes:
        type GenerationType: どこに所属するか
        name str: ライバーの名前
        description str: ライバーの詳細
        age float: ライバーの年齢
        twitter str: ライバーのTwitterアカウント

    """
    pass
