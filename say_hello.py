import os

HOSTNAME = os.environ.get('HOSTNAME')

print("Hello, It's me, I'm running on host %s" % HOSTNAME)
