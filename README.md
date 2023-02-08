# dogbot
discord bot for the stable Diffusion on Golem (DOG) service


## To run ##
create a env.json file with the following schema:
```json
{
    "token": "<Your Discord Bot Token>",
    "webhook": "<Webhook to send status notifications to>"
}
```
the `webhook` can be any format that [`apprise`](https://github.com/caronc/apprise) accepts, if you don't need it then you can just comment out the apprise notifications in `golem/__init__.py`


install dependencies with 
```
$ pip3 install -r requirements.txt
```

you will also need to set up a [golem requestor environment](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development). (or if you have enough beans on your local machine you can configure the bot to run the img2txt.py script directly, changing `pipe.to('cpu')` to `pipe.to('cuda')` if you have gpu available)

in the `golem` directory create two subdirectories called `logs` and `output`

in one terminal start the bot:
```
$ python3 dogbot.py
```

next in another terminal start the redis server, you will need to install redis-server

(on Ubuntu)
```
$ sudo apt install redis-server
```

then start the server (or more than one if you would like)
```
$ rq worker
```

now connect your bot to your server, and you should be good to go!

by default the command is set to `/generate`, and you can use it like `/generate a picture of a dog`
