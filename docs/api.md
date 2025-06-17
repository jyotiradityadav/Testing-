# API Documentation

## Endpoints

### Users

- **GET /api/v1/users**
  - Description: Retrieve a list of users.
  - Response: 200 OK, JSON array of user objects.
- **POST /api/v1/users**
  - Description: Create a new user.
  - Request Body: JSON object with user details.
  - Response: 201 Created, JSON object of new user.

### Payments

- **POST /api/v1/payments**
  - Description: Initiate a new payment.
  - Request Body: JSON object with payment details (amount, currency, recipient, etc).
  - Response: 201 Created, JSON object with transaction information.

- **GET /api/v1/payments/{payment_id}**
  - Description: Retrieve payment details by payment ID.
  - Path Parameter: payment_id (string)
  - Response: 200 OK, JSON object with payment information.

### Payment Methods

- **GET /api/v1/users/{user_id}/payment-methods**
  - Description: List payment methods for a specific user.
  - Path Parameter: user_id (string)
  - Response: 200 OK, JSON array of payment methods.

- **POST /api/v1/users/{user_id}/payment-methods**
  - Description: Add a new payment method for a user.
  - Request Body: JSON object with payment method information.
  - Response: 201 Created, JSON object with payment method details.

### Transactions

- **GET /api/v1/transactions**
  - Description: List all transactions.
  - Response: 200 OK, JSON array of transactions.

- **GET /api/v1/transactions/{transaction_id}**
  - Description: Get transaction details by transaction ID.
  - Path Parameter: transaction_id (string)
  - Response: 200 OK, JSON object of transaction details.

### Currency Conversion

- **GET /api/v1/currency/convert**
  - Description: Convert an amount from one currency to another.
  - Query Parameters: from (currency code), to (currency code), amount (decimal)
  - Response: 200 OK, JSON object with converted amount.

### Health Check

- **GET /api/v1/health**
  - Description: Basic health check endpoint.
  - Response: 200 OK, JSON with service status.

---

_Last updated: 2024-06-11_

This document lists all currently implemented REST API endpoints. For further details on request/response schemas, authentication, and error handling, refer to source code or contact maintainers.