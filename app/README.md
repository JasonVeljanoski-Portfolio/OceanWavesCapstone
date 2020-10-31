# SETUP PROCESS

## Make sure your have the correct dependencies

Install nodejs:
- https://nodejs.org/en/download/package-manager/

```{bash}
$ node -v

v12.15.0
```

## Run API Server

Open a terminal:

1. Make sure you are in the `app/server` directory.

2. Create your own virtual enviroment.

```{bash}
$ sudo pip install virtualenv # Install virtualenv if you havnt already
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

3. To run the height ml model, you must install `lightgbm`
- https://lightgbm.readthedocs.io/en/latest/Installation-Guide.html

4. Run api server

```{bash}
$ flask run
```

5. Browse

### Run Web Client

Open another terminal:
Navigate to `app/client` directory.

1. Install node dependencies

```{bash}
$ npm install
```

2. Run

```{bash}
$ npm run dev
```