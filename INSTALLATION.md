## Installation Instructions

#### UBUNTU

If you want to install from Git, make sure to install git itself. Skip this step if you've already installed it.

`sudo apt-get install git`

Once installed, you will need to close the taskhive repo.

`git clone –b alpha https://github.com/skifree-snowmonster/taskhive.git`

Python 3 is usually shipped with Ubuntu, you can check if you have it by using the following command:

`python3`

If it shows `command not found`, then proceed to install through

`sudo apt-get install python3` 

Then you need to make sure to install the pip package for python3. Use the following:

`sudo apt-get install –y python3-pip`

`pip3 install PyQt5`

`pip3 install psutil`

`pip3 install ecdsa`

`pip3 install sqlalchemy`

`pip3 install pyaes`

`pip3 install pbkdf2`

Once you've finished installing the aformentioned libraries, you should be ready to go. You can open taskhive by navigating through the console to the taskhive folder then executing with:

`python3 taskhive.py`


####Windows

First of all make sure to install python 3.5+, you can download it [here.](https://www.python.org/downloads/)

Make sure to tick the box that says ADD PYTHON TO $PATH on its installer.

If it's installed correctly, an interactive version should show once you execute it through the console:


`python`, if Python 3 is the only version of Python installed, otherwise use the launcher syntax, `py -3`


The windows python distribution comes with pip already installed. Therefore, all you need to do is to install the libraries through pip.


`pip3 install PyQt5`

`pip3 install psutil`

`pip3 install ecdsa`

`pip3 install sqlalchemy`

`pip3 install pyaes`

`pip3 install pbkdf2`

Once installed, you can either clone the alpha branch from the repo with git using 
`git clone –b alpha https://github.com/skifree-snowmonster/taskhive.git` or download it the entire source from the github website.
