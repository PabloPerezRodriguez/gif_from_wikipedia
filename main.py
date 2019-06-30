from mwclient import Site
from get_img_history import get_img_history
from download_url import download_url
from img_processing import process_svg
import imageio
import os

# Change this
IMAGE_FILE = 'World_laws_pertaining_to_homosexual_relationships_and_expression.svg'

img_history = list(get_img_history(IMAGE_FILE))

print(f'Downloading {len(img_history)} images')
dir_ = './images'

if not os.path.exists(dir_):
  os.makedirs(dir_)

i = 1

writer = imageio.get_writer('movie.gif')

for img_ordered in img_history:
  img = dict(img_ordered)
  png_ext_file = f'f{i}.png'
  png_path = os.path.join(dir_, png_ext_file)
  print(os.path.exists(png_path))
  if not os.path.exists(png_path):
    print(f'downloading image n{i}')

    # todo: use svgo to clean up svg files
    path = download_url(img['url'], filebasename=f'f{i}', folder=dir_)
    print(f'downloaded {path}')
    if path.endswith('.svg'):
      print(f'processing (svg2png)...')
      dest = f'{path[:-4]}.png'
      process_svg(path, dest)
    
      print(f'adding image to writer')
      writer.append_data(imageio.imread(dest))
    elif path.endswith('.png'):
      print(f'adding image to writer')
      writer.append_data(imageio.imread(path))
  elif os.path.exists(png_path):
    print(f'Already downloaded image n{i}, adding it to writer')
    writer.append_data(imageio.imread(png_path))
  i += 1
  print(f'done.')

print(f'closing writer...')
writer.close()
print(f'finished.')