from pathlib import Path
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


def _load_env_file() -> None:
	env_path = Path(__file__).with_name("environ.env")
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue

		key, value = line.split("=", 1)
		os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()

raw_database_url = os.getenv("DATABASE_URL")


def _normalize_database_url(url: str) -> str:
	if url.startswith("postgres://"):
		return url.replace("postgres://", "postgresql+psycopg2://", 1)
	return url

if not raw_database_url:
	database_url = URL.create(
		drivername="postgresql",
		username=os.getenv("DB_USER", "postgres"),
		password=os.getenv("DB_PASSWORD", "postgres"),
		host=os.getenv("DB_HOST", "localhost"),
		port=int(os.getenv("DB_PORT", "5432")),
		database=os.getenv("DB_NAME", "fastapi"),
	)
	SQLALCHEMY_DATABASE_URL = str(database_url)
else:
	SQLALCHEMY_DATABASE_URL = _normalize_database_url(raw_database_url)
	database_url = SQLALCHEMY_DATABASE_URL

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
