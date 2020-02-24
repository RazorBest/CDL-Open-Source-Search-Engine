# Open Source Search Engine

A basic tool that finds documents based on simple logic-structured queries.

## Getting started

To run this project you'll need Python 3.6.9 an Ubuntu 18.04.
You'll need the next python packages
```
bitstring==3.1.6
wxPython==4.0.7.post2
```
The installer will try to download the above packages.

### Installing
Clone the project:
 ```
 $ git clone https://github.com/RazorBest/CDL-Open-Source-Search-Engine
 
 ```
You can install Python from here: https://www.python.org/

#### Automatic installation
You can install the package with
```
$ sudo ./install.sh
```
If the script fails, you'll need to install the package manually.


You can install a package with pip like this:
```
$ pip3 install bitstring
```
  to install the latest version, or like this:
 ```
 $ pip3 install -Iv bitstring==3.1.6
 ```
  to install a specific version.
  
To install wxPython, use:
```
$ pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/ wxPython
```
Or find the correpsonding wheel for your OS.
  
 

## Running the tests
To run a "test_file.py" use:
  ```
  python -m unittest tests/[test_file.py]
  
  ```

## Documentation
Open Source Search Engine is a preselection project used for CDL. The problem description (in Romanian) is in CDL.pdf.
