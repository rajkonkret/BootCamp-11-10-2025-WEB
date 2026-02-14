import secrets

print(secrets.token_urlsafe(32))
# mnoRQTKSk6v0hXJUBKrmBff_PgmoLrjWzCLzrYphJFg

print(secrets.token_urlsafe(48)) # ten dla HS256
# dLMeqQ6XRrmxrb8A9e0vYSwQcJzqGL5tDC7G0DRZ6UbfdnKRLtb89MH0JJx1PpiX

print(secrets.token_urlsafe(64))
# nFgdYlFSx9c7h6kZkFBKnkwKZuhg1ueo6u3MsPIuuG1k3hdlvyV3E5HSQZW5Y52R4tFB6uvx7mtERC_i5Q9S7A