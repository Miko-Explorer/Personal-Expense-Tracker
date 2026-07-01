#Highest amount spent in different expense categories:
CREATE VIEW high_expense_based_cat 
AS SELECT user_id, category, MAX(amount_spent)
AS Max_Amount 
FROM expenses
GROUP BY user_id, category; 

#Lowest amount spent in different expense categories:
CREATE VIEW low_expense_based_cat
AS SELECT user_id, category, MIN(amount_spent)
AS Min_Amount
FROM expenses
GROUP BY user_id, category; 

#Highest amount paid in different payment methods:
CREATE VIEW high_amount_paid_based_paymethod 
AS SELECT user_id, payment_method, MAX(amount_spent)
AS Max_Amount
FROM expenses
GROUP BY user_id, payment_method; 

#Lowest amount paid in different payment methods: 
CREATE VIEW low_amount_paid_based_paymethod
AS SELECT user_id, payment_method, MIN(amount_spent)
AS Min_Amount 
FROM expenses
GROUP BY user_id, payment_method; 

#Recently created expenses/transactions: 
CREATE VIEW latest_created_expense
AS SELECT payment_method, created_at 
AS Expense_recently_created_at
FROM expenses
ORDER BY created_at DESC
LIMIT 10; 

#Outdated expenses/transactions: 
CREATE VIEW outdated_created_expense
AS SELECT payment_method, created_at 
AS Expense_outdated_created_at
FROM expenses
ORDER BY created_at ASC
LIMIT 30; 

#Recently updated expenses/transactions:
CREATE VIEW recently_updated_expense
AS SELECT payment_method, updated_at
AS Expense_recently_updated_at
FROM expenses
ORDER BY updated_at DESC; 

#Expenses/transactions that have not yet updated:
CREATE VIEW not_updated_expense
AS SELECT payment_method, updated_at
AS Expense_not_updated_at
FROM expenses
ORDER BY updated_at ASC; 

#Overall total amount spent:
CREATE VIEW total_amount_spent 
AS SELECT user_id, SUM(amount_spent)
AS Total_amount_spent 
FROM expenses
GROUP BY user_id; 

#Average amount spent based on expense category:
CREATE VIEW average_amount_spent_based_cat
AS SELECT user_id, category, AVG(amount_spent)
AS Average_spent
FROM expenses
GROUP BY user_id, category; 

#Average amount paid based on payment method:
CREATE VIEW average_amount_spent_based_paymethod
AS SELECT user_id, payment_method, AVG(amount_spent)
AS Average_paid
FROM expenses
GROUP BY user_id, payment_method; 

#Total amount paid based on payment method:
CREATE VIEW total_amount_paid_based_paymethod
AS SELECT user_id, payment_method, SUM(amount_spent)
AS Total_amount_paid 
FROM expenses
GROUP BY user_id, payment_method; 

#Total amount spent based on expense category:
CREATE VIEW total_amount_spent_based_cat
AS SELECT user_id, category, SUM(amount_spent)
AS Total_amount_spent
FROM expenses
GROUP BY user_id, category; 

#Total entries/expenses made:
CREATE VIEW total_entries
AS SELECT COUNT(id)
AS Total_entries 
FROM expenses; 

#Display records:
SELECT * FROM high_expense_based_cat; 
SELECT * FROM low_expense_based_cat; 
SELECT * FROM high_amount_paid_based_paymethod; 
SELECT * FROM low_amount_paid_based_paymethod; 
SELECT * FROM latest_created_expense; 
SELECT * FROM outdated_created_expense; 
SELECT * FROM recently_updated_expense; 
SELECT * FROM not_updated_expense; 
SELECT * FROM total_amount_spent; 
SELECT * FROM average_amount_spent_based_cat; 
SELECT * FROM average_amount_spent_based_paymethod; 
SELECT * FROM total_amount_paid_based_paymethod; 
SELECT * FROM total_amount_spent_based_cat; 
SELECT * FROM total_entries;