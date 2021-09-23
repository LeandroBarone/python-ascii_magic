# ASCII Magic

Python package that converts images into ASCII art for terminals and HTML. Thanks to [Colorama](https://github.com/tartley/colorama) it's compatible with the Windows terminal. Code based on [ProfOak's Ascii Py](https://github.com/ProfOak/Ascii_py/).

## Changelog

**v1.6**: OOP functionality, to_file()

## Instalation

    pip install ascii_magic

## Basic usage

```python
import ascii_magic
my_art = ascii_magic.from_image_file('images/moon.jpg')
ascii_magic.to_terminal(my_art)
```

Result:

![ASCII Magic example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_moon.png)

# Available functions

## from_image_file()

Converts an image file into ASCII art.

```python
ascii_magic.from_image_file(
    path: str,
    columns: int = 120,
    width_ratio: float = 2.2,
    char: str = None,
    back: Back = None,
    mode: Modes = Modes.TERMINAL,
) -> str
```

- ```path```: a PIL-compatible file, such as a jpeg or png
- ```columns (optional)```: the number of characters per row, more columns = wider art
- ```width_ratio (optional)```: ASCII characters are not squares, so this adjusts the width to height ratio
- ```char (optional)```: instead of using many different ASCII glyphs, you can use a single one, such as '#'
- ```back (optional)```: In terminal mode, sets the background color with one of:
  - ```ascii_magic.Back.BLACK```
  - ```ascii_magic.Back.RED```
  - ```ascii_magic.Back.GREEN```
  - ```ascii_magic.Back.YELLOW```
  - ```ascii_magic.Back.BLUE```
  - ```ascii_magic.Back.MAGENTA```
  - ```ascii_magic.Back.CYAN```
  - ```ascii_magic.Back.WHITE```
- ```mode (optional)```: one of:
  - ```ascii_magic.Modes.TERMINAL```: outputs ASCII with terminal color codes (8 tones)
  - ```ascii_magic.Modes.ASCII```: outputs pure ASCII with no color codes, resulting in a "grayscale" image
  - ```ascii_magic.Modes.HTML_TERMINAL```: outputs HTML simulating terminal colors
  - ```ascii_magic.Modes.HTML```: as above, but with full color

Example:

```python
my_art = ascii_magic.from_image_file(
    'images/lion.jpg',
    columns=200,
    back=ascii_magic.Back.BLUE
)
ascii_magic.to_terminal(my_art)
```

Result:

![ASCII Magic TERMINAL mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_blue.png)

Example:

```python
my_art = ascii_magic.from_image_file(
    'images/lion.jpg',
    columns=200,
    width_ratio=2,
    mode=ascii_magic.Modes.HTML
)
ascii_magic.to_html_file('ascii_art.html', my_art)
```

Result:

![ASCII Magic HTML mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_html.png)

Example:

```python
my_art = ascii_magic.from_image_file(
    'images/lion.jpg',
    columns=200,
    mode=ascii_magic.Modes.ASCII
)
ascii_magic.to_terminal(my_art)
```

Result:

![ASCII Magic ASCII mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_ascii.png)

## from_url()

As above, but using the URL of an image. Raises an ```urllib.error.URLError``` if something goes wrong while requesting the image, but you can also catch it as an ```OSError``` if you don't want to import urllib to your project.

```python
ascii_magic.from_url(
    url: str,
    # same art creation settings as above
) -> str
```

- ```url```: an URL which will be loaded via urllib (supports redirects)

Example:

```python
try:
    my_art = ascii_magic.from_url('https://source.unsplash.com/800x600?nature', columns=100)
except OSError as e:
    print(f'Could not load the image, server said: {e.code} {e.msg}')
```

## from_clipboard()

As above, but with the contents of the clipboard. Raises a ```OSError``` if the clipboard doesn't contain an image.

Requires [PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html) under Linux.

```python
ascii_magic.from_clipboard(
    # same art creation settings as above
) -> str
```

Example:

```python
try:
    my_art = ascii_magic.from_clipboard(columns=100)
except OSError:
    print('The clipboard does not contain an image')
```

## from_image()

As above, but using an image loaded with Pillow.

```python
ascii_magic.from_image(
    img: Image,
    # same art creation settings as above
) -> str
```

- ```img```: PIL image object

Example:

```python
from PIL import Image
img = Image.open('images/lion.jpg')
my_art = ascii_magic.from_image(img, columns=100)
```

## init_terminal()

Initializes Colorama, which is required on Windows for displaying art in terminal mode. It's the same as doing ```colorama.init()```.

```python
ascii_magic.init_terminal() -> None
```

## to_terminal()

Initializes Colorama, which is required on Windows for displaying ASCII with color in terminal mode, and prints the art. It's the same as doing ```colorama.init()``` and then ```print(art)```.

```python
ascii_magic.to_terminal(
    art: str
) -> None
```

## to_file()

New in v1.6. Writes the art to a text file.

```python
ascii_magic.to_file(
    path: str,
    art: str
) -> None
```

## to_html_file()

Writes the art to a barebones HTML file inside a ```<pre>```.

```python
ascii_magic.to_html_file(
    path: str,
    art: str,
    styles: str = '...', # See description
    additional_styles: str = '',
    auto_open: bool = False
) -> None
```

- ```path```: The relative path and filename of the HTML file
- ```input```: The markup which will be included
- ```styles (optional)```: A string with a bunch of CSS styles for the ```<pre>``` element, by default:
  - display: inline-block;
  - border-width: 4px 6px;
  - border-color: black;
  - border-style: solid;
  - background-color: black;
  - font-size: 8px;
- ```additional_styles (optional)```: You can add your own styles without removing the default ones
- ```auto_open (optional)```: If True, ```webbrowser.open()``` will be called on the HTML file

example:

```python
my_art = ascii_magic.from_image_file('images/lion.jpg', mode=ascii_magic.Modes.HTML)
ascii_magic.to_html_file('lion.html', my_art, additional_styles='background: #222;')
```

## quick_test()

Runs ascii_magic with a random Unsplash picture with the default parameters and prints it to the terminal.

```python
ascii_magic.quick_test() -> None
```

# The AsciiArt object

New in v1.6. The following functions return an ```AsciiArt``` object: ```obj_from_url()```, ```obj_from_clipboard()```, ```obj_from_image_file()``` and ```obj_from_image()```.

An ```AsciiArt object``` has the following methods: ```to_terminal()```, ```to_file()``` and ```to_html_file()```. These methods work as their non-oop counterparts described above and, in addition, they accept the same art settings as ```from_image_file()``` (path, columns, width_ratio, etc).

OOP example:

```python
my_art_obj = ascii_magic.obj_from_url('https://source.unsplash.com/800x600?nature')
my_art_obj.to_html_file(
    'ascii_art.html',
    columns=200,
    char="@",
    additional_styles='background: #222;'
)
```

## obj_from_url()

Takes the URL of an image and returns an ```AsciiArt``` object.

```python
ascii_magic.obj_from_url(
    url: str
) -> AsciiArt
```

## obj_from_clipboard()

As above, but with the clipboard. Check ```from_clipboard()``` for more information.

```python
ascii_magic.obj_from_clipboard() -> AsciiArt
```

## obj_from_image_file()

As above, but with the path of an image file.

```python
ascii_magic.obj_from_image_file(
    file_path: str
) -> AsciiArt
```

## obj_from_image()

As above, but with an image loaded with PIL.

```python
ascii_magic.obj_from_image(
    img: Image
) -> AsciiArt
```

## AsciiArt.to_terminal()

Generates an ASCII art, initializes Colorama and prints it to the terminal. All arguments are keyword arguments. Check ```from_image_file()``` for more details about these art creation settings (columns, char, width_ratio, etc).

```python
my_art_obj.to_terminal(
    columns: int = 120,
    width_ratio: float = 2.2,
    char: str = None,
    back: Back = None,
    mode: Modes = Modes.TERMINAL,
) -> None
```

## AsciiArt.to_file()

Generates an ASCII art and prints it to a text file. All arguments except file_path are keyword arguments.

```python
my_art_obj.to_file(
    file_path: str,
    # same art creation settings as above
) -> None
```

## AsciiArt.to_html_file()

Generates an ASCII art and prints it to an HTML file. All arguments except file_path are keyword arguments. Check the non-OOP version of this function for more details.

```python
my_art_obj.to_html_file(
    file_path: str,
    styles: str = '...', # see the non-OOP version
    additional_styles: str = '',
    auto_open: bool = False
    # same art creation settings as above
) -> None
```

# Licence

Copyright (c) 2020 Leandro Barone.

Usage is provided under the MIT License. See LICENSE for the full details.