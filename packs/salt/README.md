# SaltStack Integration Pack

Pack which allows integration with SaltStack.

## Configuration

This should be installed on the master

## Examples

```bash
    st2 run salt.client matches='web*' module=test.ping
    st2 run salt.client module=pkg.install kwargs='{"pkgs":["git","httpd"]}'

    st2 run salt.bootstrap instance_id=<uuid> provider=my-nova name=web.example.com
```
