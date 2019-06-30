from mwclient import Site

def get_img_history(image_file):
  ua = 'gif_from_wikimedia/0.1 https://github.com/pablo/gif_from_wikipedia'
  site = Site('en.wikipedia.org', clients_useragent=ua)

  file = site.images[image_file]
  img_history = file.imagehistory()

  return img_history

