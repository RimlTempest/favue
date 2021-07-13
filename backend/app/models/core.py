from typing import Optional
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, validator

JST = timezone(timedelta(hours=+9), 'JST')


class CoreModel(BaseModel):
    """CoreModel

    新しいモデルを作成する際はこの CoreModel クラスから継承する\n
    継承しているPydantic から提供される BaseModel はデータの検証とデータ型を強制してくれる機能を有しています

    """
    # いずれモデル間でロジックを共有できるように拡張していく
    pass


class DateTimeModelMixin(BaseModel):
    """DateTimeModelMixin

    created_atやupdated_atを司るクラス\n
    基本的に新しいモデルで使用する

    Attributes:
        created_at Optional[datetime]: 作成日時
        updated_at Optional[datetime]: 更新日時

    """
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now(JST)

# IDModelMixin クラスはデータベースから出てくる全てのリソースに使用


class IDModelMixin(BaseModel):
    """IDModelMixin

    モデルで必ず使用されるIDを司るクラス\n
    データベースから出てくる全てのリソースに使用

    Attributes:
        id int: intを指定しているので文字列・ バイト・float は int に
        強制的に変換され、変換できない値だった際は例外が投げられます。

    """
    id: int
