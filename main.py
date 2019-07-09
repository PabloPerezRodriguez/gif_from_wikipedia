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
img_history = [dict(img) for img in img_history]
img_history = img_history[::-1]

print(f'History length: {len(img_history)} images')
print('Cleaning up images in between reverts...', end='', flush=True)
# Clean up images in between reverts
image_hashes = []
cleaned_up_img_history = []
for i in range(len(img_history)):
  img = img_history[i]
  hash = img['sha1']

  if hash in image_hashes:
    # Found an image this image reverted to
    hash_idx = image_hashes.index(hash)
    # Remove images from the hash forwards
    image_hashes = image_hashes[:hash_idx]
    cleaned_up_img_history = cleaned_up_img_history[:hash_idx]

  image_hashes.append(hash)
  cleaned_up_img_history.append(img)
print('done')

print(f'Cleaned up length: {len(cleaned_up_img_history)} images')
dir_ = './images'

if not os.path.exists(dir_):
  os.makedirs(dir_)

i = 1

writer = imageio.get_writer('movie.mp4', fps=30)

for img in cleaned_up_img_history:
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