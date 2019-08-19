cleaning-notification-bot
=========

## Description

- Get cleaning duty data from Google Spreadsheet as RESTful API and notify Slack

## Requirement

- [SheetDB](https://sheetdb.io/)
- AWS Lambda
- [Serverless Framework](https://serverless.com/)
- Docker & Docker-Compose

## Usage

### SheetDB Settings

- Copy this sample spreadsheet.
  - [sample spreadsheet](https://docs.google.com/spreadsheets/d/11FYBwRmZESeMyWizrYBh4JnfCIAO2pqrZ3ixYluENQM/edit?usp=sharing)
- Use the copied sample spreadsheet to set up SheetDB. 

### Lambda Settings

- Clone this repository. 

```bash
$ git clone git@github.com:myoshioka/cleaning-notification-bot.git
```

- Set env.
  - Set SheetDB-API and AWS credential.

```bash
$ cd cleaning-notification-bot
$ cp .env.local .env
```
```env
SPREADSHEET_API_BASE_URL=https://sheetdb.io/api/v1/
# SheetDB-API key
SPREADSHEET_API_KEY=
# SheetDB-API Basic authentication ID
AUTH_ID=
# SheetDB-API Basic authentication password
AUTH_PASS=
# Slack incoming webhooks URL
WEB_HOOK_URL=
# spreadsheet URL
G_SPREADSHEET=
# AWS credential
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

```

- Launch Docker

```bash
$ docker-compose up -d
```

- Deploy Lambda

```bash
$ docker exec <docker-image> sls deploy -v --stage dev
```

- Test

```bash
$ docker exec <docker-image> sls invoke local -f notification -d '{"today":"20190820"}'
```

## Author

[Makoto Yoshioka](https://github.com/myoshioka)
