CREATE TABLE customers (
  customer_id VARCHAR(20) PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(255),
  state VARCHAR(2),
  created_date DATE
);

CREATE TABLE policies (
  policy_id VARCHAR(20) PRIMARY KEY,
  customer_id VARCHAR(20) REFERENCES customers(customer_id),
  policy_type VARCHAR(50),
  policy_start_date DATE,
  policy_end_date DATE,
  premium_amount DECIMAL(12, 2),
  status VARCHAR(50)
);

CREATE TABLE claims (
  claim_id VARCHAR(20) PRIMARY KEY,
  policy_id VARCHAR(20) REFERENCES policies(policy_id),
  claim_date DATE,
  claim_amount DECIMAL(12, 2),
  claim_type VARCHAR(50),
  fraud_score DECIMAL(5, 4),
  is_fraud_flagged BOOLEAN,
  status VARCHAR(50)
);

CREATE TABLE payments (
  payment_id VARCHAR(20) PRIMARY KEY,
  claim_id VARCHAR(20) REFERENCES claims(claim_id),
  payment_date DATE,
  payment_amount DECIMAL(12, 2),
  payment_method VARCHAR(50)
);
