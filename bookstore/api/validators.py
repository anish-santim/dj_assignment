import jsonschema
import re


def validate_email(email):
    # Regular expression pattern for validating email addresses
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False


def validate_manage_category_delete_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string",  "minLength": 1}
        },
        "required": ["name"],
        "additionalProperties": False
    }

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"manage_category_delete_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e}")


def validate_manage_category_post_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1}
        },
        "required": ["name"],
        "additionalProperties": False
    }

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"manage_category_post_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e}")


def validate_manage_category_put_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "old_name": {"type": "string",  "minLength": 1},
            "new_name": {"type": "string",  "minLength": 1}
        },
        "required": ["old_name", "new_name"],
        "additionalProperties": False
    }

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"manage_category_put_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e}")


def validate_manage_books_put_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "category": {"type": "string", "minLength": 1},
            "title": {"type": "string", "minLength": 1},
            "author_name": {"type": "string", "minLength": 1},
            "price": {"type": "number"},
            "stock": {"type": "integer"},
            "year_published": {"type": "integer"}
        },
        "required": ["id", "category", "title", "author_name", "price", "stock", "year_published"],
        "additionalProperties": False
    }

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"manage_books_post_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e.message}")


def validate_manage_books_post_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "category": {"type": "string", "minLength": 1},
            "title": {"type": "string", "minLength": 1},
            "author_name": {"type": "string", "minLength": 1},
            "price": {"type": "number"},
            "stock": {"type": "integer"},
            "year_published": {"type": "integer"}
        },
        "required": ["category", "title", "author_name", "price", "stock", "year_published"],
        "additionalProperties": False
    }

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"manage_books_post_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e.message}")


def validate_manage_books_delete_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "minLength": 1}
        },
        "required": ["title"],
        "additionalProperties": False
    }

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"manage_books_delete_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e.message}")


def validate_book_list_get_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "categories": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["categories"],
        "additionalProperties": False

    }

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"book_list_get_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e.message}")


def validate_post_login_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "password": {"type": "string", "minLength": 1},
        },
        "required": ["email", "password"],
        "additionalProperties": False
    }

    try:
        jsonschema.validate(payload, schema)
        if not validate_email(payload['email']):
            raise ValueError("Invalid email")
    except jsonschema.ValidationError as e:
        if 'email' in e.path:
            raise ValueError("Invalid email")
        else:
            raise ValueError(
                f"post_login_payload validation error: {e.message}")
    except jsonschema.SchemaError as e:
        raise ValueError(f"Schema validation error: {e.message}")
