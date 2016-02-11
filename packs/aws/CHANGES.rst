## v0.6.0

* Fix the result format of some of the actions such as ``ec2_run_instances``. Previously,
  the result was a list of lists of dicts and now the result is correctly a list of dicts.

  Keep in mind that this is a breaking changes.

  If you previously accessed the result of the ``ec2_run_instances`` action in the action-chain
  workflow like that - ``run_instances.result[0][0].id``, you need to update it so it looks like
  this ``run_instance.result[0].id``.
