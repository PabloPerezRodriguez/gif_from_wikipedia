from mwclient import Site
from get_img_history import get_img_history
from download_url import download_url
from img_processing import svg2png
import imageio
import os

# Change this
IMAGE_FILE = 'World_laws_pertaining_to_homosexual_relationships_and_expression.svg'
OUT_WIDTH, OUT_HEIGHT = (1920, 1088)

img_history = list(get_img_history(IMAGE_FILE))


print(f'Downloading {len(img_history)} images')
dir_ = './images'

if not os.path.exists(dir_):
  os.makedirs(dir_)

i = 1

writer = imageio.get_writer('movie.mp4', fps=30)

for img_ordered in reversed(img_history):
  img = dict(img_ordered)

  png_ext_file = f'f{i}.png'
  png_path = os.path.join(dir_, png_ext_file)

  if not os.path.exists(png_path):
    print(f'[{i}] downloading...', end='', flush=True)
    path = download_url(img['url'], filebasename=f'f{i}', folder=dir_)
    print(f'done')

    if path.endswith('.svg'):
      print(f'[{i}] processing (svg2png)...', end='', flush=True)

      svg2png(path, png_path, desired_width=OUT_WIDTH, desired_height=OUT_HEIGHT)
      print('done')
      print(f'[{i}] adding image to writer... ', end='', flush=True)
      writer.append_data(imageio.imread(png_path))
      print('done')
    elif path.endswith('.png'):
      print(f'[{i}] adding image to writer... ', end='', flush=True)
      writer.append_data(imageio.imread(path))
      print('done')
  elif os.path.exists(png_path):
    print(f'[{i}] already downloaded')
    print(f'[{i}] adding image to writer... ', end='', flush=True)
    writer.append_data(imageio.imread(png_path))
    print('done')
  i += 1

print('closing writer... ', end='')
writer.close()
print(f'done.')