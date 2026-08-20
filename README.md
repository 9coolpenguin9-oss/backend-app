# FastAPI Backend Service

FastAPIとPostgreSQLで構築した、非同期処理・自動テスト・CIデプロイに対応したRESTful APIバックエンドサービスです。

---

## 開発の背景・こだわり

実務を意識し、非同期処理や自動テスト（CI）を組み込んだ堅牢なWeb APIの構築手順を習得するため。体験することが肝心だと考えたため簡素なAPIです。

---

## 本番環境 & APIドキュメント
- **Swagger UI（動作確認）**: https://backend-app-n7ph.onrender.com/docs
- **GitHub リポジトリ**: https://github.com/9coolpenguin9-oss/backend-app

---

## 技術スタック
- **バックエンド**: Python 3.11 / FastAPI
- **データベース**: PostgreSQL / SQLAlchemy / Alembic (マイグレーション)
- **コンテナ化**: Docker / Docker Compose
- **ホスティング**: Render (Web Service + Managed PostgreSQL)
- **CI/CD**: GitHub Actions (pytest 自動テスト実行)

---

## システム構成図

```mermaid
graph TD
    User[クライアント / フロントエンド] -->|HTTPS| RenderApp[Render: FastAPI App]
    RenderApp -->|SQL| RenderDB[(Render: PostgreSQL)]
    Developer[開発者] -->|git push| GitHub[GitHub Repogitory]
    GitHub -->|Trigger| Actions[GitHub Actions CI: Pytest]
    GitHub -->|Auto Deploy| RenderApp