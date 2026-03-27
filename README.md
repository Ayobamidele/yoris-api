# Yoris Super App API

This provides the core API endpoints required for the E-commerce, Logistics, Chat, and Fintech flows.

## Environment Variables
- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`

## Example Commands

### 1. Health Check
```bash
curl -X GET http://localhost:8000/health
```

### 2. Create a User (Rider)
```bash
curl -X POST http://localhost:8000/users/ \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "username": "johndoe", "email": "john@test.com"}'
```

### 3. Create a Post (E-commerce Order)
Includes Idempotency header test (`X-Idempotency-Key`):
```bash
curl -X POST http://localhost:8000/posts/ \
-H "Content-Type: application/json" \
-H "X-Idempotency-Key: test-key-1234" \
-d '{"userId": 1, "title": "Buy iPhone", "body": "Need to purchase immediately", "amount": 1200.5}'
```

### 4. Create a Wallet Transfer
This checks atomic operations and Redis locks.
```bash
curl -X POST http://localhost:8000/wallet/transfer \
-H "Content-Type: application/json" \
-d '{"senderId": 1, "receiverId": 2, "amount": 25.0}'
```

### 5. Simulate Chaos Fast Failure
```bash
curl -X GET http://localhost:8000/users/ \
-H "X-Chaos-Type: fail"
```
