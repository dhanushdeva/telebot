from pocketbase import PocketBase

# Initialize PocketBase client
pb = PocketBase('http://127.0.0.1:8090')

# Authenticate
auth_data = pb.admins.auth_with_password('dhanushdeva212@gmail.com', 'radhamani1980')

# Access auth data from the authStore
# print(pb.auth_store.is_valid)
print(pb.auth_store.token)
print(pb.auth_store.model.id)

# "logout" the last authenticated account
pb.auth_store.clear()
