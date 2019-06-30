import requests, shutil

from urllib import parse as urlparse
import os
from pathlib import Path

def download_url(url, filebasename=None, folder=None):
  usr_path = urlparse.urlparse(url).path
  url_filename = os.path.basename(usr_path)
  filename = ''
  if filebasename is None:
    filename = url_filename
  else:
    ext = Path(url_filename).suffix
    filename = filebasename + ext

  if folder is None:
    folder = '.'
    

  path = os.path.join(folder, filename)

  response = requests.get(url, stream=True)
  with open(path, 'wb') as f:
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, f)

  return path