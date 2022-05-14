import os
import base64

wave_filename = 'sample.wav'
fd = open(wave_filename, 'rb')
bytes = fd.read()
fd.close()

b64text = base64.b64encode(bytes)
print(b64text)
rev = base64.b64decode(b64text)
assert(len(rev) == len(bytes))

base64_filename = 'sample_base64.txt'
fd = open(base64_filename, 'wb')
fd.write(b64text)
fd.close()

