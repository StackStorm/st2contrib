# Hubot Integration Pack

Pack that provides management/integration with Hubot

## Configuration

* `endpoint` - Location of Hubot HTTP endpoint (default: http://127.0.0.1:8181)

## Actions

* `branch`       - List the current deployed git branch of Hubot.
* `deploy`       - Deploy a specific git branch of deployed Hubot
* `restart`      - Restart Hubot
* `post_message` - Post raw text to Hubot via HTTP API
* `post_result`  - Send JSON formatted action output via hubot-stackstorm adapter
* `update_ref`   - Update the git branch of deployed Hubot

## ChatOps Aliases

* `hubot branch`            -> hubot.branch
* `hubot deploy {{branch}}` -> hubot.deploy
* `hubot restart`           -> hubot.restart
