# Britecore Assignment

Britecore Data Engineerning Assignment

### Requirements

- Python 3.7
- Docker

### Setup

- Create **.env** file in project directory

```
SECRET_KEY="48tkMdPi-dPyIdqGtwGqYbG-argF699U1-H46XmEmU0="

FLASK_APP=run.py
FLASK_ENV=development

DEV_DATABASE_URL=sqlite:////tmp/britecore_dev.db
TEST_DATABASE_URL=sqlite:////tmp/britecore_test.db
DATABASE_URL=sqlite:////tmp/britecore.db
```

### Get Started

- Initialize environment
  
  ```bash
  cd britecore_asssignment
  pipenv shell
  pipenv install --dev
  ```

- Build Docker Image
  
  ```bash
  docker build -t britecore_assignment .
  ```

- Run Docker Container
  
  ```bash
  docker run --name britecore_api -d -p 8000:5000 britecore_assignment:latest
  ```

REST API is now running on http://localhost:8000

### Tasks

- [ ] Build a Data Pipeline/ETL process that takes the CSVs as input and saves into a database at a detailed level while also calculating summarized views. These summarized views could follow star schema or any other that you think will allow for easy querying using different pivots/dimensions. The Data Pipeline can be manually triggered by running a script (include instructions of how to do it!) or automated somehow.

- [ ] Build an API that provides detailed information using different parameters (like agency, month, year, state, etc), summarized information using different parameters (like agency, month, year, state, etc) and an XLS, XLSX or CSV report with Premium info by Agency and Product Line using date range as parameters

- [ ] The Data Pipeline/ETL process and also the logic for generating the report must be done using Pandas

- [ ] Integration or Unit tests

- [ ] Authentication so that only authorized users can query the API

### Endpoints

| Method | URL                                      | Description                                                                                                              |
| ------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| GET    | /api/v1/                                 | Says Hello                                                                                                               |
| POST   | /api/v1/auth/register                    | This endpoint can be used to create user. These user credentails will be used to do Basic Auth with other API Endpoints. |
| GET    | /api/v1/detail/agency                    | Fetches detailed information about agencies. Support for filters.                                                        |
| POST   | /api/v1/detail/agency                    | Create Agency                                                                                                            |
| GET    | /api/v1/detail/agency/[string:agency_id] | Fetches detailed information about particular agency                                                                     |

#### Sample Requests

- Says Hello
  
  ```bash
  curl -XGET -H "Content-type: application/json" 'http://localhost:8000/api/v1/'
  ```

- Create user
  
  ```bash
  curl -XPOST -H "Content-type: application/json" -d '{
   "username": "dummy",
   "password": "dummy"
  }' 'http://localhost:8000/api/v1/auth/register'
  
  ```

- Fetch detailed information about agency with id = 3
  
  ```bash
  curl -L -XGET -H "Content-type: application/json" 'http://localhost:8000/api/v1/detail/agency/3'
  ```

-  Fetch detailed information about all agencies 
  
  ```bash
  curl -L -XGET -H "Content-type: application/json" 'http://localhost:8000/api/v1/detail/agency'
  ```

-   Fetched detailed information about agencies with filters
  
  ```bash
  curl -L -XGET -H "Content-type: application/json" 'http://localhost:8000/api/v1/detail/agency?agency_appointment_year=1957'
  ```

-   Create Agency
  
  ```bash
  curl -L -XPOST -H "Content-type: application/json" -d '{
          'id': '999999',
          'agency_appointment_year': 1957,
          'active_producers': 14,
          'max_age': 85,
          'min_age': 48,
          'vendor': 'Unknown',
          'comissions_start_year': 2011,
          'comissions_end_year': 2013
      }' 'http://localhost:8000/api/v1/detail/agency/'
  ```

### CLI

```bash
# Create admin user
flask initdb

# Import data
flask import <PATH_OF_CSV_FILE>
```
