import json
import os
from pathlib import Path
from urllib import error, request


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


def call_llm(prompt: str) -> str:
	"""Call OpenRouter and return a plain-text response.

	Falls back to a deterministic local message if credentials are missing
	or the API request fails.
	"""
	_load_env_file()
	api_key = os.getenv("OPEN_ROUTER_KEY") or os.getenv("OPENROUTER_API_KEY")
	if not api_key:
		return (
			"AI insights are unavailable because OPEN_ROUTER_KEY is not set. "
			"Add the key in environ.env and restart the API."
		)

	payload = {
		"model": "openai/gpt-4o-mini",
		"messages": [
			{"role": "system", "content": "You are a concise business analyst."},
			{"role": "user", "content": prompt},
		],
		"temperature": 0.2,
	}

	req = request.Request(
		url="https://openrouter.ai/api/v1/chat/completions",
		data=json.dumps(payload).encode("utf-8"),
		headers={
			"Authorization": f"Bearer {api_key}",
			"Content-Type": "application/json",
		},
		method="POST",
	)

	try:
		with request.urlopen(req, timeout=20) as response:
			body = response.read().decode("utf-8")
			parsed = json.loads(body)
			return parsed["choices"][0]["message"]["content"].strip()
	except (error.URLError, KeyError, IndexError, json.JSONDecodeError):
		return "AI insights are currently unavailable. Please try again shortly."
