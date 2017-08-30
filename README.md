![](http://i.imgur.com/uHWYuDY.png)

# We Have Moved!

StackStorm 2.1 was released in late 2016 and it greatly improved the way you work with integration packs.

There's new CLI commands to manage packs, support for source lists, API endpoints, but the most important change in 2.1 goes beyond the StackStorm codebase. We have built [StackStorm Exchange](https://exchange.stackstorm.org): a dedicated pack directory with a consumable JSON index, automatic version tagging, extensible CI for each pack, and more.

With all the new features in Exchange, storing all packs in one large repository doesn't cut it anymore, so we moved away from st2contrib to a separate GitHub organization. **All packs are now stored as separate repositories in [StackStorm-Exchange](https://github.com/StackStorm-Exchange), st2contrib is closed.**

As of August 2017, we've moved all `st2contrib` content into an `archive` directory. We did this in advance of the removal of `st2contrib` altogether, for those (hopefully) few of you still using this repository. If you're reading this, please consider upgrading. The content in the `archive` directory is there to get you out of a bind, but this is your final chance to upgrade to a new version of StackStorm and start using Exchange repositories.

Again, there will be no updates to `st2contrib` - the next step is to delete the repository. All the issues and pull requests for packs will only be tracked in StackStorm-Exchange repositories.

Thanks so much for being a part of StackStorm's transition to the Exchange and for taking advantage of the new features we push into StackStorm at every release cycle. We hope you love it!

_— StackStorm Engineering Team_

