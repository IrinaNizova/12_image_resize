# Image Resizer

# How to install

```python
pip install -r requirement.txt
```

# How to start

```python
python image_resize.py <filepath> [options]
```
Where 'filepath' is path to file with image, options are:

-x --width <number> - new image width

-y --height <number> - new image height

-s --scale <number> - how many times to increase or decrease the image

-o --output <string> - path for new file

# Examples

python image_resize.py image.jpg -x 250
python image_resize.py image.jpg --width 250 --height 1000
python image_resize.py image.jpg -s 2 -o big_image.jpg


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
