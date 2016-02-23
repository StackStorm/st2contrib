# Contributing to StackStorm pack directory

You've decided to create or update a StackStorm integration pack. That's great! 
We appreciate every contribution, and can't wait for your PR. To make sure other
people (and robots) can use, extend and enjoy your work as well, we have some 
guidelines in place, so please take a few minutes to read this doc through.

You can get additional information about StackStorm packs and contributions
in the StackStorm documentation:

- [Integration Packs](https://docs.stackstorm.com/packs.html)
- [Create and Contribute a Pack](https://docs.stackstorm.com/reference/packs.html)
- [Pack testing](https://docs.stackstorm.com/development/pack_testing.html)

## General guidelines

* If you're contributing to a pack, please __update the version__ in `pack.yaml`! 
  Without the version bump your PR will not be accepted. Pack versions follow 
  [SemVer](http://semver.org/), and you should declare the new version 
  accordingly.

* If you're creating a brand-new pack, make sure all the __metadata__ is in place: 
  the `pack.yaml` file, the necessary folder structure, ideally a 64x64 PNG icon.

* It's important that all packs remain stable and reliable, so we recommend 
  writing __automated tests__ for your actions and sensors: refer to the 
  [pack testing manual](https://docs.stackstorm.com/development/pack_testing.html) 
  for details. While it's not mandatory, complex or mission-critical packs should 
  normally have at least a few tests; smaller contributions can do with 
  a reasonable amount of manual testing.

* __Formatting your code__ should be done according to PEP8 (see 
  [StackStorm code style guide](https://docs.stackstorm.com/development/index.html#code-style-guide) 
  for details) and will be evaluated with `flake8` and `pylint`. The styling tests 
  are run automatically and the PR won't be accepted unless they pass, so it usually 
  makes sense to have a linter in your text editor or lint the code manually before
  submitting it.

* Packs in `st2contrib` should normally be __dedicated to a single product__
  and independent of other packs except for the default packs in StackStorm core. 
  If you must have a dependency, please mention it in the readme; if you have a 
  workflow encompassing actions from multiple packs, consider placing it into a 
  separate `examples` directory.

* Lastly, we would really appreciate it if you could enrich your pack with some
  __ChatOps aliases__. A lot of people use ChatOps in StackStorm, and having default
  aliases can increase the pack's adoption. Bonus points for alias contributions 
  to existing packs!

Thank you for reading! Please remember those are just guidelines, not strict rules, 
and if there's a reason some of them don't apply to your pack, it's fine;
just make sure to mention it in your PR, and may the force be with you! :heart: