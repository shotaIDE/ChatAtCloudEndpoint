# Chat@Cloud Message Endpoint

## How to start?

Open folder in VSCode.

Prepare Python environment by using virtualenv.

```shell
pip install virtualenv
virtualenv env
```

Activate Python environment.

```shell
source env/bin/activate
```

Install required packages.

```shell
pip install -r requirements.txt
```

Download Selenium Chrome driver from below.  
https://chromedriver.chromium.org/downloads

Copy settings json file and write Selenium Chrome driver path and credentials in it.

```shell
cp settings_sample.json settings.json
```

Run the following command.

```shell
python main.py --prod SendMessageSuffix
```

## How to develop ?

Run the script using the "Launch" configuration.
