import os.path
import argparse
import logging
from PIL import Image

logging.basicConfig(level=logging.WARNING)


def get_size(im_width, im_height, width=None, height=None, scale=None):
    if scale:
        new_width = im_width * scale
        new_height = im_height * scale
    elif width and not height:
        new_width = width
        new_height = im_height * (width/im_width)
    elif not width and height:
        new_width = im_width * (height/im_height)
        new_height =  height
    else:
        new_width = width
        new_height = height
        if round(new_width/im_width, 2) != round(new_height/im_height, 2):
            logging.warning('At the length and width specified by you, '
                  'the proportions do not match')
    return int(new_width), int(new_height)


def check_resize_possible(filepath, width=None, height=None, scale=None):
    if not width and not height and not scale:
        raise AttributeError('Need to width or scale to resize')
    if (width or height) and scale:
        raise AttributeError('You wrote width and scale together. '
                             'It is unacceptable')
    if not os.path.exists(filepath):
        raise IOError('There is no file in the path {}'.format(filepath))
    if os.path.splitext(filepath)[1].lower() not in \
            ('.jpg', '.png', '.jpeg', '.gif', '.tiff'):
        raise TypeError('This file is not a picture')


def resize_image(filepath, output=None, width=None, height=None, scale=None):
    im = Image.open(filepath)
    im_width, im_height = im.size
    new_width, new_height = get_size(im_width, im_height, width, height, scale)
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
    path, suffix = os.path.splitext(filepath)
    if output:
        output_name = output
    else:
        output_name = "".join([path, "__{}*{}".format(new_width, new_height), suffix])
    im.save(output_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filepath', type=str, help='path to source file')
    parser.add_argument('-x', '--width', type=int, required=False)
    parser.add_argument('-y', '--height', type=int, required=False)
    parser.add_argument('-s', '--scale', type=float, required=False,
                        help='how many times increase the image')
    parser.add_argument('-o', '--output', type=str, required=False,
                        help='path to result file')

    script_args = parser.parse_args()
    filepath = script_args.filepath
    width = script_args.width
    height = script_args.height
    scale = script_args.scale
    output = script_args.output

    check_resize_possible(filepath, width, height, scale)
    resize_image(filepath, output, width, height, scale)
