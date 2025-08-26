# Simple centralization of SQL snippets (can be imported by other scripts)
GET_CUSTOMER_BY_IBAN = """
SELECT customers.id, customers.name FROM customers
JOIN accounts ON accounts.customer_id = customers.id
WHERE accounts.iban = %s LIMIT 1;
"""

GET_CUSTOMER_ADDRESSES = """
SELECT address_type, name, line1, line2, postal_code, city, country FROM addresses WHERE customer_id = %s;
"""

GET_CUSTOMER_ACCOUNTS = "SELECT iban FROM accounts WHERE customer_id = %s;"
