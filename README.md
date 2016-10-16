# Matterbook #
Tool for sending [Facebook](https://facebook.com) posts to the [Mattermost](https://www.mattermost.org). Matterbook checks if the latest post from given facebook page contains specific expression and then sends it to the Mattermost

## Requirements ##
 - Python
 - [virtualenv](https://virtualenv.readthedocs.io/en/latest)
 - [pip](https://packaging.python.org/install_requirements_linux/#installing-pip-setuptools-wheel-with-linux-package-managers)

## Setup ##
run `./setup-venv.sh`

It will create the virtual env and install all required dependencies (see `requirements.txt`)

Create config file:

`cp matterbook.yml.default matterbook.yml`


## Configuration ##

Set paramaters in `matterbook.yml`:
```
facebook:
  access_token: SGEgaGEgaGEhIENoY2lhxYJiecWbIDpQ # Obtained from https://developers.facebook.com/tools/explorer
  app_id: 123 # Obtained from https://developers.facebook.com/apps
  app_secret: 123 # Obtained from https://developers.facebook.com/apps

mattermost:
  webhook_url: https://mattermost.host/hooks/abc
  basic_auth: # (Optional)
    username: some_user
    password: some_password

integrations:
- some_unique_name:
    fb_page_id: somePageName # part or url right after https://www.facebook.com/, e.g. https://www.facebook.com/somePageName
    fb_post_filter: some keyword # (Optional) send to mattermost only posts containing given expression
    mm_icon_url: http://some.host/with/icon.png # (Optional)
    mm_username: bot.name # (Optional)
- some_other_unique_name:
    fb_page_id: someOtherPageName # part or url right after https://www.facebook.com/, e.g. https://www.facebook.com/someOtherPageName
    fb_post_filter: some other keyword # (Optional) send to mattermost only posts containing given expression
    mm_icon_url: http://some.other.host/with/other_icon.png # (Optional)
    mm_username: other.bot.name # (Optional)
```

**Important!** Be aware that after each run matterbook.yml will be updated with new extended(long-lived) access token

## Run ##
Run `./matterbook-run.sh` to start matterbook in current terminal. If you want to start matterbook in the background use `./matterbook-start.sh`
  
run `./matterbook-stop.sh` to stop matterbook
