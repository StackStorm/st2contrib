## Readme

This pack allows you to use CLICRUD effectively within StackStorm or the Brocade Workflow Composer.


This pack contains three actions:
```text
- ops_command
- config_command
- chain_remediate
```

####ops_command

Allows you to run an operational command on a Brocade ICX, MLX or VDX using CLI.

####config_command

Allows you to run a comma separated LIST of configuration commands. The real world rarely leads to running a single command so this action allows you to create a list of them which will be pushed. This could also mean a comma separated template, with the comma allowing each input to be treated as a line.

####chain_remediate

This simple action-chain takes input in the form of an alert (from another open source project called GoPE: http://github.com/davidjohngee/gope), alerts a Slack channel, attempts autoremediation with a single or list of commands, then updates slack users.

Have a play!

####CLICRUD

If you are not familiar with CLICRUD, check out http://github.com/davidjohngee/clicrud for the latest or install using PyPi:

```bash
pip install clicrud
```

This dependency will automatically be installed on ST2/BWC so don't worry about that! You do not have to install this to get the clicrudST2 integration working.

####Installing

Install is straight forward.

1.	Login in to your ST2/BWC

2.	Go to the ```bash /opt/stackstorm/packs/``` directory

3.	Execute ```bash git clone http://github.com/davidjohngee/clicrudST2.git

4.	On the ST2 client: ```bash st2 run packs.setup_virtualenv packs=clicrud```

5.	On the ST2 client: ```bash st2 run packs.load register=clicrud```

5.	Veryfiy the install with ```bash st2 action list --pack=default```

You're good to go.

####Configuration file/s

```bash config.yaml```

This file hides the connectivity method and credentials from the actual composer itself. This is to limit what can change in the workflows/rules.

Currently the connectivity method is also in the configuration file. This in the future may change. Everyone uses SSH right? (Just nod).

Last step for this part, copy this configuration file to the ```bash/config``` directory within ```bash/opt/stackstorm```

```python
  ---
  username: "admin"
  password: "password"
  enable:   "password"
  method:    "ssh"
```

####Rules

So you can get going quickly with The ST2 CLICRUD integration, there are some existing rules.
Take a look at them!







