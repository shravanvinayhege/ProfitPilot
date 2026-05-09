import secrets
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> str:
	if USERNAME is None or PASSWORD is None:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Authentication credentials are not configured.",
		)

	is_username_valid = secrets.compare_digest(credentials.username, USERNAME)
	is_password_valid = secrets.compare_digest(credentials.password, PASSWORD)

	if not (is_username_valid and is_password_valid):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid username or password",
			headers={"WWW-Authenticate": "Basic"},
		)

	return credentials.username


def get_current_user(username: str = Depends(verify_credentials)) -> str:
	return username
