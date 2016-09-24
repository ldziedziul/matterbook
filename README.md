# Matterbook #
Tool for sending [Facebook](facebook.com) posts to the [Mattermost](https://www.mattermost.org). Matterbook checks if the latest post from given facebook page contains specific expression and then sends it to the Mattermost

## Requirements ##
 - Python
 - [virtualenv][virtualenv]
 - [pip (package manager)][pip]

## Setup ##
run `./setup-venv.sh`
`cp matterbook.cfg.default matterbook.cfg`
It will create the virtual env and install all required dependencies (see `requirements.txt`)

## Configuration ##

Set paramaters in `matterbook.yml`:
```
facebook:
  access_token: SGEgaGEgaGEhIENoY2lhxYJiecWbIDpQ # Obtained from https://developers.facebook.com/tools/explorer
  app_id: 123 # Obtained from https://developers.facebook.com/apps
  app_secret: 123 # Obtained from https://developers.facebook.com/apps
  page_id: somePageName # part or url right after https://www.facebook.com/, e.g. https://www.facebook.com/somePageName
  post_filter: some keyword # (Optional) send to mattermost only posts containing given expression

mattermost:
  webhook_url: https://mattermost.host/hooks/abc
  username: bot.name # (Optional)
  icon_url: http://some.host/with/icon.png # (Optional)
  basic_auth: # (Optional)
    username: some_user
    password: some_password
```

**Important!** Be aware that after each run matterbook.yml will be updated with new extended(long-lived) access token

## Run ##
run simply `./matterbook.py` or 
`./matterbook-start.sh` to start matterbook in background.
  
run `./matterbook-stop.sh` to stop matterbook