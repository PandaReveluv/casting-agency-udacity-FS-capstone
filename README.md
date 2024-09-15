# casting-agency-udacity-FS-capstone

## Document endpoint

### GET /actors

- Retrieve all actors information
- Example response:

```json
{
  "actors": [
    {
      "age": 20,
      "gender": "Male",
      "id": 1,
      "name": "Test"
    }
  ],
  "success": true
}
```

### GET /movies

- Retrieve all movies information
- Example response:

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 08 Sep 2024 21:39:45 GMT",
      "title": "Movie1"
    }
  ],
  "success": true
}
```

### POST /actor

- Create new actor
- Example request body:

```json
{
  "name": "Test2",
  "age": 56,
  "gender": "Female"
}
```

- Example response body:

```json
{
  "actor": {
    "age": 56,
    "gender": "Female",
    "id": 3,
    "name": "Test2"
  },
  "success": true
}
```

### POST /movie

- Create new movie
- Example request body:

```json
{
  "title": "Movie2",
  "release_date": "2024-09-07 21:39:45.859"
}
```

- Example response body:

```json
{
  "movie": {
    "id": 3,
    "release_date": "Sat, 07 Sep 2024 21:39:45 GMT",
    "title": "Movie2"
  },
  "success": true
}
```

### PATCH /actor/<actor_id>

- Edit information of existing actor
- Example request body:

```json
{
  "name": "Test2",
  "age": 46,
  "gender": "Female"
}
```

- Example response body:

```json
{
  "actor": {
    "age": 46,
    "gender": "Female",
    "id": 1,
    "name": "Test2"
  },
  "success": true
}
```

### PATCH /movie/<movie_id>

- Edit information of existing movie
- Example request body:

```json
{
  "title": "Edited",
  "release_date": "2024-09-08 21:39:45.859"
}
```

- Example response body:

```json
{
  "actor": {
    "id": 1,
    "release_date": "Sun, 08 Sep 2024 21:39:45 GMT",
    "title": "Edited"
  },
  "success": true
}
```

### DELETE /actor/<actor_id>

- Delete existing actor
- Example response:

```json
{
  "delete": "4",
  "success": true
}
```

### DELETE /movie/<movie_id>

- Delete existing movie
- Example response:

```json
{
  "delete": "4",
  "success": true
}
```

## How to run local

#### Install pip requirements
```bash
pip install -r requirements.txt
```

#### Setup environment variables, example:

- FLASK_APP=api.py
- FLASK_ENV=development
- DATABASE_USERNAME=postgres
- DATABASE_PASSWORD=admin
- DATABASE_URL=localhost
- DATABASE_NAME=casting-agency
- JWT_SECRET=my_secret

#### Run command:

```bash
flask run --reload
```

## Deployment on Render
- Setup Postgres database
- Create new web service
- Build docker image:
```bash
docker build --tag "casting-agency" .
```
- Run docker using this command:
```bash
docker run -p 8080:8080 casting-agency
```
