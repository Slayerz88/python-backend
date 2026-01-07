DOWNLOAD THE ZIP FILE (backend assessment_zip.zip) FOR ALL THE CODE


## 1⃣ Problem Understanding & Assumptions

### Interpretation
This project implements a REST API service using FastAPI and PostgreSQL that acts as a bridge between a local database and an external AI service. The service manages tasks and uses an external AI provider to generate summaries for important tasks.

### Use Case
The specific scenario implemented is an "AI-Powered Task Summarizer" where users can create, read, update, and delete tasks. When a task is marked as important, the system automatically generates an AI summary using an external service.

### Assumptions
- **Data Formats**: Task titles are required strings, descriptions are optional text, status/priority have specific allowed values
- **External API Reliability**: The system degrades gracefully when external AI services are unavailable
- **User Authentication**: For this example, authentication is not implemented but would be needed for production
- **Business Logic**: Only important tasks should trigger AI summary generation to optimize API usage costs
- **Environment Variables**: Required configuration values are provided via environment variables

## 2⃣ Design Decisions

### Database Schema
The database schema consists of a single `tasks` table with the following structure:
- `id`: Primary key, auto-incremented integer
- `title`: Required string with index for efficient search
- `description`: Optional text field
- `status`: String field with values: pending, in_progress, completed
- `priority`: String field with values: low, medium, high
- `created_at`: Timestamp with timezone (auto-populated)
- `updated_at`: Timestamp with timezone (auto-updates)
- `is_important`: Boolean flag to determine if AI summary should be generated
- `summary`: Text field to store AI-generated summary

### Project Structure
```
fastapi-postgres-api/
├── app/
│   ├── api/          # API endpoints and CRUD operations
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic validation schemas
│   ├── database/     # Database configuration
│   ├── utils/        # Utility functions and API integrations
│   └── tests/        # Test files
├── main.py           # Main application entry point
├── requirements.txt  # Project dependencies
├── .env.example      # Example environment variables
└── README.md         # Project documentation
```

### Validation Logic
- Pydantic models are used for both request bodies and response schemas
- Custom validators ensure status and priority fields have allowed values
- Input validation is performed at the API layer using FastAPI's automatic validation
- Database constraints provide additional data integrity

### External API Design
- Async function handles external API calls to avoid blocking
- Proper timeout handling prevents hanging requests
- Fallback mechanisms ensure functionality when external service is unavailable
- API keys and endpoints are configurable via environment variables

## 3⃣ Solution Approach

### Data Flow
1. **POST /tasks/**: User submits new task
   - Validate input using Pydantic models
   - Save to database
   - If task is important, trigger AI summary generation
   - Update record with generated summary
   - Return created task

2. **GET /tasks/{id}**: User requests specific task
   - Validate task ID exists
   - Retrieve from database
   - Return task data

3. **PUT /tasks/{id}**: User updates existing task
   - Validate task ID exists
   - Update specified fields
   - If task becomes important and has no summary, generate one
   - Return updated task

4. **DELETE /tasks/{id}**: User deletes task
   - Validate task ID exists
   - Remove from database
   - Return success response

## 4⃣ Error Handling Strategy

### Database Errors
- SQLAlchemy errors are caught and converted to appropriate HTTP responses
- Connection failures return 500 Internal Server Error
- Missing records return 404 Not Found

### API Validation
- FastAPI automatically validates Pydantic models
- Invalid input returns 422 Unprocessable Entity with detailed error information
- Custom validators in Pydantic models enforce business rules

### External API Failures
- Errors during external API calls are logged
- System falls back to default behavior when external service unavailable
- Timeouts prevent hanging requests

### Global Exception Handlers
- Custom exception handlers for different error types
- Consistent error response format
- Proper HTTP status codes for all error conditions

## 5⃣ How to Run the Project

### Prerequisites
- Python 3.10+
- PostgreSQL database
- pip package manager

### Setup Instructions
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and external API credentials
   ```
5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### Required Environment Variables
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_db
EXTERNAL_API_KEY=your_external_api_key_here
EXTERNAL_API_URL=https://api.example.com
DEBUG=true
```

### Example API Calls

#### Create a new task:
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the project",
    "status": "pending",
    "priority": "high",
    "is_important": true
  }'
```

#### Get a specific task:
```bash
curl -X GET "http://localhost:8000/tasks/1"
```

#### Update a task:
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "priority": "medium"
  }'
```

#### Delete a task:
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

### Running Tests
```bash
pytest
```

The API documentation is available at `http://localhost:8000/docs` when the application is running (Swagger UI).
