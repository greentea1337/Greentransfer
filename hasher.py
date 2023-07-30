# hasher.py

import hashlib 

def hash_chunk(data):
  hasher = hashlib.sha256()
  hasher.update(data)
  return hasher.hexdigest()