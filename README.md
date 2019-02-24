## ROV 2019 Code
_Developed by Mahmoud T Soltan for his ROV team._

### Usage Instructions
This is a work in progress.

There is a python virtual environment in .../src/python, where ... is
the repository path. Please set one up, with cv2 and numpy installed
before using the project.

All *.less files are compiled to *.min.css and *.min.css.map files,
which are also git ignored. Please make sure you have an environment
set up to process *.less files.


Finally, please download openh264-1.8.0-win64.dll (or the respective
openh264 library on linux systems), and place it inside .../src/python.

To check that all classes are working properly, run their respective
test scripts.
To run the code, consider running FitTogether_test, which tests all
the components fit together, until the main code is finished and a
production-ready version is made.

### Licence
This code is licensed under GNU General Public License v3, the full
text of which is available at https://www.gnu.org/licenses/gpl-3.0.txt.

If this code is used for future competition purposes, however,
you are legally obliged to clarify this to the judges for fair
judging purposes.
