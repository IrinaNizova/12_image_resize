import os.path
import argparse
from PIL import Image


def get_size(parser, width, height):
    args = parser
    if args.scale:
        new_width = width * args.scale
        new_height = height * args.scale
    elif args.width and not args.height:
        new_width = args.width
        new_height = height * (args.width/width)
    elif not args.width and args.height:
        new_width = width * (args.height/height)
        new_height = args.height
    else:
        new_width = args.width
        new_height = args.height
        if new_width/width != new_height/height:
            print('At the length and width specified by you, '
                  'the proportions do not match')
    return int(new_width), int(new_height)


def check_resize_possible(script_args):
    if not ('width' in script_args or 'scale' in script_args):
        raise AttributeError('Need to width or scale to resize')
    if script_args.width and script_args.scale:
        raise AttributeError('You wrote width and scale together. It is unacceptable')
    file_path = script_args.filepath
    if not os.path.exists(file_path):
        raise IOError('There is no file in the path {}'.format(file_path))
    if os.path.splitext(file_path)[1].lower() not in \
            ('.jpg', '.png', '.jpeg', '.gif', '.tiff'):
        raise TypeError('This file is not a picture')


def resize_image(script_args):
    im = Image.open(script_args.filepath)
    width, height = im.size
    new_width, new_height = get_size(script_args, width, height)
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
    path, suffix = os.path.splitext(script_args.filepath)
    if script_args.output:
        output_name = script_args.output
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
    check_resize_possible(script_args)
    resize_image(script_args)
