from app.schemas.users_schema import UserSchema

# def fake_decode_token(token):
#     return UserSchema(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )
def fake_hash_password(password: str):
    return "fakehashed" + password
