import requests

url = 'https://download.Example.zip' # insert the link
r = requests.get(url, allow_redirects=True)
open('Example.zip', 'wb').write(r.content)
