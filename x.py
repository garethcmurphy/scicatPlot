import base64
with open('phs.png', 'rb') as params_source:
    params = params_source.read()  # bytes object

params_encoded = base64.b64encode(params)
print(params_encoded.decode('utf8'))
