# favue

fastAPI + Vue + Dockerのサンプル  

## 立ち上げ方

### サーバ側

ビルド＆up
`docker-compose up -d --build`

停める
`docker-compose down`

立ち上がってるコンテナ確認
`docker ps`

#### マイグレーション
`docker exec -it favue_server_1 /bin/sh`
※ favue_server_1の部分は`docker ps`で確認したserverの名前

スクリプトファイル（script.py.mako）からマイグレートファイルを作成
`alembic revision -m "create_first_tables"`
※1 create_first_tablesは好きな文字列でおｋ
※2 コマンドがコピペできないかもしれないので手打ちがんばろう！

`backend/app/db/migrations/versions`に生成されている。

生成されたファイルにマイグレーションする内容を記述する

```py
# 例
# created_at, updated_atのトリガー
def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

# timestampsのモデル
def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_holo_member_table() -> None:
    op.create_table(
        "holo_member",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("twitter", sa.Text, nullable=False),
        sa.Column("age", sa.Numeric(10, 1), nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_holo_member_modtime
            BEFORE UPDATE
            ON holo_member
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def upgrade() -> None:
    create_updated_at_trigger()
    create_holo_member_table()


def downgrade() -> None:
    op.drop_table("holo_member")
    op.execute("DROP FUNCTION update_updated_at_column")
```

生成したファイルをマイグレートする
`alembic upgrade head`

※ 作り直した際
`FAILED: Can't locate revision identified by '29951ce35180'`
のようなエラーが出る場合はリビジョンテーブルにデータが残ってないか確認する

こちらでposgreのコンテナに入る
`docker-compose exec db psql -h localhost -U postgres --dbname=postgres`

確認
`SELECT * FROM alembic_version`

```Text
+-------------+
| version_num |
+-------------+
| 29951ce35180|
+-------------+
```

このように残ってたらDropする

`DROP TABLE alembic_version;`

もう一度Select文で確認してしっかりDropできていればalembic upgradeをする

成功したら作成したテーブルを確認する
`\d holo_member`

※ holo_memberは作ったテーブル名で

#### 実行

Imageビルド
`docker-compose build`

コンテナの起動
`docker-compose up -d`

build & upを行う
`docker-compose up -d --build`

テストの実行
`docker-compose exec server pytest -vv`