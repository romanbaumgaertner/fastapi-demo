CREATE TABLE IF NOT EXISTS employee (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    department VARCHAR(200) NOT NULL,
    dob DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name),
    UNIQUE (employee_id)
);
