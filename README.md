# Hanzi Worksheets

Use the public generator at https://vlligo.github.io/hanzi-worksheets/ — no installation or file downloads are required. Enter your characters, generate a preview, then choose **Open PDF / Print** to view the PDF in a browser tab and print it. Browser PDF handling depends on your device and browser settings.

Cross and diagonal guides are selected by default. All worksheet generation happens locally in your browser; entries are not uploaded to a server. The site bundles stroke data and its annotation font without external runtime dependencies.

For offline use, you can optionally open `hanzi-worksheets.html` locally. `index.html` is the same standalone generator, published through GitHub Pages.

Enter one word or group per line. Pinyin and English definitions are optional. The worksheet prints pinyin with accent marks and converts numbered tones automatically.

```text
学习 | xue2xi2 | to study
人
中文 | | Chinese language
```

## Rebuild

Run these commands from this directory with Python 3.10 or later.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py
```

`template.html` contains the worksheet interface and PDF code. The build embeds 9,574 characters from Hanzi Writer Data 2.0.1, consolidated as stroke outlines in `data/strokes.json`, and the bundled DejaVu Sans font. It also embeds the vector logo from `chinlearn-brand-mark.xml`, copied from the Chinlearn Android app. License notices are in `data/licenses.json` and `DejaVuSans-LICENSE.txt` and are included in the generated HTML.

## Hosting

GitHub Pages serves the repository root on the `main` branch. Run `build.py` after changing the template or assets; it updates both HTML entry points. Commit both outputs to update the public site.
