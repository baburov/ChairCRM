from __future__ import annotations

from typing import NamedTuple


class UserQueries(NamedTuple):
    """Queries related to User operations."""
    get_by_login_pswd: str = """
        SELECT *
        FROM Manager
        WHERE login = $1 AND password = $2
    """
    
    get_by_role: str = """
        SELECT id, fio, contacts, bonus
        FROM Manager
        WHERE role ILIKE '%' || $1 || '%'
    """
    
    get_by_fio: str = """
        SELECT id, fio, contacts, bonus
        FROM Manager
        WHERE fio ILIKE '%' || $1 || '%'
    """
    
    get_all_users: str = "SELECT id, fio, contacts, bonus FROM Manager"
    
    add_user: str = """
        INSERT INTO Manager (fio, contacts, bonus, login, password, role)
        VALUES ($1, $2, $3, $4, $5, $6)
    """


class ClientQueries(NamedTuple):
    """Queries related to Client operations."""
    get_by_order: str = """
        SELECT c.id, c.fio, c.phone_number
        FROM Client c
        JOIN Order_ o ON o.client_id = c.id
        WHERE o.id = $1
    """
    
    get_all: str = "SELECT id, fio, phone_number FROM Client"
    
    get_by_params: str = """
        SELECT id, fio, phone_number
        FROM Client
        WHERE fio ILIKE '%' || $1 || '%'
    """


class OrderQueries(NamedTuple):
    """Queries related to Order operations."""
    insert: str = """
        INSERT INTO Order_ (client_id, creation_date, status, total)
        VALUES ($1, $2, $3, $4)
    """
    
    get_by_owner: str = """
        SELECT id, client_id, creation_date, status, total
        FROM Order_
        WHERE client_id = $1
    """


class ItemQueries(NamedTuple):
    """Queries related to Item operations."""
    get_by_params: str = """
        SELECT id, name, price, stock
        FROM Product
        WHERE name ILIKE '%' || $1 || '%'
    """


class InteractionQueries(NamedTuple):
    """Queries related to Interaction operations."""
    get_by_user: str = """
        SELECT ih.id, ih.client_id, ih.date, ih.type, ih.details
        FROM InteractionHistory ih
        JOIN Interaction i ON i.client_id = ih.client_id
        WHERE i.manager_id = $1
    """
    
    get_by_client: str = """
        SELECT id, client_id, date, type, details
        FROM InteractionHistory
        WHERE client_id = $1
    """


user_queries = UserQueries()
client_queries = ClientQueries()
order_queries = OrderQueries()
item_queries = ItemQueries()
interaction_queries = InteractionQueries()