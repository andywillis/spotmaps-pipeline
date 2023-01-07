# Spotmaps pipeline

Python / OpenCV pipeline to process films and extract their colour information.

## Requirements

* [Python](http://python.org/) - version ^3.10.0
* [Poetry](https://python-poetry.org/) - package management
* [Pillow](https://pillow.readthedocs.io/en/latest/index.html)
* [Numpy](https://numpy.org/)
* [OpenCV](http://opencv.org/)

# Installing and running the pipeline

- Clone the repo
- `cd spotmaps-pipeline`
- `poetry install`

Add film files to the `files\input` folder.

- `poetry shell`
- `py src/main.py`

## Licence

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
