# Bitcoin integration pack

Pack which integrates with bitcoin-cli.

## Pre-requisites

* Expects `btc_wallet` property to be defined in the StackStorm kv-store. This value
  must point to a server running bitcoind with the right bitcoin.conf already configured
  for the StackStorm user.

## Actions

* ``getaccoountaddress`` - Retrieves address of local wallet.
* ``getwalletinfo`` - Information of the local wallet.
* ``sendtoaddress`` - Send some BTC to supplied address.
