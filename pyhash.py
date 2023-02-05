from hashlib import sha1
import os

email = os.environ["email"]


print(sha1(email.lower().encode("utf-8")).hexdigest())
