import subprocess

# This is no longer needed because of inkscape, but I leave it here in case I need to use it for
# something like using cairosvg again in the future.
#
# import svgutils.transform as st
# import svgutils.compose as sc
# import re
#
#
# reg = re.compile(r'(.\d)(px)')  # regex to search numbers with "px"
#
#
# def resize_svg(input_file, desired_height, desired_width):
#   print(f'Resizing {input_file}')
#   with open(input_file, 'r+') as f:
#     svg_str = f.read()
#     svg_str = reg.sub(r'\1', svg_str)  # Remove 'px' because svgutils chokes on them
#
#     svg_transform = st.fromstring(svg_str)
#     # Sometimes height and width are None for some strange reason 🤷‍
#     height = svg_transform.height
#     if height is None:
#       raise ValueError('Height is NoneType')
#     height = float(height)
#
#     width = svg_transform.width
#     if width is None:
#       raise ValueError('Width is NoneType')
#     width = float(width)
#
#     original_svg = sc.SVG(input_file)
#     x_scale_factor = desired_width / width
#     y_scale_factor = x_scale_factor  # <- Use this if you want images to retain their original aspect ratio
#     # y_scale_factor = desired_height / height  # <- Use this if you want to stretch images
#     original_svg.scale_xy(x=x_scale_factor, y=y_scale_factor)
#
#     # Could be able to add text here (like the week in which the image was posted or something).
#
#     fig = sc.Figure(str(width*x_scale_factor), str(height*y_scale_factor), original_svg)
#
#     # I've got the same problem as https://stackoverflow.com/a/55866088
#     # But instead of scour, my problem is with cairosvg
#     # And instead of pt, my problem is with px
#
#     svg_str = fig.tostr().decode()  # svgutils delivers ascii byte strings.
#     svg_str = reg.sub(r'\1', svg_str)  # the incorrectly added "px" unit is removed here
#
#     f.seek(0)
#     f.write(svg_str)
#     f.truncate()


def svg2png(input_file, output_file, desired_height, desired_width):
  # I'd like to use CairoSVG but it fails with a 'CAIRO_STATUS_NO_MEMORY' on some files
  # (here's the stack trace https://pastebin.com/upvGqHx2)

  # cairosvg.svg2png(url=input_file, write_to=output_file, output_height=desired_height, output_width=desired_width)

  # So... now I'm using inkscape, and it seems to work
  args = [
    'inkscape',
    '--without-gui',
    '-f', input_file,
    '--export-area-page',
    '-w', str(desired_width),
    '-h', str(desired_height),
    f'--export-png={output_file}'
  ]

  proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = proc.communicate()
  exitcode = proc.returncode
  if exitcode != 0:
    raise BaseException(f'Inkscape exited with non-zero error code {exitcode}', out, err)

