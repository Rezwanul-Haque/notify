# Notify service
FastAPI based application to send messages to user registered devices using cloud messaging service
(For this application I'll use Firebase Cloud Messaging also known as FCM).

## API Client
Application gives two OpenAPI standard API Client for testing APIs.

**Swagger** /docs

**ReDoc** /redoc 

## Application API Endpoints

**POST** /notify/v1/register
   
**Description:** Endpoint will register user device token to server.
       
**Payload** 

```
      {
          "user_id": 1,
          "token": "<fcm_device_registered_token>",
          "device_info": {
              "device_type": "android",
              "ip": "127.0.0.1"
          }
      }
``` 

**Response**
    
```
      {
          "user_id": 1,
          "token": "<fcm_device_registered_token>",
          "device_info": {
              "device_type": "android",
              "ip": "127.0.0.1"
          }
      }
```

**POST** /notify/v1/message
   
**Description:** Endpoint will send a message to user's registered devices.
       
**Payload** 

```
      {
          "user_id": 1,
          "message":  "Leave of Absense",
          "notify": {
              "title" : "Leave Approval test 3",
              "body" : "One Leave Request Is Pending for your approval From Employee"
          }
      }
``` 

**Response**
    
```
    {
        "success_count": 1,
        "message": "sent message to 1 device(s)",
        "error": {
            "count": 2,
            "errors": [
                {
                    "status": "NOT_FOUND",
                    "code": 404,
                    "error_code": "UNREGISTERED",
                    "cause": "Requested entity was not found."
                },
                {
                    "status": "NOT_FOUND",
                    "code": 404,
                    "error_code": "UNREGISTERED",
                    "cause": "Requested entity was not found."
                }
            ]
        }
    }
```

| No     | Table of content |
| :-----------: | ----------------: |
| 1      | [Local Development Guide](docs/local.md)  |
