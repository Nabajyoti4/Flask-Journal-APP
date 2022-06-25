from project import ma


# -------
# Schemas
# -------

class NewUserSchema(ma.Schema):
    """Schema defining the attributes when creating a new user."""
    email = ma.String()
    password_plaintext = ma.String()


class UserSchema(ma.Schema):
    """Schema defining the attributes of a user."""
    id = ma.Integer()
    email = ma.String()


class TokenSchema(ma.Schema):
    """Schema defining the attributes of a token."""
    token = ma.String()


new_user_schema = NewUserSchema()
user_schema = UserSchema()
token_schema = TokenSchema()
