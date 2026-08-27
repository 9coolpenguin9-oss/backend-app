import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# プロジェクトルートをパスに追加(2つ上のフォルダ、backend_app参照)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.config import settings
from database import Base

# テーブル定義（モデル）をメタデータに登録するために読み込む これがないとテーブルが全削除される
import models  

# alembic.iniのコピー（自動）　元ファイルを書き換えたくないため
config = context.config

# .env から読み込んだ DATABASE_URL を Alembic にセット　URLにはパスワードが含まれているため分離している
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# ログ設定　二重否定に見えるのは、空文字や０でも実行するため
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic が監視する MetaData　Alembic指定の変数名
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """オフラインモードでマイグレーションを実行"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """オンラインモード（DB接続状態）でマイグレーションを実行"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()