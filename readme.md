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

- Launch Docker and deploy.

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
