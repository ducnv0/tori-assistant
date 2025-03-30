## Setting Up the Environment and Running the App

Currently, there is an issue with the presigned Minio URL in Docker. To work around this, we'll run Minio in Docker while keeping the server on the local machine.

### Steps to Set Up and Run the App

1. **Configure the Environment**
    - Set up the `.env` file based on `.env.example`.

2. **Initialize the Database**
    - Run the following command to create database tables:
      ```sh
      alembic upgrade head
      ```  
    - Alternatively, you can use `example-db.sqlite`.

3. **Set Up Minio/S3**
    - Start Minio using Docker:
      ```sh
      docker-compose up -d minio
      ```  

4. **Install Dependencies**
    - Install required dependencies:
      ```sh
      pip install -r requirements.txt
      ```  

5. **Run the Application**
    - Start the application with:
      ```sh
      uvicorn main:app --port 8000
      ``` 
6. Access the application at `http://localhost:8000`
7. Access the API documentation at `http://localhost:8000/docs`

### Run Unit Tests
- To run the tests, use:
  ```sh
  pytest
  ```

## Database Diagram

```mermaid
erDiagram
    user {
        int id PK
        string username
    }
    conversation {
        int id PK
        int user_id FK
        string title
    }
    message {
        int id PK
        int conversation_id FK
        string role
        string message_type
        string content
        string file_path
    }
    websocket_connection {
        int user_id PK, FK
        int conversation_id PK, FK
        datetime last_active
    }

    user ||--o{ conversation : "has"
    conversation ||--o{ message : "contains"
    user ||--o{ websocket_connection : "has"
    conversation ||--o{ websocket_connection : "has"
```

## System Architecture
```mermaid
graph LR
    Client -- 1/WS Message --> APIServer
    APIServer -- 2. Save Media --> Minio
    APIServer -- 3. Save Message --> DB[(PostgreSQL)]
    APIServer -- 4. Send Task (message_id) --> Celery
    Celery -- 5. Process Message --> LLM
    LLM -- 6. Response --> Celery
    Celery -- 7. Save Response Message --> DB
    Celery -- 8. Save Media --> Minio
    Celery -- 9. Response message_id --> APIServer
    APIServer -- 10. Read Response --> DB
    APIServer -- 11. Get Pre-signed URL --> Minio
    APIServer -- 12. Response to Client --> Client
 ```

### API Server (FastAPI, SQLAlchemy)
- Handles client interactions via REST and WebSocket APIs.
- Receives messages, saves them to the database, and delegates processing to Celery.

### Database (PostgreSQL)
- Stores messages, user data, and metadata for retrieval.

### MinIO
- Manages storage of media files (images, audio, video).
- Provides pre-signed URL access for secure media retrieval.

### Client (Vue.js)
- Provides a user interface for chat interactions.
- Sends and receives messages via WebSockets.

### Celery
- Asynchronously processes messages.
- Calls the LLM API and stores responses in the database and MinIO.
- Notifies the API server when the response is ready.

### LLM API
- Processes messages using an AI model.
- Generates responses for the chat system.

### Workflow

1. **Client** sends a message over WebSocket.
2. **API Server** saves the message in PostgreSQL and stores media in MinIO.
3. **API Server** sends a processing task to Celery.
4. **Celery** retrieves the message, calls the LLM API, processes the response, and stores it in PostgreSQL and MinIO.
5. **Celery** notifies the API Server with the response message ID.
6. **API Server** retrieves the response, generates pre-signed URLs for media, and sends it to the client.

### Why This Tech Stack?

- **WebSocket** – Enables **real-time chat functionality** with low-latency message delivery.
- **FastAPI** – High-performance, async-ready API framework with **WebSockets, REST APIs**. Pydantic ensures **data validation and serialization**.
- **SQLAlchemy + PostgreSQL** – Ensures **efficient data storage, integrity, and retrieval** for chat messages and media metadata.
- **Celery** – Handles **background task execution** for LLM processing, media pre-processing (audio/video), and **scheduled tasks (cron jobs)**. Includes **retry mechanisms** for fault tolerance.
- **MinIO + Pre-Signed URLs** – Securely stores **user-generated media**, allowing **direct client access** while offloading bandwidth from the API server.


## Implementation Plan
I will build the entire system flow, making sure all key parts—like the WebSocket API, message handling, database storage, and response processing—work correctly. However, I will not use Celery for background tasks.

Instead of running Celery, I will mock its behavior by returning predefined or simple test responses. This means the system will still process messages, but without actually using Celery to handle them in the background.

This approach allows me to focus on building and testing the core system, making sure messages are sent, received, and stored properly. It also keeps things simple and easy to run, without needing a full Celery setup.

## Constraints

### 1. At any time, a maximum of 50 clients are allowed to communicate
see `app.service.websocket_connection_service.WebsocketConnectionService`
- Check websocket_connection table for the number of concurrent user
- If accepted, create a new websocket_connection entry, else reject the connection
- Release the connection (delete) when the client disconnects

What if the server crashes in the middle of connection, the connection will not be released, and the client will not be able to connect again.

- After establishing the connection, periodically update the last_active timestamp
- Have a cron job to delete the websocket_connection entry if the last_active timestamp is older than a certain threshold
- This will ensure that the connection is released even if the server crashes

### 2. At any time, a maximum of 500 messages are processed by the server
- Use T**ask Rate Limit** in Celery

### 3. 1 client cannot make 2 connections to the server simultaneously
- Similar to the first point, check the websocket_connection table for number of active connections for the user

### 4. All clients must send at least one message to the server
- I quite don't understand this requirement. All clients must send at least one message to the server, If not what to expect?

