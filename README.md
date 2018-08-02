# Savory-Backend

This is the generic CRUD REST API powering the savory app. You probably don't care enough to read the rest of the 
document.

## Getting started

First, clone the repo from Heroku:
```bash
https://git.heroku.com/savory-backend.git
```
Or clone it from Github:
```bash
https://github.com/jchio001/Savory-Backend.git
```

Before beginning development, please ensure that the following tools are installed on your laptop:
- Python 3 (NOTE: Python 2.7 is the default on Mac!. [This guide](
https://docs.python-guide.org/starting/install3/osx/)gives a pretty good rundown on installing Python 3 with Brew. 
Be aware that there's 2 versions of Python on your laptop and to specific Python 3, use python3/pip3 instead! Currently, 
this app is using<b>Python 3.7</b>)
- Virtualenv (This should be done after installing Python3! Virtualenvs allows us to isolate python dependencies for a 
project, meaning that we have multiple projects cleanly running multiple different versions of a library.[Here's a 
good guide on installing and setting up a virtualenv.](
https://packaging.python.org/guides/installing-using-pip-and-virtualenv/))  

Once the Python environment has been set up correctly and that there's a virtualenv up and running, download all the 
requirements contained in `requirements.txt` with:
```bash
pip3 install -r requirements.txt
```

This should download all the libraries needed for the project and contain them within your virtualenv.

For security reasons, a lot of critical constant values are hidden in environment variables. These values 
(as of currently) are:
- App id for Facebook (`SAVORY_FB_APP_ID`)
- App secret for Facebook (`SAVORY_FB_APP_SECRET`)
- URL to the PostgresQL database (`SAVORY_DB_URL`)
- JWT secret (`SAVORY_JWT_SECRET`)

There is some amount of irony in this statement because this application is in a stage where no one cares enough to do 
something malicious with that information. If you are one of those people, I'm pretty sure browsing cat pictures on 
reddit is a better use of your time. If you are someone who is or will be developing this application, please 
ping[@jchio001](https://github.com/jchio001)for the appropriate values.

Finally, you're ready to deploy the application. To deploy the application locally, run:
```bash
gunicorn -w 2 -b 0.0.0.0:<put_port_number_here> routes:app
```

## Contributing

- Submit pull requests
- If your pull request installs a new requirement, please run `pip3 freeze > requirements.txt` before submitting a PR
- Don't write spaghetti code
- Actually QA your code before submitting a pull request
- Maybe one day unit tests will be a requirement

## License

What license thing homie?