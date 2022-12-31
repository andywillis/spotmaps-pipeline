# Film colour blueprints pipeline

Python / OpenCV pipeline to process films and extract their colour information.

## Requirements

* [Python](http://python.org/) - version ^3.0
* [Python Imaging Library](http://www.pythonware.com/products/pil/)
* [Numpy](http://sourceforge.net/projects/numpy/)
* [OpenCV](http://opencv.org/) - Ensure that you add the path of the OpenCV build module to your PYTHONPATH environment variable, for example: ;[root]\opencv\build\python\2.7;

## Preparation

* Convert your DVDs to AVI files.
* Rename the files so that they conform to the spotmap title style:  
	* Full Monty, The
	* Christmas Carol, A
	* Die Hard
* Use a text editor to
	* edit the getList.py file to point to the folder containing the films.
	* edit the spotmaps.py file to:
		* point to the folder containing the films
		* the handle/name of the contributor

## Procedure

* Run files in small batches of around 20.
* Run the getList.bat file to build a new list of processable files from the input folder. Note that due to the vagaries of openCV some files might be unreadable because of a format issue.
* Run the spotmaps.bat file to start the main process. Map, PNG and TIF files will be placed in the output folder.
* Zip up the files - including the processedFiles.txt file - and, depending on filesize, either:
	* attach the zip file to a new email to spotmaps@lavabit.com, or
	* put the zip file somewhere it can be downloaded and email spotmaps@lavabit.com with the download location
	
## Note

**Do not delete the processedFiles.txt file from the folder as this is added to and used with each new process.**
	
## Licence

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
