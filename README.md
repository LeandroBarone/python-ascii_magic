# ASCII Magic

Python package that converts images into ASCII art for terminals and HTML. Thanks to Colorama it's compatible with the Windows terminal. Code based on [ProfOak's Ascii Py](https://github.com/ProfOak/Ascii_py/).

![ASCII Magic example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example.png)

## Basic usage

```python
import ascii_magic
output = ascii_magic.from_image_file('picture.jpg')
ascii_magic.to_terminal(output)
```

# Available functions

## from_image_file()

Converts an image file into ASCII art with terminal color codes.

```python
from_image_file(
    path: str,
    columns: int = 120,
    width_ratio: float = 2,
    char: str = None,
    mode: Modes = Modes.TERMINAL,
) -> str
```

- path => a PIL-compatible file, such as a jpeg or png
- columns (optional) => the number of characters per row, more columns = wider art
- pixel_width (optional) => ASCII characters are not squares, so this adjusts the width to height ratio
- char (optional) => instead of using many different ASCII glyphs, you can use a single one, such as '#'
- mode (optional) => one of:
  - ```ascii_magic.Modes.TERMINAL```  => outputs ASCII with terminal color codes
  - ```ascii_magic.Modes.HTML_TERMINAL``` => outputs HTML that simulates terminal colors; just wrap it inside a ```<pre>```
  - ```ascii_magic.Modes.HTML``` => as above, but with full color

Example:

```python
ascii_magic.from_image_file(
    'images/lion.jpg',
    columns=200,
    mode=ascii_magic.Modes.HTML
)
```

Result:

![ASCII Magic HTML mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion.png)

## from_url()

As above, but using the URL of an image.

```python
from_url(
    url: str,
    # ... as above
) -> str
```

- url => an URL which will be loaded via urllib (supports redirects)

Example:

```python
img_url = 'https://source.unsplash.com/800x600?nature'
ascii_art = ascii_magic.from_url(img_url, columns=100)
```

## from_image()

As above, but using an image loaded with Pillow.

```python
from_image(
    img: Image,
    # ... as above
) -> str
```

- img => PIL image object

Example:

```python
from PIL import Image
with Image.open('images/1.jpg') as img:
    ascii_art = ascii_magic.from_image(img, columns=100)
```

## to_terminal()

Initializes Colorama (which is required on Windows) and prints ASCII art to the terminal. It's the same as doing ```colorama.init()``` before printing normally.

```python
to_terminal(ascii_art: str) -> None
```

# Licence

Copyright (c) 2020 Leandro Barone.

Usage is provided under the MIT License. See LICENSE for the full details.