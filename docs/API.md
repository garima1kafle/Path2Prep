# Path2Prep API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /api/auth/users/register/
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirm": "string",
  "full_name": "string (optional)",
  "country": "string (optional)",
  "age": "integer (optional)"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "string",
  "password": "string"
}

Response:
{
  "user": {...},
  "access": "jwt_token",
  "refresh": "refresh_token"
}
```

#### Get Current User
```http
GET /api/auth/users/me/
Authorization: Bearer <token>
```

#### Logout
```http
POST /api/auth/users/logout/
Authorization: Bearer <token>

{
  "refresh_token": "string"
}
```

### Profile

#### Get Profile
```http
GET /api/profiles/me/
Authorization: Bearer <token>
```

#### Create/Update Profile
```http
POST /api/profiles/profiles/
PATCH /api/profiles/profiles/
Authorization: Bearer <token>

{
  "gpa": 3.5,
  "degree_level": "Bachelor's",
  "major": "Computer Science",
  "country": "USA",
  "target_country": "Canada",
  "ielts_score": 7.5,
  "toefl_score": 100,
  "technical_skills": ["Python", "JavaScript"],
  "soft_skills": ["Leadership", "Communication"],
  "interests": ["Technology", "Research"]
}
```

### Career Recommendations

#### Get Career Recommendations
```http
POST /api/recommend-career/recommend/
Authorization: Bearer <token>

{
  "top_k": 3 (optional)
}

Response:
{
  "top_careers": [
    {
      "career": "Data Scientist",
      "confidence": 0.87,
      "description": "...",
      "category": "STEM"
    }
  ]
}
```

#### Get My Recommendations
```http
GET /api/recommend-career/my_recommendations/
Authorization: Bearer <token>
```

### Scholarships

#### List Scholarships
```http
GET /api/scholarships/?country=USA&search=engineering&ordering=-deadline
```

#### Match Scholarships
```http
POST /api/scholarships/match/
Authorization: Bearer <token>

{
  "top_k": 5 (optional)
}

Response:
{
  "matches": [
    {
      "scholarship": {...},
      "relevance_score": 0.92,
      "method": "bert_tfidf_ensemble"
    }
  ]
}
```

#### Create Application
```http
POST /api/applications/
Authorization: Bearer <token>

{
  "scholarship_id": 1,
  "status": "not_started"
}
```

#### Create Bookmark
```http
POST /api/bookmarks/
Authorization: Bearer <token>

{
  "scholarship_id": 1
}
```

### Notifications

#### List Notifications
```http
GET /api/notifications/
Authorization: Bearer <token>
```

#### Mark Notification as Read
```http
POST /api/notifications/{id}/mark_read/
Authorization: Bearer <token>
```

#### Get Unread Count
```http
GET /api/notifications/unread_count/
Authorization: Bearer <token>

Response:
{
  "unread_count": 5
}
```

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

Common status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

