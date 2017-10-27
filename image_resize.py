import os.path
import argparse
import logging
from PIL import Image

logging.basicConfig(level=logging.WARNING)


def get_size(im_width, im_height, **kwargs):
    if kwargs['scale']:
        new_width = im_width * kwargs['scale']
        new_height = im_height * kwargs['scale']
    elif kwargs['width'] and not kwargs['height']:
        new_width = kwargs['width']
        new_height = im_height * (kwargs['width']/im_width)
    elif not kwargs['width'] and kwargs['height']:
        new_width = im_width * (kwargs['height']/im_height)
        new_height =  kwargs['height']
    else:
        new_width = kwargs['width']
        new_height = kwargs['height']
        if round(new_width/im_width, 2) != round(new_height/im_height, 2):
            logging.warning('At the length and width specified by you, '
                  'the proportions do not match')
    return int(new_width), int(new_height)


def check_resize_possible(**kwargs):
    if not kwargs['width'] and not kwargs['height'] and not kwargs['scale']:
        raise AttributeError('Need to width or scale to resize')
    if (kwargs['width'] or kwargs['height']) and kwargs['scale']:
        raise AttributeError('You wrote width and scale together. '
                             'It is unacceptable')
    if not os.path.exists(kwargs['filepath']):
        raise IOError('There is no file in the path {}'.format(kwargs['file_path']))
    if os.path.splitext(kwargs['filepath'])[1].lower() not in \
            ('.jpg', '.png', '.jpeg', '.gif', '.tiff'):
        raise TypeError('This file is not a picture')


def resize_image(**kwargs):
    im = Image.open(kwargs['filepath'])
    im_width, im_height = im.size
    new_width, new_height = get_size(im_width, im_height, **kwargs)
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
    path, suffix = os.path.splitext(kwargs['filepath'])
    if kwargs['output']:
        output_name = kwargs['output']
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
    check_resize_possible(**script_args.__dict__)
    resize_image(**script_args.__dict__)
