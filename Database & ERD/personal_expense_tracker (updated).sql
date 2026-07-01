#Create database to store expenses:
CREATE DATABASE expense_db; 

#Set database to default schema:
USE expense_db;

#Table for user information:
CREATE TABLE users(
	 id INT AUTO_INCREMENT PRIMARY KEY, 
   username VARCHAR(100) NOT NULL UNIQUE, 
   email VARCHAR(100) NOT NULL UNIQUE, 
   passwords VARCHAR(255) NOT NULL, 
   created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP()),
   CONSTRAINT chk_created_at_users CHECK(created_at BETWEEN '1970-01-01 00:00:01' AND '2038-01-19 03:14:07')
);

#Table for user's expenses:
CREATE TABLE expenses(
	id INT AUTO_INCREMENT PRIMARY KEY, 
  user_id INT NOT NULL, 
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE, 
  amount_spent DECIMAL(7,2) NOT NULL, 
  CONSTRAINT chk_amount_spent CHECK(amount_spent BETWEEN 00000.00 AND 50000.00), 
  category ENUM('Food', 'Transport', 'Utilities', 'Subscription', 
  'Health', 'Work', 'School', 'Entertainment', 'Insurance', 'Miscellaneous') NULL DEFAULT NULL, 
  description VARCHAR(500) NULL DEFAULT NULL, 
  dates DATE NOT NULL DEFAULT (CURRENT_DATE()), 
  CONSTRAINT chk_dates CHECK(dates BETWEEN '1000-01-01' AND '9999-12-31'), 
  payment_method ENUM('Debit', 'Credit', 'Cash', 'Online Payment') NULL DEFAULT NULL, 
  location VARCHAR(100) NULL DEFAULT NULL, 
  created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP()),
  CONSTRAINT chk_created_at_exp CHECK(created_at BETWEEN '1970-01-01 00:00:01' AND '2038-01-19 03:14:07'), 
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP()
); 

#Display records: 
SELECT * FROM users; 
SELECT * FROM expenses; 

#Describe table characteristics:
DESCRIBE users;
DESCRIBE expenses;