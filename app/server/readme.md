# Set up a virtual environment instructions

### [1] Create the Workspace

1. First you will need to have Python installed. Download here if you don't have it *https://www.python.org/*.

2. Next you need to create a workspace directory for your Machine Learning code and datasets. 

   As an example, open a terminal and type the following commands (after the $ prompts):

   ```
   $ export ML_PATH="$HOME/ml" # You can change the path if you prefer
   $ mkdir -p $ML_PATH
   ```

3. You will need a number of Python modules: Jupyter, NumPy, Pandas, Matplotlib, and Scikit-Learn. There are many ways to install them (and their dependencies). You can use your system’s packaging system (e.g., apt-get on Ubuntu, or MacPorts or HomeBrew on MacOS), install a Scientific Python distribution such as Anaconda and use its packaging system, or just use Python’s own packaging system, pip, which is included by default with the Python binary installers (since Python 2.7.9). You can check to see if pip is installed by typing the following command:

```
$ python3 -m pip --version
pip 19.2.3 from /Users/jasonveljanoski/opt/anaconda3/lib/python3.7/site-packages/pip (python 3.7)
```

You should make sure you have a recent version of pip installed. To upgrade the pip module, type:

```bash
$ pip install -U pip # on macOS or Linux

$ python -m pip install -U pip # On Windows 
```

___



### [2] Creating an Isolated Environment

1. If you would like to work in an isolated environment (which is strongly recom‐ mended so you can work on different projects without having conflicting library versions), install virtualenv by running the following pip command (again, if you want virtualenv to be installed for all users on your machine, remove --user and run this command with administrator rights):

```bash
$ sudo pip install virtualenv
```

2. Now you can create an isolated Python environment by typing:

```bash
$ cd $ML_PATH # or to disired path
$ virtualenv env
```

3. Now every time you want to activate this environment, just open a terminal and type:

```bash
$ cd $ML_PATH
$ source env/bin/activate 	# on Linux or MacOSX 
$ .\env\Scripts\activate 		# on Windows
```

4. To deactivate this environment, just type `deactivate`.

While the environment is active, any package you install using pip will be installed in this isolated environment, and Python will only have access to these packages (if you also want access to the sys‐ tem’s packages, you should create the environment using virtualenv’s --system-site- packages option). 

Check out virtualenv’s documentation for more information: https://codefellows.github.io/sea-f2-python-sept14/supplements/virtualenv.html

___



### [3] Installing Modules for ML

1. Now you can install all the required modules and their dependencies using this simple pip command (if you are not using a virtualenv, you will need the --user option or administrator rights):

```bash
$ env/bin/python -m pip install --upgrade pip # update pip in THIS environment to be safe
$ pip install -U Flask Flask-Cors matplotlib numpy pandas scipy scikit-learn tensorflow # add others
```

2. To check your installation, try to import every module like this:

```bash
$ python3 -c "import Flask, Flask-Cors, matplotlib, numpy, pandas, scipy, sklearn" # add others
```

There should be no output and <u>no error</u>. 

___



### [bonus] Useful Commands

List all packages installed in the environment

```bash
$ pip list		# or, pip freeze (search the difference)
```

To export and import package versions and dependencies

```bash
$ pip freeze >> requirements.txt	# write list of packages in environment to .txt file

$ pip install -r requirements.txt	# install packages from a .txt
```

This is useful for step `[3]` if someone else has given you the dependencies for their project, for example.

___



# Basic Flask setup

```
server/
  nuxt-flask-venv/
  app/
    __init__.py
    routes.py
  oceanwaves.py
  .flaskenv
  readme.md
```

___



```python
# __init__.py
from flask import Flask

app = Flask(__name__)

from app import routes
```

The script above simply creates the application object as an instance of class `Flask` imported from the flask package. The `__name__` variable passed to the `Flask` class is a Python predefined variable, which is set to the name of the module in which it is used. Flask uses the location of the module passed here as a starting point when it needs to load associated resources such as template files, for example. Note, this project does not have any templates as nuxt acts as the templating engine.

The application then imports the `routes` module.

One aspect that may seem confusing at first is that there are two entities named `app`. The `app` package is defined by the *app* directory and the `__init__.py` script, and is referenced in the `from app import routes` statement. The `app` variable is defined as an instance of class `Flask` in the `__init__.py` script, which makes it a member of the `app` package.

Another peculiarity is that the `routes` module is imported at the bottom and not at the top of the script as it is always done. The bottom import is a workaround to *circular imports*, a common problem with Flask applications. You are going to see that the `routes` module needs to import the `app` variable defined in this script, so putting one of the reciprocal imports at the bottom avoids the error that results from the mutual references between these two files.

___



```python
# oceanwaves.py
from app import app
```

To complete the application, you need to have a Python script at the top-level that defines the Flask application instance. This is called `oceanwaves.py`, and define it as a single line that imports the application instance:

Remember the two `app` entities? Here you can see both together in the same sentence. The Flask application instance is called `app` and is a member of the `app` package. The `from app import app` statement imports the `app` variable that is a member of the `app` package. If you find this confusing, you can rename either the package or the variable to something else.

___



To run the application.

```bash
$ export FLASK_APP=microblog.py
$ flask run
```

Since environment variables aren't remembered across terminal sessions, you may find tedious to always have to set the `FLASK_APP` environment variable when you open a new terminal window. Starting with version 1.0, Flask allows you to register environment variables that you want to be automatically imported when you run the `flask` command. 

To use this option you have to install the *python-dotenv* package: `$ pip install python-dotenv`. You can then add the environment variable to a `.flaskenv` file.

```
# .flaskenv
FLASK_APP=oceanwaves.py
```

Now all you need to do is:

```bash
$ flask run
```



All other files and folders in this project should be self explainable with any intermediate knowledge of flask. The above will set you up with a "hello, world" flask application in which can be build upon. 

for more visit: `https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world`

