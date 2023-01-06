# Object-oriented and Function Programming with Python

## Setup

### Install Python3 using brew (macOS)
If you do not have brew installed visit this link [https://brew.sh/](https://brew.sh/)
```shell
brew install python3
```

### Install Python3 using Chocolatey (Windows)
If you do not have chocolatey installed visit this link [https://chocolatey.org/install](https://chocolatey.org/install)
```shell
brew install python3
```

### Install Python3 from the official page.
Visit [https://www.python.org/downloads/macos/](https://www.python.org/downloads/).


After the installation completes, check the python version (Note Python version should be > 3.0.0)
```shell
python3 -V
```

### Install virtualenv
A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them. [[1]](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi1gf-qwuz7AhWOSKQEHeDvC9UQFnoECBUQAw&url=https%3A%2F%2Fwww.geeksforgeeks.org%2Fpython-virtual-environment%2F&usg=AOvVaw2kPMPw1yz7bo7vEimkj7x6)
```shell
python3 -m pip install --user virtualenv
```

### Pull the repository and Checkout into the directory
You can pull the repository to any directory of your choice.
```shell
git clone https://github.com/Cmion/oofpp-habit-project.git
cd oofpp-habit-project
```

### Create and activate a virtual environment using `venv` (macOS)
```shell
python3 -m venv venv
source venv/bin/activate
```

### Create and activate a virtual environment using `venv` (Windows)
```shell
python3 -m venv venv
.\venv\Scripts\activate
```

Congratulations 🎉, you have successfully installed python,  venv, activated it. Now continue, just few more steps to go.

### To run the project you have to install the project dependencies.
A requirements.txt file has been provided in order to keep track of the projects dependencies and allow for easy installation.
```shell
pip install -r requirements.txt 
```

Yay!!  🎉 🎉, you have successfully installed the project's dependencies. Now let's run the app.

## Running the app

Make sure you're in the root project directory, then run the following command.

```shell
python3 main.py
```

The above command accepts a custom database parameter. Note that database file does not need to be created, passing any
string value to the command will automatically create a _.db_ file.

```shell
python3 main.py --database=my_custom_db.db
```

Or

```shell
python3 main.py -d my_custom_db.db
```

*Note: If you are running the app again after setup, make sure your virtual environment is activated using.

#### macOS

```shell
source venv/bin/activate
```

#### Windows

```shell
.\venv\Scripts\activate
```

## Test

The test command runs a simple unit test on the app classes and helper functions.

```shell
pytest test/
```

## Reference

GeeksforGeeks. (2022, November 25). Python Virtual Environment |
Introduction. https://www.geeksforgeeks.org/python-virtual-environment/ [1]



    
    
