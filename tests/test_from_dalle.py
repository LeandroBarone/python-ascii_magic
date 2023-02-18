import ascii_magic

import os


def test_from_dalle():
    api_key = os.environ.get('DALLE_API_KEY')
    my_art = ascii_magic.from_dalle('A hyperrealistic portrait of a cow with noble clothes, digital art', api_key, True)
    my_art.to_html_file('test_dalle.html', columns=200)
