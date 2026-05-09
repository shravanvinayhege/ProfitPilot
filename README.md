# ProfitPilot

ProfitPilot integrates FastAPI with AI-powered Large Language Models (LLM) to deliver intelligent business insights via a RESTful API. It provides endpoints for retrieving monthly sales and expense summaries, calculating totals and profit margins from PostgreSQL, validating inputs, handling errors, and returning structured responses.

## Features
- **AI-Powered Insights:** Leverages LLM for natural language insights on business data.
- **FastAPI REST API:** Exposes endpoints for financial summaries, profit margin calculations, and reporting.
- **Database Integration:** Retrieves information from a PostgreSQL backend.
- **Input Validation & Error Handling:** Ensures reliable, structured responses.

## Endpoints
Some typical endpoints (actual details may vary):
- `/sales/summary` – Get monthly sales summary
- `/expenses/summary` – Get monthly expenses
- `/profit/margin` – Calculate profit margin
- `/ai/insight` – Get business insight from AI

Full API documentation is available via FastAPI’s built-in docs at `/docs` after running the server.

## Project Structure
```
ProfitPilot/
├── app.py         # FastAPI application entry point
├── main.py        # Main runner (could alias to app.py)
├── ai.py          # AI integration logic
├── database.py    # Database connection logic
├── models.py      # ORM models for DB tables
├── schemas.py     # Pydantic schemas for request/response validation
├── security.py    # Security/authentication helpers
├── requirements.txt
├── runtime.txt
├── render.yaml    # Deployment configuration
├── alembic.py     # Migration tool (consider using Alembic folder structure)
├── .gitignore
├── .python-version
```

## Getting Started
### Prerequisites
- Python 3.9+
- PostgreSQL database
- (Optional) Virtualenv or Conda

### Installation
```bash
# Clone the repo
$ git clone https://github.com/shravanvinayhege/ProfitPilot.git
$ cd ProfitPilot

# Create virtual environment and activate
$ python -m venv venv
$ source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
$ pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file with the following (modify as needed):
```
DATABASE_URL=postgresql://user:password@localhost/dbname
AI_API_KEY=your_ai_api_key
```

### Running the Application
```bash
# Start FastAPI app
$ uvicorn app:app --reload
```
Visit `http://localhost:8000/docs` for interactive API documentation.



## Deployment (Render)
1. Push this repository to GitHub.
2. In Render, create a **Blueprint** service and select this repository.
3. Render will read `render.yaml` and create the web service using:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set these required environment variables in Render:
   - `DATABASE_URL`
   - `APP_USERNAME`
   - `APP_PASSWORD`
   - Note: `render.yaml` keeps these with `sync: false`, so set them directly on the service in Render.
5. Set this optional environment variable if you want AI insights:
   - `OPEN_ROUTER_KEY` (or `OPENROUTER_API_KEY`)

After deploy, verify the health endpoint at `/healthz` and the API docs at `/docs`.

## Contributing
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## License
[MIT](LICENSE)
