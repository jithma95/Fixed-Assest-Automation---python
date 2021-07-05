# KPMG Powerapps Solution POC


## Installation / Usage
* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv or pip3 install virtualenv 
    ```
* Git clone this repo to your PC
    ```
        $ git clone https://gitlab.platformer.com/achalad/kpmg-powerapp-poc.git
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd <file-name>
        ```

    2. Create and fire up your virtual environment in python3:
        ```
        $ virtualenv -p python3 venv
        ```

* #### Install requirements
    ```
    (venv)$ pip install -r requirements.txt

* #### Run 
    ```
    (venv)$ python main.py