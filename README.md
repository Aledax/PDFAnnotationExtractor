# PDF Annotation Extractor (Windows)

This application extracts annotated text from PDF files using [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/).

### How To Use:

1. Clone the repository.
2. Make sure Python 3 is installed. (This application was built with ```3.13.1```)
3. Make sure the required libraries, listed in ```requirements.txt```, are installed in your current environment.
4. In the repository root, create a two-layer directory ```user/input/```.
5. Suppose your PDF's name is ```annotated.pdf```. Place it inside your newly created ```user/input/``` directory.
6. From the repository root, run ```py main.py annotated```, where ```annotated``` is the name of your PDF **WITHOUT** the ```.pdf``` extension.
7. If you get the message ```Complete. Press Enter to continue...```, look for the extracted ```.txt``` output in ```user/output/```.
