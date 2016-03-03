# StackStorm Community Repo

[![StackStorm](https://github.com/stackstorm/st2/raw/master/stackstorm_logo.png)](http://www.stackstorm.com)

[![Build Status](https://travis-ci.org/StackStorm/st2contrib.svg?branch=master)](https://travis-ci.org/StackStorm/st2contrib)  [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/StackStorm/st2contrib/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/StackStorm/st2contrib/?branch=master)  [![IRC](https://img.shields.io/irc/%23stackstorm.png)](http://webchat.freenode.net/?channels=stackstorm)

Contents of this repository are comprise of integrations and automations that
are consumed by the [StackStorm automation platform](http://www.stackstorm.com/product/).

* Get [StackStorm](http://www.stackstorm.com/start-now/).
* Explore community portal at [stackstorm.com/community](http://www.stackstorm.com/community).
* Read the docs to learn how to use integration packs with StackStorm at
  [docs.stackstorm.com](http://docs.stackstorm.com/packs.html).

## Packs

Actions, Sensors and Rules all organized neatly into to domain or tool specific
packs.

## Extra

Related tools that help make it easier to integrate and consume StackStorm content.

## Tests and Automated Checks

By default, Travis CI runs the following checks (makefiles tasks):

* ``flake8`` - Runs ``flake8`` on all the Python files.
* ``pylint`` - Runs ``pylint`` on all the Python files.
* ``configs-check`` - Makes sure that all the JSON and YAML resource metadata
  files contain correct syntax.
* ``metadata-check`` - Verifies that each pack contains pack metadata file
  (``pack.yaml``).
* ``packs-resource-register`` - Registers resources from all the packs and
  makes sure the registration succeeds.
* ``packs-tests`` - Runs tests for all the packs.

To run all those checks locally, you can use the following command:

```bash
make all
```

By default when running this command on a non-master branch, it will only
perform checks on changed files and packs. If you want to run checks on all the
files and packs (regardless if they changed or not), you can do that by
specifying ``FORCE_CHECK_ALL_FILES=true`` environment variable as show below.

```bash
FORCE_CHECK_ALL_FILES=true make all
```

If you want to force run checks on a specific pack you can do that by specifying
``FORCE_CHECK_PACK=<pack name>` environment variable as shown below.

```bash
FORCE_CHECK_PACK=csv make all
# or
FORCE_CHECK_PACK=csv make packs-tests
```

## Available Packs

Icon | Name | Description | Keywords | Author | Latest Version | Available Resources
---- | ---- | ----------- | -------- | ------ | -------------- | -------------------
[![activecampaign icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/activecampaign/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/activecampaign) | [activecampaign](https://github.com/StackStorm/st2contrib/tree/master/packs/activecampaign) | Integration with ActiveCampaign |  | [DoriftoShoes](mailto:patrick@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#activecampaign-pack)
[![ansible icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/ansible/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/ansible) | [ansible](https://github.com/StackStorm/st2contrib/tree/master/packs/ansible) | st2 content pack containing ansible integrations | ansible, cfg management, configuration management | [st2-dev](mailto:info@stackstorm.com) | 0.3 | [click](https://github.com/StackStorm/st2contrib#ansible-pack)
[![aws icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/aws/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/aws) | [aws](https://github.com/StackStorm/st2contrib/tree/master/packs/aws) | st2 content pack containing Amazon Web Services integrations. | aws, amazon web services, amazon, ec2, sqs, sns, route53, cloud, iam, vpc, s3, CloudFormation, RDS, SQS | [st2-dev](mailto:info@stackstorm.com) | 0.6.0 | [click](https://github.com/StackStorm/st2contrib#aws-pack)
[![azure icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/azure/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/azure) | [azure](https://github.com/StackStorm/st2contrib/tree/master/packs/azure) | st2 content pack containing Microsoft Azure integrations. | microsoft, azure, cloud, libcloud, servers, virtual machines, azure virtual machines | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#azure-pack)
[![bitbucket icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/bitbucket/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/bitbucket) | [bitbucket](https://github.com/StackStorm/st2contrib/tree/master/packs/bitbucket) | Pack which allows integration with Bitbucket. | bitbucket, vcs, mercuriral, git, source control | [Aamir](mailto:raza.aamir01@gmail.com) | 0.1.1 | [click](https://github.com/StackStorm/st2contrib#bitbucket-pack)
[![bitcoin icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/bitcoin/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/bitcoin) | [bitcoin](https://github.com/StackStorm/st2contrib/tree/master/packs/bitcoin) | bitcoin integration pack | bitcoin | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#bitcoin-pack)
[![cassandra icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/cassandra/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/cassandra) | [cassandra](https://github.com/StackStorm/st2contrib/tree/master/packs/cassandra) | st2 content pack containing cassandra integrations | datastax, cassandra | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#cassandra-pack)
[![chef icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/chef/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/chef) | [chef](https://github.com/StackStorm/st2contrib/tree/master/packs/chef) | st2 chef integration pack | chef, chef-client, chef-solo, chef-apply, cfg management, configuration management, opscode | [st2-dev](mailto:info@stackstorm.com) | 0.1.1 | [click](https://github.com/StackStorm/st2contrib#chef-pack)
[![Circle CI icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/circle_ci/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/Circle CI) | [Circle CI](https://github.com/StackStorm/st2contrib/tree/master/packs/Circle CI) | Pack which allows integration with Circle CI. | circle, circle ci, continous integration, ci | [StackStorm dev](mailto:support@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#Circle CI-pack)
[![consul icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/consul/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/consul) | [consul](https://github.com/StackStorm/st2contrib/tree/master/packs/consul) | consul |  | [jfryman](mailto:james@fryman.io) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#consul-pack)
[![csv icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/csv/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/csv) | [csv](https://github.com/StackStorm/st2contrib/tree/master/packs/csv) | st2 content pack containing CSV integrations | csv, serialization, deserialization, text processing | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#csv-pack)
[![cubesensors icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/cubesensors/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/cubesensors) | [cubesensors](https://github.com/StackStorm/st2contrib/tree/master/packs/cubesensors) | st2 content pack containing CubeSensors integrations | cubesensors, iot, smart home, sensors, probes, home automation | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#cubesensors-pack)
[![Digital Ocean icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/digitalocean/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/Digital Ocean) | [Digital Ocean](https://github.com/StackStorm/st2contrib/tree/master/packs/Digital Ocean) | st2 content pack containing Digital Ocean integration. |  | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#Digital Ocean-pack)
[![dimensiondata icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/dimensiondata/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/dimensiondata) | [dimensiondata](https://github.com/StackStorm/st2contrib/tree/master/packs/dimensiondata) | st2 content pack containing Dimension Data Cloud integrations | cloud, load balancers, dimension data | [Anthony Shaw](mailto:anthony.shaw@dimensiondata.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#dimensiondata-pack)
[![docker icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/docker/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/docker) | [docker](https://github.com/StackStorm/st2contrib/tree/master/packs/docker) | st2 content pack containing docker integrations | docker, containers, virtualization, cgroups | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#docker-pack)
[![dripstat icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/dripstat/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/dripstat) | [dripstat](https://github.com/StackStorm/st2contrib/tree/master/packs/dripstat) | Integration with the Dripstat Application Performance Monitoring tool | dripstat, java, monitoring, performance monitoring | [James Fryman](mailto:james@fryman.io) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#dripstat-pack)
[![elasticsearch icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/elasticsearch/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/elasticsearch) | [elasticsearch](https://github.com/StackStorm/st2contrib/tree/master/packs/elasticsearch) | st2 elasticsearch integration pack | elasticsearch, curator, databases | [st2-dev](mailto:info@stackstorm.com) | 0.2.0 | [click](https://github.com/StackStorm/st2contrib#elasticsearch-pack)
[![email icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/email/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/email) | [email](https://github.com/StackStorm/st2contrib/tree/master/packs/email) | E-Mail Actions/Sensors for StackStorm |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#email-pack)
[![fireeye icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/fireeye/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/fireeye) | [fireeye](https://github.com/StackStorm/st2contrib/tree/master/packs/fireeye) | FireEye CM Series Integration |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#fireeye-pack)
[![fpm icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/fpm/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/fpm) | [fpm](https://github.com/StackStorm/st2contrib/tree/master/packs/fpm) | fpm |  | [jfryman](mailto:jfryman@FryBook-2.local) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#fpm-pack)
[![freight icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/freight/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/freight) | [freight](https://github.com/StackStorm/st2contrib/tree/master/packs/freight) | freight |  | [James Fryman](mailto:james@fryman.io) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#freight-pack)
[![git icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/git/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/git) | [git](https://github.com/StackStorm/st2contrib/tree/master/packs/git) | st2 content pack containing git integrations | git, scm | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#git-pack)
[![github icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/github/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/github) | [github](https://github.com/StackStorm/st2contrib/tree/master/packs/github) | st2 content pack containing github integrations | github, git, scm | [st2-dev](mailto:info@stackstorm.com) | 0.3 | [click](https://github.com/StackStorm/st2contrib#github-pack)
[![google icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/google/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/google) | [google](https://github.com/StackStorm/st2contrib/tree/master/packs/google) | st2 content pack containing google integrations | google, search | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#google-pack)
[![gpg icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/gpg/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/gpg) | [gpg](https://github.com/StackStorm/st2contrib/tree/master/packs/gpg) | Pack for working with GPG. | gpg, pgp, gnupg, privacy, encryption, crypto | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#gpg-pack)
[![hubot icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/hubot/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/hubot) | [hubot](https://github.com/StackStorm/st2contrib/tree/master/packs/hubot) | Hubot integration pack |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#hubot-pack)
[![hue icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/hue/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/hue) | [hue](https://github.com/StackStorm/st2contrib/tree/master/packs/hue) | Philips Hue Pack | hue, philips, iot | [James Fryman](mailto:james@stackstorm.com) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#hue-pack)
[![ipcam icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/ipcam/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/ipcam) | [ipcam](https://github.com/StackStorm/st2contrib/tree/master/packs/ipcam) | st2 content pack containing integration for various home IP cams | ipcam, ip cam, ip camera, camera, smart home, home automation | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#ipcam-pack)
[![irc icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/irc/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/irc) | [irc](https://github.com/StackStorm/st2contrib/tree/master/packs/irc) | st2 content pack containing irc integrations | irc, internet relay chat, chat, messaging, instant messaging | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#irc-pack)
[![jenkins icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/jenkins/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/jenkins) | [jenkins](https://github.com/StackStorm/st2contrib/tree/master/packs/jenkins) | Jenkins CI Integration Pack |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#jenkins-pack)
[![jira icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/jira/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/jira) | [jira](https://github.com/StackStorm/st2contrib/tree/master/packs/jira) | st2 content pack containing jira integrations | issues, ticket management, project management | [st2-dev](mailto:info@stackstorm.com) | 0.3 | [click](https://github.com/StackStorm/st2contrib#jira-pack)
[![jmx icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/jmx/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/jmx) | [jmx](https://github.com/StackStorm/st2contrib/tree/master/packs/jmx) | st2 content pack containing Java JMX integrations | jmx, javajmx, java management extensions, mbean | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#jmx-pack)
[![kubernetes icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/kubernetes/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/kubernetes) | [kubernetes](https://github.com/StackStorm/st2contrib/tree/master/packs/kubernetes) | st2 content pack containing Kubernetes sensors | kubenetes, sensors, thirdpartyresource | [Michael Ward](mailto:mward29@gmail.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#kubernetes-pack)
[![lastline icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/lastline/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/lastline) | [lastline](https://github.com/StackStorm/st2contrib/tree/master/packs/lastline) | Lastline Security Breach Detection Integration |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#lastline-pack)
[![libcloud icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/libcloud/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/libcloud) | [libcloud](https://github.com/StackStorm/st2contrib/tree/master/packs/libcloud) | st2 content pack containing libcloud integrations | libcloud, cloud, dns, dnsaas, lbaas, load balancers, aws, amazon, s3, ec2, rackspace, cloudstack, openstack, cloudsigma, gce, google compute engine | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#libcloud-pack)
[![librato icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/librato/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/librato) | [librato](https://github.com/StackStorm/st2contrib/tree/master/packs/librato) | Send and manage metrics with Librato |  | [James Fryman](mailto:james@fryman.io) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#librato-pack)
[![mailgun icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mailgun/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/mailgun) | [mailgun](https://github.com/StackStorm/st2contrib/tree/master/packs/mailgun) | st2 content pack containing mailgun integrations | email, mail, mailgun | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#mailgun-pack)
[![mistral icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mistral/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/mistral) | [mistral](https://github.com/StackStorm/st2contrib/tree/master/packs/mistral) | Mistral integrations to operate mistral. | mistral, workflows | [StackStorm](mailto:support@stackstorm.com) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#mistral-pack)
[![mmonit icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mmonit/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/mmonit) | [mmonit](https://github.com/StackStorm/st2contrib/tree/master/packs/mmonit) | st2 content pack containing mmonit integrations | monitoring, mmonit | [Itxaka Serrano Garcia](mailto:itxakaserrano@gmail.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#mmonit-pack)
[![mqtt icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mqtt/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/mqtt) | [mqtt](https://github.com/StackStorm/st2contrib/tree/master/packs/mqtt) | MQTT Integration for StackStorm |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#mqtt-pack)
[![nagios icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/nagios/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/nagios) | [nagios](https://github.com/StackStorm/st2contrib/tree/master/packs/nagios) | Nagios integration pack. See README.md for setup instructions. | nagios, monitoring, alerting | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#nagios-pack)
[![nest icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/nest/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/nest) | [nest](https://github.com/StackStorm/st2contrib/tree/master/packs/nest) | StackStorm integration with Nest Thermostats |  | [James Fryman](mailto:james@stackstorm.com) | 0.0.1 | [click](https://github.com/StackStorm/st2contrib#nest-pack)
[![newrelic icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/newrelic/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/newrelic) | [newrelic](https://github.com/StackStorm/st2contrib/tree/master/packs/newrelic) | st2 content pack containing newrelic integrations | new relic, monitoring, app monitoring, application level monitoring | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#newrelic-pack)
[![octopusdeploy icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/octopusdeploy/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/octopusdeploy) | [octopusdeploy](https://github.com/StackStorm/st2contrib/tree/master/packs/octopusdeploy) | st2 content pack containing octopusdeploy integrations | octopus, octopusdeploy, deployment, continous deployment, continous integration | [Anthony Shaw](mailto:anthony.shaw@dimensiondata.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#octopusdeploy-pack)
[![openhab icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/openhab/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/openhab) | [openhab](https://github.com/StackStorm/st2contrib/tree/master/packs/openhab) | Integration with OpenHAB | openhab, iot, smart home, home automation | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#openhab-pack)
[![openstack icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/openstack/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/openstack) | [openstack](https://github.com/StackStorm/st2contrib/tree/master/packs/openstack) | st2 content pack containing openstack integrations | cloud, nova, glance, neutron | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#openstack-pack)
[![packagecloud icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/st2/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/packagecloud) | [packagecloud](https://github.com/StackStorm/st2contrib/tree/master/packs/packagecloud) | packagecloud integration pack | packagecloud | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#packagecloud-pack)
[![packer icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/packer/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/packer) | [packer](https://github.com/StackStorm/st2contrib/tree/master/packs/packer) | Hashicorp Packer builder integration | packer, provisioning, pipeline, hashicorp | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#packer-pack)
[![pagerduty icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/pagerduty/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/pagerduty) | [pagerduty](https://github.com/StackStorm/st2contrib/tree/master/packs/pagerduty) | Packs which allows integration with PagerDuty services. |  | [Aamir](mailto:raza.aamir01@gmail.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#pagerduty-pack)
[![puppet icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/puppet/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/puppet) | [puppet](https://github.com/StackStorm/st2contrib/tree/master/packs/puppet) | st2 content pack containing puppet integrations | puppet, cfg management, configuration management | [st2-dev](mailto:info@stackstorm.com) | 0.2 | [click](https://github.com/StackStorm/st2contrib#puppet-pack)
[![qualys icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/qualys/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/qualys) | [qualys](https://github.com/StackStorm/st2contrib/tree/master/packs/qualys) | Qualys Cloud Security Services integration pack | security, qualys | [Anthony Shaw](mailto:anthony.shaw@dimensiondata.com) | 1.0 | [click](https://github.com/StackStorm/st2contrib#qualys-pack)
[![rabbitmq icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/rabbitmq/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/rabbitmq) | [rabbitmq](https://github.com/StackStorm/st2contrib/tree/master/packs/rabbitmq) | st2 content pack containing rabbitmq integrations | rabbitmq, queuing, messaging, aqmp, stomp, message broker | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#rabbitmq-pack)
[![rackspace icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/rackspace/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/rackspace) | [rackspace](https://github.com/StackStorm/st2contrib/tree/master/packs/rackspace) | Packs which allows integration with Rackspace services such as servers, load balancers and DNS. |  | [jfryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#rackspace-pack)
[![reamaze icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/reamaze/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/reamaze) | [reamaze](https://github.com/StackStorm/st2contrib/tree/master/packs/reamaze) | reamaze Integration Pack |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.1 | [click](https://github.com/StackStorm/st2contrib#reamaze-pack)
[![salt icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/salt/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/salt) | [salt](https://github.com/StackStorm/st2contrib/tree/master/packs/salt) | st2 salt integration pack | salt, cfg management, configuration management | [jcockhren](mailto:jurnell@sophicware.com) | 0.4 | [click](https://github.com/StackStorm/st2contrib#salt-pack)
[![sensu icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/sensu/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/sensu) | [sensu](https://github.com/StackStorm/st2contrib/tree/master/packs/sensu) | st2 content pack containing sensu integrations | sensu, monitoring, alerting | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#sensu-pack)
[![servicenow icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/servicenow/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/servicenow) | [servicenow](https://github.com/StackStorm/st2contrib/tree/master/packs/servicenow) | ServiceNow Integration Pack |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#servicenow-pack)
[![signalr icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/signalr/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/signalr) | [signalr](https://github.com/StackStorm/st2contrib/tree/master/packs/signalr) | st2 content pack containing signalr integrations | signalr, messaging | [Anthony Shaw](mailto:anthony.shaw@dimensiondata.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#signalr-pack)
[![slack icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/slack/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/slack) | [slack](https://github.com/StackStorm/st2contrib/tree/master/packs/slack) | st2 content pack containing slack integrations | slack, chat, messaging, instant messaging | [st2-dev](mailto:info@stackstorm.com) | 0.2.1 | [click](https://github.com/StackStorm/st2contrib#slack-pack)
[![SmartThings icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/smartthings/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/SmartThings) | [SmartThings](https://github.com/StackStorm/st2contrib/tree/master/packs/SmartThings) | Integration with SmartThings | smartthings, iot, smart home, home automation | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#SmartThings-pack)
[![softlayer icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/softlayer/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/softlayer) | [softlayer](https://github.com/StackStorm/st2contrib/tree/master/packs/softlayer) | st2 content pack containing Softlayer integrations. | softlayer, cloud | [Itxaka Serrano Garcia](mailto:itxakaserrano@gmail.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#softlayer-pack)
[![splunk icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/splunk/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/splunk) | [splunk](https://github.com/StackStorm/st2contrib/tree/master/packs/splunk) | Splunk integration pack | splunk | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#splunk-pack)
[![st2 icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/st2/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/st2) | [st2](https://github.com/StackStorm/st2contrib/tree/master/packs/st2) | StackStorm pack management |  | [st2-dev](mailto:info@stackstorm.com) | 0.1.1 | [click](https://github.com/StackStorm/st2contrib#st2-pack)
[![time icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/time/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/time) | [time](https://github.com/StackStorm/st2contrib/tree/master/packs/time) | st2 content pack containing different date and time related functionality | date, time | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#time-pack)
[![Travis CI icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/travis_ci/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/Travis CI) | [Travis CI](https://github.com/StackStorm/st2contrib/tree/master/packs/Travis CI) | Pack which allows integration with Travis CI. | travis, travis ci, continous integration, ci | [Aamir](mailto:raza.aamir01@gmail.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#Travis CI-pack)
[![trello icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/trello/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/trello) | [trello](https://github.com/StackStorm/st2contrib/tree/master/packs/trello) | Integration with Trello, Web based Project Management | trello, kanban, productivity, collaboration | [James Fryman](mailto:james@stackstorm.com) | 0.2.0 | [click](https://github.com/StackStorm/st2contrib#trello-pack)
[![twilio icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/twilio/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/twilio) | [twilio](https://github.com/StackStorm/st2contrib/tree/master/packs/twilio) | st2 content pack containing twilio integrations |  | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#twilio-pack)
[![twitter icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/twitter/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/twitter) | [twitter](https://github.com/StackStorm/st2contrib/tree/master/packs/twitter) | st2 content pack containing twitter integrations | twitter, social media, social networks | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#twitter-pack)
[![typeform icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/typeform/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/typeform) | [typeform](https://github.com/StackStorm/st2contrib/tree/master/packs/typeform) | Typeform service integration pack |  | [st2-dev](mailto:info@stackstorm.com) | 0.2 | [click](https://github.com/StackStorm/st2contrib#typeform-pack)
[![urbandict icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/urbandict/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/urbandict) | [urbandict](https://github.com/StackStorm/st2contrib/tree/master/packs/urbandict) | st2 content pack containing urban dictionary integrations | urban dict, urban dictionary, puns | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#urbandict-pack)
[![victorops icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/victorops/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/victorops) | [victorops](https://github.com/StackStorm/st2contrib/tree/master/packs/victorops) | Packs which allows integration with Victorops events. | victorps integration, open, ack and resolve incidents | [Aamir](mailto:raza.aamir01@gmail.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#victorops-pack)
[![webpagetest icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/webpagetest/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/webpagetest) | [webpagetest](https://github.com/StackStorm/st2contrib/tree/master/packs/webpagetest) | st2 content pack containing webpagetest integrations | webpagetest, benchmarking | [Linuturk](mailto:linuturk@onitato.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#webpagetest-pack)
[![windows icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/windows/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/windows) | [windows](https://github.com/StackStorm/st2contrib/tree/master/packs/windows) | st2 content pack containing windows integrations | windows, wmi, windows management interface, wql | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#windows-pack)
[![witai icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/witai/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/witai) | [witai](https://github.com/StackStorm/st2contrib/tree/master/packs/witai) | Wit AI Integration with StackStorm |  | [James Fryman](mailto:james@stackstorm.com) | 0.1.0 | [click](https://github.com/StackStorm/st2contrib#witai-pack)
[![xml icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/xml/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/xml) | [xml](https://github.com/StackStorm/st2contrib/tree/master/packs/xml) | st2 content pack containing XML integrations | xml, serialization, deserialization, text processing | [st2-dev](mailto:info@stackstorm.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#xml-pack)
[![yammer icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/yammer/icon.png)](https://github.com/StackStorm/st2contrib/tree/master/packs/yammer) | [yammer](https://github.com/StackStorm/st2contrib/tree/master/packs/yammer) | st2 content pack containing yammer integrations | yammer, chatops, social | [Anthony Shaw](mailto:anthony.shaw@dimensiondata.com) | 0.1 | [click](https://github.com/StackStorm/st2contrib#yammer-pack)
### activecampaign pack

![activecampaign icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/activecampaign/icon.png)

#### Sensors

Name | Description
---- | -----------
ActiveCampaignWebhook | ActiveCapmaign Webhook sensor

#### Actions

Name | Description
---- | -----------
account_view | View hosted account information.
automation_contact_add | Add contact to automation
automation_contact_list | View contacts from an automation
automation_contact_remove | Remove contact from automation
automation_contact_view | View a single contact in an automation
automation_list | View existing automations
branding_edit | Update Design/Branding settings for User Groups.
branding_view | View Design/Branding settings for a specific User Group.
campaign_create | Create new campaign.
campaign_delete | Delete existing campaign.
campaign_delete_list | Delete multiple existing campaigns.
campaign_list | View one or many campaigns.
campaign_paginator | View a list of existing campaigns using pagination, much like it appears in the standard user interface.
campaign_report_bounce_list | View bounced email addresses for a specific campaign.
campaign_report_bounce_totals | Obtain bounce totals for a specific campaign.
campaign_report_forward_list | View forwarded email addresses for a specific campaign.
campaign_report_forward_totals | Obtain forward totals for a specific campaign.
campaign_report_link_list | View all links (and click data) for a specific campaign.
campaign_report_link_totals | Obtain link click totals for a specific campaign.
campaign_report_open_list | View opens for a specific campaign.
campaign_report_open_totals | Obtain open totals for a specific campaign.
campaign_report_totals | Obtain all totals for a specific campaign.
campaign_report_unopen_list | View unopens for a specific campaign.
campaign_report_unsubscription_list | View unsubscriptions for a specific campaign.
campaign_report_unsubscription_totals | Obtain unsubscription totals for a specific campaign.
campaign_send | Send a campaign.
campaign_status | Set a campaign's status.
contact_add | Add new contact.
contact_automation_list | View automations for a contact
contact_delete | Delete existing contact.
contact_delete_list | Delete multiple existing contacts.
contact_edit | Edit existing contact.
contact_list | View multiple (a list of) contacts.
contact_note_add | Add a new contact note.
contact_note_delete | Delete contact note.
contact_note_edit | Edit a contact note.
contact_paginator | View a list of existing contacts using pagination, much like it appears in the standard user interface.
contact_sync | Sync a contact.
contact_tag_add | Add new tags to a contact.
contact_tag_remove | Remove tags from a contact.
contact_view | View a single contact.
contact_view_email | View a single contact by looking up their email address.
contact_view_hash | View a single contact by looking up their hash.
deal_add | Add new deal.
deal_delete | Delete deal.
deal_edit | Update deal.
deal_get | Get a deal.
deal_list | View multiple (a list of) deals.
deal_note_add | Add new deal note.
deal_note_edit | Update deal note.
deal_pipeline_add | Add new deal pipeline.
deal_pipeline_delete | Delete deal pipeline.
deal_pipeline_edit | Update deal pipeline.
deal_pipeline_list | View multiple (a list of) deal pipelines.
deal_stage_add | Add new deal stage.
deal_stage_delete | Delete deal stage.
deal_stage_edit | Update deal stage.
deal_stage_list | View multiple (a list of) deal stages.
deal_task_add | Add new deal task.
deal_task_edit | Update deal task.
deal_tasktype_add | Add new deal task type.
deal_tasktype_delete | Delete deal task type.
deal_tasktype_edit | Update deal task type.
form_getforms | View all forms.
form_html | View a specific subscription form.
group_add | Add new User Group.
group_delete | Delete existing User Group.
group_delete_list | Delete multiple User Groups.
group_edit | Edit an existing User Group.
group_list | View many User Groups.
group_view | View a specific User Group.
list_add | Add new mailing list.
list_delete | Delete existing mailing list.
list_delete_list | Delete multiple existing mailing lists.
list_edit | Edit existing mailing list.
list_field_add | Add new contact custom field.
list_field_delete | Delete existing contact custom field.
list_field_edit | Modify existing contact custom field.
list_field_view | View contact custom fields (no data).
list_list | View multiple mailing lists.
list_paginator | View many existing mailing lists using pagination, much like it appears in the standard user interface.
list_view | View a specific mailing list.
message_add | Add new email message.
message_delete | Delete existing email message.
message_delete_list | Delete multiple existing email messages.
message_edit | Edit existing email message.
message_list | View multiple (a list of) email messages.
message_template_add | Add new basic message template.
message_template_delete | Delete existing basic message template.
message_template_delete_list | Delete multiple basic template.
message_template_edit | Edit an existing basic message template.
message_template_export | Export basic message template.
message_template_import | Import basic message template.
message_template_list | View multiple (a list of) basic message templates.
message_template_view | View a single basic message template.
message_view | View a single email message.
organization_list | View multiple (a list of) contact organizations.
settings_edit | Edit general software settings
singlesignon | Utilize Single Sign-On.
track_event_add | Add event tracking event name and value
track_event_delete |  Developers Portal 
track_event_list |  Developers Portal 
track_event_status_edit |  Developers Portal 
track_site_list |  Developers Portal 
track_site_status_edit |  Developers Portal 
track_site_whitelist_add |  Developers Portal 
track_site_whitelist_delete |  Developers Portal 
user_add | Add new user.
user_delete | Delete existing user.
user_delete_list | Delete multiple existing users.
user_edit | Edit existing user.
user_list | View multiple (a list of) users.
user_me | View user information.
user_view | View a single user.
user_view_email | View a single user by looking up their email address.
user_view_username | View a single user by looking up their username.
webhook_add | Add new webhook.
webhook_delete | Delete existing webhook.
webhook_edit | Edit existing webhook.
webhook_events | Webhook event types
webhook_list | View a list of webhooks.
webhook_view | View a single webhook.

### ansible pack

![ansible icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/ansible/icon.png)

#### Actions

Name | Description
---- | -----------
command | Run ad-hoc ansible command (module)
command_local | Run ad-hoc ansible command (module) on local machine
galaxy.install | Download & Install role from ansible galaxy
galaxy.list | Display a list of installed roles from ansible galaxy
galaxy.remove | Remove an installed from ansible galaxy role
playbook | Run ansible playbook
vault.decrypt | Decrypt ansible data files
vault.encrypt | Encrypt ansible data files

### aws pack

![aws icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/aws/icon.png)

#### Sensors

Name | Description
---- | -----------
AWSSQSSensor | Sensor which monitors a SQS queue for new messages
ServiceNotificationsSensor | Sensor which exposes an HTTP interface and listens for AWS service notifications delivered via AWS SNS

#### Actions

Name | Description
---- | -----------
cf_build_base_http_request | 
cf_build_complex_list_params | 
cf_build_list_params | 
cf_cancel_update_stack | 
cf_close | 
cf_create_stack | 
cf_delete_stack | 
cf_describe_stack_events | 
cf_describe_stack_resource | 
cf_describe_stack_resources | 
cf_describe_stacks | 
cf_encode_bool | 
cf_estimate_template_cost | 
cf_get_http_connection | 
cf_get_list | 
cf_get_object | 
cf_get_path | 
cf_get_proxy_auth_header | 
cf_get_proxy_url_with_auth | 
cf_get_stack_policy | 
cf_get_status | 
cf_get_template | 
cf_get_utf8_value | 
cf_handle_proxy | 
cf_list_stack_resources | 
cf_list_stacks | 
cf_make_request | 
cf_new_http_connection | 
cf_prefix_proxy_to_path | 
cf_proxy_ssl | 
cf_put_http_connection | 
cf_server_name | 
cf_set_host_header | 
cf_set_request_hook | 
cf_set_stack_policy | 
cf_skip_proxy | 
cf_update_stack | 
cf_validate_template | 
create_vm | Create a VM, add DNS to Route53
destroy_vm | Destroys a VM and removes it from Route53
ec2_allocate_address | 
ec2_assign_private_ip_addresses | 
ec2_associate_address | 
ec2_associate_address_object | 
ec2_attach_network_interface | 
ec2_attach_volume | 
ec2_authorize_security_group | 
ec2_authorize_security_group_deprecated | 
ec2_authorize_security_group_egress | 
ec2_build_base_http_request | 
ec2_build_complex_list_params | 
ec2_build_configurations_param_list | 
ec2_build_filter_params | 
ec2_build_list_params | 
ec2_build_tag_param_list | 
ec2_bundle_instance | 
ec2_cancel_bundle_task | 
ec2_cancel_reserved_instances_listing | 
ec2_cancel_spot_instance_requests | 
ec2_close | 
ec2_confirm_product_instance | 
ec2_copy_image | 
ec2_copy_snapshot | 
ec2_create_image | 
ec2_create_key_pair | 
ec2_create_network_interface | 
ec2_create_placement_group | 
ec2_create_reserved_instances_listing | 
ec2_create_security_group | 
ec2_create_snapshot | 
ec2_create_spot_datafeed_subscription | 
ec2_create_tags | 
ec2_create_volume | 
ec2_delete_key_pair | 
ec2_delete_network_interface | 
ec2_delete_placement_group | 
ec2_delete_security_group | 
ec2_delete_snapshot | 
ec2_delete_spot_datafeed_subscription | 
ec2_delete_tags | 
ec2_delete_volume | 
ec2_deregister_image | 
ec2_describe_account_attributes | 
ec2_describe_reserved_instances_modifications | 
ec2_describe_vpc_attribute | 
ec2_detach_network_interface | 
ec2_detach_volume | 
ec2_disassociate_address | 
ec2_enable_volume_io | 
ec2_get_all_addresses | 
ec2_get_all_bundle_tasks | 
ec2_get_all_classic_link_instances | 
ec2_get_all_images | 
ec2_get_all_instance_status | 
ec2_get_all_instance_types | 
ec2_get_all_instances | 
ec2_get_all_kernels | 
ec2_get_all_key_pairs | 
ec2_get_all_network_interfaces | 
ec2_get_all_placement_groups | 
ec2_get_all_ramdisks | 
ec2_get_all_regions | 
ec2_get_all_reservations | 
ec2_get_all_reserved_instances | 
ec2_get_all_reserved_instances_offerings | 
ec2_get_all_security_groups | 
ec2_get_all_snapshots | 
ec2_get_all_spot_instance_requests | 
ec2_get_all_tags | 
ec2_get_all_volume_status | 
ec2_get_all_volumes | 
ec2_get_all_zones | 
ec2_get_console_output | 
ec2_get_http_connection | 
ec2_get_image | 
ec2_get_image_attribute | 
ec2_get_instance_attribute | 
ec2_get_key_pair | 
ec2_get_list | 
ec2_get_object | 
ec2_get_only_instances | 
ec2_get_params | 
ec2_get_password_data | 
ec2_get_path | 
ec2_get_proxy_auth_header | 
ec2_get_proxy_url_with_auth | 
ec2_get_snapshot_attribute | 
ec2_get_spot_datafeed_subscription | 
ec2_get_spot_price_history | 
ec2_get_status | 
ec2_get_utf8_value | 
ec2_get_volume_attribute | 
ec2_handle_proxy | 
ec2_import_key_pair | 
ec2_make_request | 
ec2_modify_image_attribute | 
ec2_modify_instance_attribute | 
ec2_modify_network_interface_attribute | 
ec2_modify_reserved_instances | 
ec2_modify_snapshot_attribute | 
ec2_modify_volume_attribute | 
ec2_modify_vpc_attribute | 
ec2_monitor_instance | 
ec2_monitor_instances | 
ec2_new_http_connection | 
ec2_prefix_proxy_to_path | 
ec2_proxy_ssl | 
ec2_purchase_reserved_instance_offering | 
ec2_put_http_connection | 
ec2_reboot_instances | 
ec2_register_image | 
ec2_release_address | 
ec2_request_spot_instances | 
ec2_reset_image_attribute | 
ec2_reset_instance_attribute | 
ec2_reset_snapshot_attribute | 
ec2_revoke_security_group | 
ec2_revoke_security_group_deprecated | 
ec2_revoke_security_group_egress | 
ec2_run_instances | 
ec2_server_name | 
ec2_set_host_header | 
ec2_set_request_hook | 
ec2_skip_proxy | 
ec2_start_instances | 
ec2_stop_instances | 
ec2_terminate_instances | 
ec2_trim_snapshots | 
ec2_unassign_private_ip_addresses | 
ec2_unmonitor_instance | 
ec2_unmonitor_instances | 
ec2_wait_for_state | 
iam_add_role_to_instance_profile | 
iam_add_user_to_group | 
iam_build_base_http_request | 
iam_build_complex_list_params | 
iam_build_list_params | 
iam_close | 
iam_create_access_key | 
iam_create_account_alias | 
iam_create_group | 
iam_create_instance_profile | 
iam_create_login_profile | 
iam_create_role | 
iam_create_saml_provider | 
iam_create_user | 
iam_create_virtual_mfa_device | 
iam_deactivate_mfa_device | 
iam_delete_access_key | 
iam_delete_account_alias | 
iam_delete_account_password_policy | 
iam_delete_group | 
iam_delete_group_policy | 
iam_delete_instance_profile | 
iam_delete_login_profile | 
iam_delete_role | 
iam_delete_role_policy | 
iam_delete_saml_provider | 
iam_delete_server_cert | 
iam_delete_signing_cert | 
iam_delete_user | 
iam_delete_user_policy | 
iam_enable_mfa_device | 
iam_generate_credential_report | 
iam_get_account_alias | 
iam_get_account_password_policy | 
iam_get_account_summary | 
iam_get_all_access_keys | 
iam_get_all_group_policies | 
iam_get_all_groups | 
iam_get_all_mfa_devices | 
iam_get_all_server_certs | 
iam_get_all_signing_certs | 
iam_get_all_user_policies | 
iam_get_all_users | 
iam_get_credential_report | 
iam_get_group | 
iam_get_group_policy | 
iam_get_groups_for_user | 
iam_get_http_connection | 
iam_get_instance_profile | 
iam_get_list | 
iam_get_login_profiles | 
iam_get_object | 
iam_get_path | 
iam_get_proxy_auth_header | 
iam_get_proxy_url_with_auth | 
iam_get_response | 
iam_get_role | 
iam_get_role_policy | 
iam_get_saml_provider | 
iam_get_server_certificate | 
iam_get_signin_url | 
iam_get_status | 
iam_get_user | 
iam_get_user_policy | 
iam_get_utf8_value | 
iam_handle_proxy | 
iam_list_instance_profiles | 
iam_list_instance_profiles_for_role | 
iam_list_role_policies | 
iam_list_roles | 
iam_list_saml_providers | 
iam_list_server_certs | 
iam_make_request | 
iam_new_http_connection | 
iam_prefix_proxy_to_path | 
iam_proxy_ssl | 
iam_put_group_policy | 
iam_put_http_connection | 
iam_put_role_policy | 
iam_put_user_policy | 
iam_remove_role_from_instance_profile | 
iam_remove_user_from_group | 
iam_resync_mfa_device | 
iam_server_name | 
iam_set_host_header | 
iam_set_request_hook | 
iam_skip_proxy | 
iam_update_access_key | 
iam_update_account_password_policy | 
iam_update_assume_role_policy | 
iam_update_group | 
iam_update_login_profile | 
iam_update_saml_provider | 
iam_update_server_cert | 
iam_update_signing_cert | 
iam_update_user | 
iam_upload_server_cert | 
iam_upload_signing_cert | 
r53_build_base_http_request | 
r53_change_rrsets | 
r53_close | 
r53_create_health_check | 
r53_create_hosted_zone | 
r53_create_zone | 
r53_delete_health_check | 
r53_delete_hosted_zone | 
r53_get_all_hosted_zones | 
r53_get_all_rrsets | 
r53_get_change | 
r53_get_checker_ip_ranges | 
r53_get_hosted_zone | 
r53_get_hosted_zone_by_name | 
r53_get_http_connection | 
r53_get_list_health_checks | 
r53_get_path | 
r53_get_proxy_auth_header | 
r53_get_proxy_url_with_auth | 
r53_get_zone | 
r53_get_zones | 
r53_handle_proxy | 
r53_make_request | 
r53_new_http_connection | 
r53_prefix_proxy_to_path | 
r53_proxy_ssl | 
r53_put_http_connection | 
r53_server_name | 
r53_set_host_header | 
r53_set_request_hook | 
r53_skip_proxy | 
r53_zone_add_a | 
r53_zone_add_cname | 
r53_zone_add_mx | 
r53_zone_add_record | 
r53_zone_delete | 
r53_zone_delete_a | 
r53_zone_delete_cname | 
r53_zone_delete_mx | 
r53_zone_delete_record | 
r53_zone_find_records | 
r53_zone_get_a | 
r53_zone_get_cname | 
r53_zone_get_mx | 
r53_zone_get_nameservers | 
r53_zone_get_records | 
r53_zone_update_a | 
r53_zone_update_cname | 
r53_zone_update_mx | 
r53_zone_update_record | 
rds_authorize_dbsecurity_group | 
rds_build_base_http_request | 
rds_build_complex_list_params | 
rds_build_list_params | 
rds_close | 
rds_copy_dbsnapshot | 
rds_create_db_subnet_group | 
rds_create_dbinstance | 
rds_create_dbinstance_read_replica | 
rds_create_dbsecurity_group | 
rds_create_dbsnapshot | 
rds_create_option_group | 
rds_create_parameter_group | 
rds_delete_db_subnet_group | 
rds_delete_dbinstance | 
rds_delete_dbsecurity_group | 
rds_delete_dbsnapshot | 
rds_delete_option_group | 
rds_delete_parameter_group | 
rds_describe_option_group_options | 
rds_describe_option_groups | 
rds_get_all_db_subnet_groups | 
rds_get_all_dbinstances | 
rds_get_all_dbparameter_groups | 
rds_get_all_dbparameters | 
rds_get_all_dbsecurity_groups | 
rds_get_all_dbsnapshots | 
rds_get_all_events | 
rds_get_all_logs | 
rds_get_http_connection | 
rds_get_list | 
rds_get_log_file | 
rds_get_object | 
rds_get_path | 
rds_get_proxy_auth_header | 
rds_get_proxy_url_with_auth | 
rds_get_status | 
rds_get_utf8_value | 
rds_handle_proxy | 
rds_make_request | 
rds_modify_db_subnet_group | 
rds_modify_dbinstance | 
rds_modify_parameter_group | 
rds_new_http_connection | 
rds_prefix_proxy_to_path | 
rds_promote_read_replica | 
rds_proxy_ssl | 
rds_put_http_connection | 
rds_reboot_dbinstance | 
rds_reset_parameter_group | 
rds_restore_dbinstance_from_dbsnapshot | 
rds_restore_dbinstance_from_point_in_time | 
rds_revoke_dbsecurity_group | 
rds_revoke_security_group | 
rds_server_name | 
rds_set_host_header | 
rds_set_request_hook | 
rds_skip_proxy | 
s3_build_base_http_request | 
s3_build_post_form_args | 
s3_build_post_policy | 
s3_close | 
s3_create_bucket | 
s3_delete_bucket | 
s3_generate_url | 
s3_generate_url_sigv4 | 
s3_get_all_buckets | 
s3_get_bucket | 
s3_get_canonical_user_id | 
s3_get_http_connection | 
s3_get_path | 
s3_get_proxy_auth_header | 
s3_get_proxy_url_with_auth | 
s3_handle_proxy | 
s3_head_bucket | 
s3_lookup | 
s3_make_request | 
s3_new_http_connection | 
s3_prefix_proxy_to_path | 
s3_proxy_ssl | 
s3_put_http_connection | 
s3_server_name | 
s3_set_bucket_class | 
s3_set_host_header | 
s3_set_request_hook | 
s3_skip_proxy | 
set_hostname_cloud | Set the hostname on a VM and update cloud.cfg
sqs_add_permission | 
sqs_build_base_http_request | 
sqs_build_complex_list_params | 
sqs_build_list_params | 
sqs_change_message_visibility | 
sqs_change_message_visibility_batch | 
sqs_close | 
sqs_create_queue | 
sqs_delete_message | 
sqs_delete_message_batch | 
sqs_delete_message_from_handle | 
sqs_delete_queue | 
sqs_get_all_queues | 
sqs_get_dead_letter_source_queues | 
sqs_get_http_connection | 
sqs_get_list | 
sqs_get_object | 
sqs_get_path | 
sqs_get_proxy_auth_header | 
sqs_get_proxy_url_with_auth | 
sqs_get_queue | 
sqs_get_queue_attributes | 
sqs_get_status | 
sqs_get_utf8_value | 
sqs_handle_proxy | 
sqs_lookup | 
sqs_make_request | 
sqs_new_http_connection | 
sqs_prefix_proxy_to_path | 
sqs_proxy_ssl | 
sqs_purge_queue | 
sqs_put_http_connection | 
sqs_receive_message | 
sqs_remove_permission | 
sqs_send_message | 
sqs_send_message_batch | 
sqs_server_name | 
sqs_set_host_header | 
sqs_set_queue_attribute | 
sqs_set_request_hook | 
sqs_skip_proxy | 
vpc_accept_vpc_peering_connection | 
vpc_allocate_address | 
vpc_assign_private_ip_addresses | 
vpc_associate_address | 
vpc_associate_address_object | 
vpc_associate_dhcp_options | 
vpc_associate_network_acl | 
vpc_associate_route_table | 
vpc_attach_classic_link_vpc | 
vpc_attach_internet_gateway | 
vpc_attach_network_interface | 
vpc_attach_volume | 
vpc_attach_vpn_gateway | 
vpc_authorize_security_group | 
vpc_authorize_security_group_deprecated | 
vpc_authorize_security_group_egress | 
vpc_build_base_http_request | 
vpc_build_complex_list_params | 
vpc_build_configurations_param_list | 
vpc_build_filter_params | 
vpc_build_list_params | 
vpc_build_tag_param_list | 
vpc_bundle_instance | 
vpc_cancel_bundle_task | 
vpc_cancel_reserved_instances_listing | 
vpc_cancel_spot_instance_requests | 
vpc_close | 
vpc_confirm_product_instance | 
vpc_copy_image | 
vpc_copy_snapshot | 
vpc_create_customer_gateway | 
vpc_create_dhcp_options | 
vpc_create_image | 
vpc_create_internet_gateway | 
vpc_create_key_pair | 
vpc_create_network_acl | 
vpc_create_network_acl_entry | 
vpc_create_network_interface | 
vpc_create_placement_group | 
vpc_create_reserved_instances_listing | 
vpc_create_route | 
vpc_create_route_table | 
vpc_create_security_group | 
vpc_create_snapshot | 
vpc_create_spot_datafeed_subscription | 
vpc_create_subnet | 
vpc_create_tags | 
vpc_create_volume | 
vpc_create_vpc | 
vpc_create_vpc_peering_connection | 
vpc_create_vpn_connection | 
vpc_create_vpn_connection_route | 
vpc_create_vpn_gateway | 
vpc_delete_customer_gateway | 
vpc_delete_dhcp_options | 
vpc_delete_internet_gateway | 
vpc_delete_key_pair | 
vpc_delete_network_acl | 
vpc_delete_network_acl_entry | 
vpc_delete_network_interface | 
vpc_delete_placement_group | 
vpc_delete_route | 
vpc_delete_route_table | 
vpc_delete_security_group | 
vpc_delete_snapshot | 
vpc_delete_spot_datafeed_subscription | 
vpc_delete_subnet | 
vpc_delete_tags | 
vpc_delete_volume | 
vpc_delete_vpc | 
vpc_delete_vpc_peering_connection | 
vpc_delete_vpn_connection | 
vpc_delete_vpn_connection_route | 
vpc_delete_vpn_gateway | 
vpc_deregister_image | 
vpc_describe_account_attributes | 
vpc_describe_reserved_instances_modifications | 
vpc_describe_vpc_attribute | 
vpc_detach_classic_link_vpc | 
vpc_detach_internet_gateway | 
vpc_detach_network_interface | 
vpc_detach_volume | 
vpc_detach_vpn_gateway | 
vpc_disable_vgw_route_propagation | 
vpc_disable_vpc_classic_link | 
vpc_disassociate_address | 
vpc_disassociate_network_acl | 
vpc_disassociate_route_table | 
vpc_enable_vgw_route_propagation | 
vpc_enable_volume_io | 
vpc_enable_vpc_classic_link | 
vpc_get_all_addresses | 
vpc_get_all_bundle_tasks | 
vpc_get_all_classic_link_instances | 
vpc_get_all_classic_link_vpcs | 
vpc_get_all_customer_gateways | 
vpc_get_all_dhcp_options | 
vpc_get_all_images | 
vpc_get_all_instance_status | 
vpc_get_all_instance_types | 
vpc_get_all_instances | 
vpc_get_all_internet_gateways | 
vpc_get_all_kernels | 
vpc_get_all_key_pairs | 
vpc_get_all_network_acls | 
vpc_get_all_network_interfaces | 
vpc_get_all_placement_groups | 
vpc_get_all_ramdisks | 
vpc_get_all_regions | 
vpc_get_all_reservations | 
vpc_get_all_reserved_instances | 
vpc_get_all_reserved_instances_offerings | 
vpc_get_all_route_tables | 
vpc_get_all_security_groups | 
vpc_get_all_snapshots | 
vpc_get_all_spot_instance_requests | 
vpc_get_all_subnets | 
vpc_get_all_tags | 
vpc_get_all_volume_status | 
vpc_get_all_volumes | 
vpc_get_all_vpc_peering_connections | 
vpc_get_all_vpcs | 
vpc_get_all_vpn_connections | 
vpc_get_all_vpn_gateways | 
vpc_get_all_zones | 
vpc_get_console_output | 
vpc_get_http_connection | 
vpc_get_image | 
vpc_get_image_attribute | 
vpc_get_instance_attribute | 
vpc_get_key_pair | 
vpc_get_list | 
vpc_get_object | 
vpc_get_only_instances | 
vpc_get_params | 
vpc_get_password_data | 
vpc_get_path | 
vpc_get_proxy_auth_header | 
vpc_get_proxy_url_with_auth | 
vpc_get_snapshot_attribute | 
vpc_get_spot_datafeed_subscription | 
vpc_get_spot_price_history | 
vpc_get_status | 
vpc_get_utf8_value | 
vpc_get_volume_attribute | 
vpc_handle_proxy | 
vpc_import_key_pair | 
vpc_make_request | 
vpc_modify_image_attribute | 
vpc_modify_instance_attribute | 
vpc_modify_network_interface_attribute | 
vpc_modify_reserved_instances | 
vpc_modify_snapshot_attribute | 
vpc_modify_volume_attribute | 
vpc_modify_vpc_attribute | 
vpc_monitor_instance | 
vpc_monitor_instances | 
vpc_new_http_connection | 
vpc_prefix_proxy_to_path | 
vpc_proxy_ssl | 
vpc_purchase_reserved_instance_offering | 
vpc_put_http_connection | 
vpc_reboot_instances | 
vpc_register_image | 
vpc_reject_vpc_peering_connection | 
vpc_release_address | 
vpc_replace_network_acl_entry | 
vpc_replace_route | 
vpc_replace_route_table_assocation | 
vpc_replace_route_table_association_with_assoc | 
vpc_request_spot_instances | 
vpc_reset_image_attribute | 
vpc_reset_instance_attribute | 
vpc_reset_snapshot_attribute | 
vpc_revoke_security_group | 
vpc_revoke_security_group_deprecated | 
vpc_revoke_security_group_egress | 
vpc_run_instances | 
vpc_server_name | 
vpc_set_host_header | 
vpc_set_request_hook | 
vpc_skip_proxy | 
vpc_start_instances | 
vpc_stop_instances | 
vpc_terminate_instances | 
vpc_trim_snapshots | 
vpc_unassign_private_ip_addresses | 
vpc_unmonitor_instance | 
vpc_unmonitor_instances | 

### azure pack

![azure icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/azure/icon.png)

#### Actions

Name | Description
---- | -----------
create_container | Create a new storage container.
create_linked_resource_url | Create a new ARM Linked Resource from a URI.
create_resource | Create a new ARM Generic Resource.
create_vm | Create a new VM.
delete_container | Delete a storage container.
delete_object | Delete an object.
destroy_vm | Destroy a VM.
list_container_objects | List storage objects for the provided container.
list_containers | List storage containers.
list_resource_groups | List ARM resource group names
list_vms | List available VMs.
reboot_vm | Reboot a running VM.
upload_file | Upload a file to the provided container.

### bitbucket pack

![bitbucket icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/bitbucket/icon.png)

#### Actions

Name | Description
---- | -----------
archive_repo | Retruns a path to the downloaded archived repository
associate_ssh_key | Associate a SSH key with your account
create_issue | Create an issue
create_repo | Create a Repository
create_service | Create a service/hook for a given repository
delete_issues | Delete issue for a given repository
delete_repo | Delete a Repository
delete_services | Delete services for a given repository.
delete_ssh_key | Delete SSH key
list_branches | List all branches for a given repository
list_issues | List all issues for a given repository
list_repos | List details of repositories for a user
list_services | List all services for a given repository
list_ssh_keys | List all SSH keys for a user
update_issue | Update issue for a given repository
update_service | Update hook/service for a given repository

### bitcoin pack

![bitcoin icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/bitcoin/icon.png)

#### Actions

Name | Description
---- | -----------
getaccountaddress | Retrieves address of local wallet.
getwalletinfo | Information of the local wallet.
sendtoaddresss | Send some BTC to supplied address.

### cassandra pack

![cassandra icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/cassandra/icon.png)

#### Actions

Name | Description
---- | -----------
append_replace_address_env_file | Appends replace.address JVM OPT to cassandra env file.
clear_cass_data | Clear cassandra data directory.
get_dse_status | Get DSE cassandra service status.
is_seed_node | Find whether given node is a seed node.
list_seed_nodes | List seed nodes in cassandra config.
nodetool | Cassandra nodetool wrapper.
remove_gossip_peer_info | Remove gossip peer info data from cassandra nodes.
remove_replace_address_env_file | Remove replace.address JVM OPT from cassandra env file.
replace_host | Cassandra replace host workflow.
start_dse | Start DSE cassandra service.
stop_dse | Stop DSE cassandra service.
wait_for_port_open | Find whether given node is a seed node.

### chef pack

![chef icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/chef/icon.png)

#### Actions

Name | Description
---- | -----------
apply | Performs one-off resource converge on remote hosts.
client | Performs chef-client run on remote hosts.
install | Performs installation of chef-client on remote nodes
ohai | Performs chef-solo run on remote hosts.
solo | Performs chef-solo run on remote hosts.

### circle_ci pack

![circle_ci icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/circle_ci/icon.png)

#### Actions

Name | Description
---- | -----------
get_build_number | Get build number for given SHA.
wait_until_build_finishes | Wait until build finishes.

### consul pack

![consul icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/consul/icon.png)

#### Actions

Name | Description
---- | -----------
get | Get value from Consul server
list_datacenters | Real-time query of all known datacenters in Consul
list_nodes | Real-time query of all known nodes in Consul
list_services | Real-time query of all known services in Consul
parse_nodes | Helper function to extract hosts from a consul response to be used with StackStorm workflows
put | Put value in Consul server
query_node | Query details about a node in consul
query_service | Query details about a service in consul

### csv pack

![csv icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/csv/icon.png)

#### Actions

Name | Description
---- | -----------
parse | Parse CSV string and return JSON object.

### cubesensors pack

![cubesensors icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/cubesensors/icon.png)

#### Sensors

Name | Description
---- | -----------
CubeSensorsMeasurementsSensor | Sensor which polls CubeSensors API for new measurements and dispatch a trigger every time a new measurement is detected.

#### Actions

Name | Description
---- | -----------
get_device | Retrieve details for a particular device (cube).
get_measurements | Retrieve current measurements for a particular device (cube).
list_devices | List information about all the available devices (cubes).

### digitalocean pack

![digitalocean icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/digitalocean/icon.png)

#### Actions

Name | Description
---- | -----------
get_action | 
get_all_domains | 
get_all_droplets | 
get_all_images | 
get_all_regions | 
get_all_sizes | 
get_all_sshkeys | 
get_data | 
get_domain | 
get_droplet | 
get_global_images | 
get_image | 
get_my_images | 
get_ssh_key | 

### dimensiondata pack

![dimensiondata icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/dimensiondata/icon.png)

#### Actions

Name | Description
---- | -----------
add_storage_to_vm | Add another disk to the VM
attach_node_to_vlan | Attach a VM to a VLAN
balancer_attach_member | Attach a member to a load balancer
balancer_delete_node | Delete a node
balancer_detach_member | Detach a member to a load balancer
balancer_list_members | List members of a load balancer
clone_vm_to_image | Clone a VM to a customer image
configure | Configure the pack
create_balancer | Create a load balancer
create_firewall_rule | Create a firewall (ACL) rule in a network domain
create_nat_rule | Create a NAT rule in a network domain
create_network | Create a network
create_network_domain | Create a network domain
create_pool_member | add member to a pool
create_public_ip_block | Create a public IP block in a network domain
create_vip_node | Create node in the network domain
create_vlan | Create a VLAN
create_vm_mcp1 | Create a VM on MCP 1 datacenter
create_vm_mcp2 | Create a VM on MCP 2 datacenter
delete_network | Delete a network
delete_network_domain | Delete a network domain
delete_vlan | Delete a VLAN
delete_vlan | Get a VLAN
destroy_nic | Delete (remove) a NIC from a VM
destroy_vm | Destroy a virtual machine
disable_monitoring | Enable monitoring on a node
enable_monitoring | Enable monitoring on a node
get_balancer | Get a specific load balancer by ID
get_balancer_by_name | Get an balancer by name
get_image | Get an image by ID
get_image_by_name | Get an image by name
get_ipv6_address_of_vm | get ipv6 address of vm
get_location_by_id | Get a location (DC) by ID e.g. NA1
get_network_by_name | Get an network by name
get_network_domain | Get a network domain
get_network_domain_by_name | Get an network domain by name
get_public_ip_block | Get a public IP block
get_vlan_by_name | Get vlan by name
get_vm | Get a VM by ID
get_vm_by_name | Get a VM by name
list_balancer_nodes | List the load balancer nodes
list_balancers | List the load balancers available
list_customer_images | List the images available
list_default_health_monitors | List the default health monitors
list_firewall_rules | List the firewall rules in a network domain
list_images | List the customer images available
list_locations | List the locations available
list_nat_rules | List NAT rules in a network domain
list_network_domains | List the network domains available
list_networks | List the networks available
list_pool_members | List the members of a load balancer pool
list_public_ip_blocks | List the public IP blocks in a network domain
list_vlans | List the VLANs available
list_vms | List the Virtual Machines available
power_off_vm | Power Off a virtual machine
reboot_vm | Reboot a virtual machine
reconfigure_vm | Reconfigure the virtual hardware specification of a node
remove_storage_from_vm | Remove disk from VM
reset_vm | Reset a virtual machine
shutdown_vm | Shutdown a virtual machine
start_vm | Start a virtual machine
update_disk_size | Update the size of a disk
update_disk_speed | Update the speed of a disk
update_monitoring_plan | Update monitoring plan on a node
update_vm | Update VM specification, name or description
update_vm_tools | Update VMware tools on a node
wait_for_server_operation | wait for the server operation to complete

### docker pack

![docker icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/docker/icon.png)

#### Sensors

Name | Description
---- | -----------
DockerSensor | Docker sensor

#### Actions

Name | Description
---- | -----------
build_image | Build docker image action. Equivalent to docker build.
pull_image | Pull docker image action. Equivalent to docker pull.
push_image | Push docker image action. Equivalent to docker push.

### dripstat pack

![dripstat icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/dripstat/icon.png)

#### Sensors

Name | Description
---- | -----------
DripstatAlertSensor | Sensor which monitors Dripstat API for active alerts

### elasticsearch pack

![elasticsearch icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/elasticsearch/icon.png)

#### Actions

Name | Description
---- | -----------
indices.alias | Index Aliasing
indices.allocation | Index Allocation
indices.bloom | Disable bloom filter cache
indices.close | Close indices
indices.delete | Delete indices
indices.open | Open indices
indices.optimize | Optimize indices
indices.replicas | Replica Count Per-shard
indices.show | Show indices
indices.snapshot | Create snapshot of indices
search.body | Search query (full body)
search.q | Search query (lucene syntax)
snapshots.delete | Delete snapshots
snapshots.show | Show snapshots

### email pack

![email icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/email/icon.png)

#### Sensors

Name | Description
---- | -----------
IMAPSensor | Sensor that emits triggers when e-mail message is received via IMAP
SMTPSensor | Sensor that emits triggers when e-mail message is received via SMTP

#### Actions

Name | Description
---- | -----------
send_email | Send an email.

### fireeye pack

![fireeye icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/fireeye/icon.png)

#### Actions

Name | Description
---- | -----------
get_alert_query | Request existing alert profiles with optional filters
get_submission_results | Query results of completed job
get_submission_status | Query status of running job
submit_malware | Submit a Malware object to FireEye AX appliance
view_ax_config | Returns a list of profiles and applications on AX devices

### fpm pack

![fpm icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/fpm/icon.png)

#### Actions

Name | Description
---- | -----------
create_deb_from_deb | Create a deb package from deb with fpm
create_deb_from_dir | Create a deb package from dir with fpm
create_deb_from_empty | Create a deb package from empty with fpm
create_deb_from_gem | Create a deb package from gem with fpm
create_deb_from_python | Create a deb package from python with fpm
create_deb_from_rpm | Create a deb package from rpm with fpm
create_deb_from_tar | Create a deb package from tar with fpm
create_rpm_from_deb | Create a rpm package from deb with fpm
create_rpm_from_dir | Create a rpm package from dir with fpm
create_rpm_from_empty | Create a rpm package from empty with fpm
create_rpm_from_gem | Create a rpm package from gem with fpm
create_rpm_from_python | Create a rpm package from python with fpm
create_rpm_from_rpm | Create a rpm package from rpm with fpm
create_rpm_from_tar | Create a rpm package from tar with fpm
load_metadata | Load package metadata from directory

### freight pack

![freight icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/freight/icon.png)

#### Actions

Name | Description
---- | -----------
add_package | Add package to the Freight cache
update_cache | Update the Freight cache and regenerate the repository

### git pack

![git icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/git/icon.png)

#### Sensors

Name | Description
---- | -----------
GitCommitSensor | Sensor which monitors git repository for new commits

#### Actions

Name | Description
---- | -----------
clone | Clone a repository
get_local_repo_latest_commit | Retrieve SHA of the latest commit for the provided branch in a local repository.
get_remote_repo_latest_commit | Retrieve SHA of the latest commit for the provided branch in a remote repository.

### github pack

![github icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/github/icon.png)

#### Sensors

Name | Description
---- | -----------
GithubRepositorySensor | Sensor which monitors Github repository for activity

#### Actions

Name | Description
---- | -----------
add_comment | Add a comment to the provided issue / pull request.
add_status | Add a commit status for a provided ref.
add_team_membership | Add (and invite if not a member) a user to a team
create_issue | Create a Github issue.
get_clone_stats | Retrieve clone statistics for a given repository
get_issue | Retrieve information about a particular Github issue.
get_traffic_stats | Retrieve traffic statistics for a given repository
get_user | Get a user from the Github user database
list_issues | Retrieve a list of issues (including pull requests) for a particular repository.
list_teams | List teams in organization

### google pack

![google icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/google/icon.png)

#### Actions

Name | Description
---- | -----------
get_search_results | Retrieve Google search results for the provided query.

### gpg pack

![gpg icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/gpg/icon.png)

#### Actions

Name | Description
---- | -----------
decrypt_file | Decrypt asymmetrically encrypted GPG file.
encrypt_file | Encrypt a file using asymmetric encryption for the provided recipients.
import_keys | Import keys into the keyring.
list_keys | List all keys in the keyring.

### hubot pack

![hubot icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/hubot/icon.png)

#### Actions

Name | Description
---- | -----------
branch | Determine which branch Hubot is currently running
deploy | Manage Hubot installs on a per-pack basis
post_message | Post a message to Hubot
post_result | Post an execution result to Hubot
restart | Restart hubot
update_ref | Manage Hubot installs on a per-pack basis

### hue pack

![hue icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/hue/icon.png)

#### Actions

Name | Description
---- | -----------
alert | Send an alert to a light
brightness | Change the brightness of a bulb
color_temp_kelvin | Change the bulb color temperature to a specific temperature in Kelvin
color_temp_mired | Change the bulb color temperature to a specific temperature in mired scale
current_state | Get current state of bridge
find_id_by_name | Find bulb ID based on nickname
list_bulbs | List all registered bulbs
off | Turn off a bulb
on | Turn on a bulb
rgb | Change bulb color based on RGB Values
set_state | Send manual state to bulb
toggle | Toggle on/off state of a bulb
xy | Change bulb color based on CIE color space values

### ipcam pack

![ipcam icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/ipcam/icon.png)

#### Actions

Name | Description
---- | -----------
capture_screenshot | Capture a screenshot of the camera's FOV.

### irc pack

![irc icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/irc/icon.png)

#### Sensors

Name | Description
---- | -----------
IRCSensor | Sensor which monitors IRC and dispatches a trigger for each public and private message

### jenkins pack

![jenkins icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/jenkins/icon.png)

#### Actions

Name | Description
---- | -----------
build_job | Kick off Jenkins Build Jobs
list_running_jobs | List currently running Jenkins jobs

### jira pack

![jira icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/jira/icon.png)

#### Sensors

Name | Description
---- | -----------
JIRASensor | Sensor which monitors JIRA for new tickets

#### Actions

Name | Description
---- | -----------
comment_issue | Comment on a JIRA issue / ticket.
create_issue | Create a new JIRA issue / ticket.
get_issue | Retrieve information about a particular JIRA issue.
transition_issue | Do a transition on a JIRA issue / ticket.

### jmx pack

![jmx icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/jmx/icon.png)

#### Sensors

Name | Description
---- | -----------
JMXSensor | Sensor which monitors Java application for attributes / metrics exposed through JMX protocol

#### Actions

Name | Description
---- | -----------
invoke_method | Invoke a provided MBean method exposed over JMX.

### kubernetes pack

![kubernetes icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/kubernetes/icon.png)

#### Sensors

Name | Description
---- | -----------
ThirdPartyResource | Sensor which watches Kubernetes API for new thirdpartyresource.

#### Actions

Name | Description
---- | -----------
db_create_chain | RDS Create Action Chain Workflow
db_delete_chain | RDS Delete Action Chain Workflow
db_rds_spec | Munge Kubernetes data so we can create a database.

### lastline pack

![lastline icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/lastline/icon.png)

#### Actions

Name | Description
---- | -----------
get_completed | Get artifact generated by an analysis result for a previously submitted analysis task.
get_progress | Get a progress estimate for a previously submitted analysis task.
get_result | Get results for a previously submitted analysis task.
get_result_artifact | Get artifact generated by an analysis result for a previously submitted analysis task.
get_result_summary | Get result summary for a previously submitted analysis task.
submit_file | Submit a file to Lastline for analysis
submit_file_hash | Submit a file hash to Lastline for analysis
submit_url | Submit a URL for analysis to Lastline

### libcloud pack

![libcloud icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/libcloud/icon.png)

#### Actions

Name | Description
---- | -----------
balancer_attach_member | Attach a member to a load balancer
balancer_list_members | List members of a load balancer
create_balancer | Create a load balancer
create_container_cluster | Create a cluster container
create_dns_record | Create a new DNS record.
create_vm | Create a new VM.
delete_dns_record | Delete an existing DNS record.
deploy_container | Deploy a container
destroy_container | Destroy a Container
destroy_vm | Destroy a VM.
enable_cdn_for_container | Enable CDN for container and return the CDN URL
get_container_cdn_url | Retrieve CDN URL for existing CDN enabled container
get_object_cdn_url | Retrieve CDN URL for an object which is stored in a CDN enable container
import_public_ssh_key | Import an existing public SSH key.
list_balancers | List load balancers
list_container_clusters | List container clusters
list_containers | List containers
list_dns_records | List available DNS records for a particular zone.
list_dns_zones | List available zones.
list_images | List available node images.
list_sizes | List available node sizes.
list_vms | List available VMs.
reboot_vm | Reboot a running VM.
restart_container | Restart a container.
start_container | Start a container.
start_vm | Start a new VM.
stop_container | Stop a container.
stop_vm | Stop a running VM.
upload_file | Upload a file to the provided container

### librato pack

![librato icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/librato/icon.png)

#### Actions

Name | Description
---- | -----------
add_annotation | Add an annotation
delete_metric | Delete a metric from Librato
get_metric | Retrieve a metric from Librato
list_metrics | List all metrics setup on Librato
submit_counter | List all metrics setup on Librato
submit_gauge | List all metrics setup on Librato

### mailgun pack

![mailgun icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mailgun/icon.png)

#### Actions

Name | Description
---- | -----------
send_email | Send email via Mailgun HTTP API.

### mistral pack

![mistral icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mistral/icon.png)

#### Actions

Name | Description
---- | -----------
get_task_results | Get results of mistral task in an execution.
get_workbook_definition | Get the definition of the mistral workbook.
get_workflow_results | Get results of mistral workflow.
kill_workflow | Kill a running mistral workflow.

### mmonit pack

![mmonit icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mmonit/icon.png)

#### Sensors

Name | Description
---- | -----------
MmonitEventsSensor | Sensor which monitors mmonit for events

#### Actions

Name | Description
---- | -----------
action_host | Performs the specified action for the selected host services.
delete_host | Returns details for the given host id.
dismiss_event | Dismiss the given active event so it doesn't show up in the event list if active filter is set to 2.
get_event | Returns details for a specific event.
get_host | Returns details for the given host id.
get_status_host | Returns detailed status of the given host.
get_uptime_hosts | Returns services uptime for a particular host.
list_events | Returns a list of events stored in M/Monit.
list_hosts | Returns a list of all hosts registered in M/Monit.
list_status_hosts | Returns the current status of all hosts registered in M/Monit.
list_uptime_hosts | Returns hosts uptime overview. If a custom range is used, the difference between datefrom and dateto should be in minutes, not in seconds since 1 minute is the lowest data resolution in M/Monit.
session_delete | Delete session attributes matching key. If no keys were specified, delete all stored attributes.
session_get | Returns the session attribute matching the session_key argument. If no keys are specified, all stored attributes in the session are returned.
session_put | Add or update the session attribute. If a named attribute already exist, its old value is replaced.
summary_events | Returns the events summary for the last 24 hours.
summary_status | Returns a status summary of all hosts.
test_connection_to_host | Checks that M/Monit can connect to the host with the given network settings.
update_host | Updates the host settings in the M/Monit database.

### mqtt pack

![mqtt icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/mqtt/icon.png)

#### Sensors

Name | Description
---- | -----------
MQTTSensor | Listen for events on MQTT bus/topic

#### Actions

Name | Description
---- | -----------
publish | Publish message to MQTT broker

### nest pack

![nest icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/nest/icon.png)

#### Actions

Name | Description
---- | -----------
get_humidity | Get the current humidity
get_mode | Manage nest modes
get_temperature | Get the current temperature.
set_away | Set nest to away mode
set_fan | Manage fan state
set_home | Set nest to home mode
set_humidity | Set humidity goal for nest
set_mode | Set current operating mode
set_temperature | Set current temperature.
show | Show current Nest information
toggle_away | Toggle current Home/Away status

### newrelic pack

![newrelic icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/newrelic/icon.png)

#### Sensors

Name | Description
---- | -----------
NewRelicHookSensor | Sensor which watches for alerts from the NewRelic legacy API.
NewRelicHookSensor | Sensor which watches for alerts from NewRelic API.

#### Actions

Name | Description
---- | -----------
get_alerts | Get alerts for app.
get_metric_data | Get metric data for metric.

### octopusdeploy pack

![octopusdeploy icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/octopusdeploy/icon.png)

#### Sensors

Name | Description
---- | -----------
NewDeploymentSensor | A sensor for new deployments.
NewReleaseSensor | A sensor for new releases.

#### Actions

Name | Description
---- | -----------
add_machine | Add a new machine (tentacle) to an Octopus Environment
create_release | Create a new release in Octopus.
deploy_release | Deploy a release in Octopus.
list_deployments | Get a list of deployments for a project
list_projects | Get a list of projects in Octopus.
list_releases | Get a list of releases for a project in Octopus.

### openhab pack

![openhab icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/openhab/icon.png)

#### Actions

Name | Description
---- | -----------
get_status | Get status on an item
send_command | Send a command to an item
set_state | Set state on an item

### openstack pack

![openstack icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/openstack/icon.png)

#### Actions

Name | Description
---- | -----------
cinder | Run OpenStack Cinder commands
get_instance_owners | Returns the users associated with a list of instance ids
glance | Run OpenStack Glance commands
nova | Run OpenStack Nova commands
nova_confirm | Confirms a resize or migrate
nova_instances | Returns a list of instances by hypervisor
nova_migrate_server | Evacuate guests from compute node

### packagecloud pack

![packagecloud icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/st2/icon.png)

#### Actions

Name | Description
---- | -----------
create_master_token | None
destroy_master_token | None
destroy_read_token | None
list_master_token | None

### packer pack

![packer icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/packer/icon.png)

#### Actions

Name | Description
---- | -----------
build | Build images from a packer template
fix | Takes a template and finds backwards incompatible parts of it and brings it up to date so it can be used with the latest version of Packer
inspect | Takes a template and outputs the various components a template defines
push | Push a template to Hashicorp Atlas
validate | Validate a packer template

### pagerduty pack

![pagerduty icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/pagerduty/icon.png)

#### Actions

Name | Description
---- | -----------
ack_incident | ACK an incident on PagerDuty
get_open_incidents | Retrive list of open incidents from PagerDuty
launch_incident | Launch an incident on PagerDuty
resolve_incident | Resolve an incident whose key is provided

### puppet pack

![puppet icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/puppet/icon.png)

#### Actions

Name | Description
---- | -----------
apply | Apply a standalone puppet manifest to a local system.
cert_clean | Revoke a host's certificate (if applicable) and remove all files related to that host from puppet cert's storage.
cert_revoke | Revoke the certificate of a client.
cert_sign | Sign an outstanding certificate request.
run_agent | Run puppet agent.

### qualys pack

![qualys icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/qualys/icon.png)

#### Actions

Name | Description
---- | -----------
add_host | Add an IP of a host to the Qualys registry
add_hosts | Add IPs of hosts to the Qualys registry
get_host | Get a registered host from the host collection
get_host_range | Get the status of a range of hosts (IP range)
get_report | Get a report
launch_scan | Launch a scan
list_hosts_not_scanned_since | Get a list of host not scanned in a number of days
list_reports | Get a list of available reports
list_scans | List the scans

### rabbitmq pack

![rabbitmq icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/rabbitmq/icon.png)

#### Sensors

Name | Description
---- | -----------
RabbitMQSensor | Sensor which monitors a RabbitMQ queue for new messages

#### Actions

Name | Description
---- | -----------
list_exchanges | List RabbitMQ exchanges
list_queues | List RabbitMQ queues
publish_message | Publish a message in RabbitMQ

### rackspace pack

![rackspace icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/rackspace/icon.png)

#### Actions

Name | Description
---- | -----------
add_node_to_loadbalancer | Add a new node to load balancer
create_dns_record | Create a new DNS record.
create_dns_zone | Create a new DNS zone.
create_loadbalancer | Create a new loadbalancer.
create_vm | Create a new VM / cloud server
delete_dns_record | Delete a DNS record.
delete_dns_zone | Delete a DNS zone.
delete_loadbalancer | Delete a loadbalancer
delete_node_from_loadbalancer | Delete a node from a load balancer
delete_vm | Delete a vm.
find_dns_record_id | Find a DNS record ID based on name
find_dns_zone_id | Find a DNS zone id based on name
find_loadbalancer_id | Find a loadbalancer id based on name
find_vm_id | Find a virtual machine id based on name
get_vm_by_ip | Retrieve information for a VM which matches the provided public IP.
get_vm_ids | Retrieve IDs for all the available VMs. Optionally filter by metadata and count.
get_vm_info | Retrieve information for a provided VM. Optionally filter on the metadata values.
get_vm_ips | Retrieve public IP addresses for all the available VMs. Optionally filter by metadata and count.
get_vm_names | List all the available vms by names. Optionally filter by metadata and count
list_dns_records | List all records for a particular zone.
list_dns_zones | List all the DNS zones.
list_vm_images | List all the available VM images
list_vm_sizes | List all the available VM sizes
list_vms | List all the available vms. Optionally filter on the metadata values.
set_vm_metadata | Set metadata values for the provided VM.
set_vm_metadata_item | Set a value of a metadata item for a provided VM.

### reamaze pack

![reamaze icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/reamaze/icon.png)

#### Actions

Name | Description
---- | -----------
article_create | This action creates a specific article given article name (called 'slug' in reamaze). You can optionally provide a topic to place article under.
article_get | This action gets a specific article given article name (called 'slug' in reamaze).
article_search | This action searches through articles that may be related to a user query
article_update | This action updates a specific article given article name (called 'slug' in reamaze).
create_message | Create a new message under a specific conversation
get_conversations | This action looks through open re:amaze issues and reports back status

### salt pack

![salt icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/salt/icon.png)

#### Actions

Name | Description
---- | -----------
bootstrap | Bootstrap servers with salt.cloud runner
client | Run salt LocalClient functions
local | Run Salt Exection Modules through Salt API
local_archive.gunzip | Run Salt Execution modules through Salt API
local_archive.gzip | Run Salt Execution modules through Salt API
local_archive.rar | Run Salt Execution modules through Salt API
local_archive.tar | Run Salt Execution modules through Salt API
local_archive.unrar | Run Salt Execution modules through Salt API
local_archive.unzip | Run Salt Execution modules through Salt API
local_archive.zip_ | Run Salt Execution modules through Salt API
local_cloud.action | Run Salt Execution modules through Salt API
local_cloud.create | Run Salt Execution modules through Salt API
local_cloud.destroy | Run Salt Execution modules through Salt API
local_cloud.network_create | Run Salt Execution modules through Salt API
local_cloud.profile_ | Run Salt Execution modules through Salt API
local_cloud.virtual_interface_create | Run Salt Execution modules through Salt API
local_cloud.volume_attach | Run Salt Execution modules through Salt API
local_cloud.volume_create | Run Salt Execution modules through Salt API
local_cloud.volume_delete | Run Salt Execution modules through Salt API
local_cloud.volume_detach | Run Salt Execution modules through Salt API
local_cmdmod.run | Run Salt Execution modules through Salt API
local_cmdmod.run_chroot | Run Salt Execution modules through Salt API
local_cmdmod.script | Run Salt Execution modules through Salt API
local_cp.get_file | Run Salt Execution modules through Salt API
local_cp.get_url | Run Salt Execution modules through Salt API
local_cp.push | Run Salt Execution modules through Salt API
local_cp.push_dir | Run Salt Execution modules through Salt API
local_cron.ls | Run Salt Execution modules through Salt API
local_cron.rm_env | Run Salt Execution modules through Salt API
local_cron.rm_job | Run Salt Execution modules through Salt API
local_cron.set_env | Run Salt Execution modules through Salt API
local_cron.set_job | Run Salt Execution modules through Salt API
local_data.cas | Run Salt Execution modules through Salt API
local_data.dump | Run Salt Execution modules through Salt API
local_data.getval | Run Salt Execution modules through Salt API
local_data.update | Run Salt Execution modules through Salt API
local_event.fire | Run Salt Execution modules through Salt API
local_event.fire_master | Run Salt Execution modules through Salt API
local_event.send | Run Salt Execution modules through Salt API
local_file.access | Run Salt Execution modules through Salt API
local_file.chgrp | Run Salt Execution modules through Salt API
local_file.chown | Run Salt Execution modules through Salt API
local_file.directory_exists | Run Salt Execution modules through Salt API
local_file.file_exists | Run Salt Execution modules through Salt API
local_file.find | Run Salt Execution modules through Salt API
local_file.manage_file | Run Salt Execution modules through Salt API
local_file.mkdir | Run Salt Execution modules through Salt API
local_file.remove | Run Salt Execution modules through Salt API
local_file.replace | Run Salt Execution modules through Salt API
local_file.search | Run Salt Execution modules through Salt API
local_file.symlink | Run Salt Execution modules through Salt API
local_file.touch | Run Salt Execution modules through Salt API
local_file.truncate | Run Salt Execution modules through Salt API
local_grains.append | Run Salt Execution modules through Salt API
local_grains.delval | Run Salt Execution modules through Salt API
local_grains.get | Run Salt Execution modules through Salt API
local_grains.remove | Run Salt Execution modules through Salt API
local_grains.setval | Run Salt Execution modules through Salt API
local_hosts.add_hosts | Run Salt Execution modules through Salt API
local_hosts.get_alias | Run Salt Execution modules through Salt API
local_hosts.get_ip | Run Salt Execution modules through Salt API
local_hosts.rm_host | Run Salt Execution modules through Salt API
local_hosts.set_host | Run Salt Execution modules through Salt API
local_htpasswd.useradd | Run Salt Execution modules through Salt API
local_htpasswd.userdel | Run Salt Execution modules through Salt API
local_mine.delete | Run Salt Execution modules through Salt API
local_mine.get | Run Salt Execution modules through Salt API
local_mine.send | Run Salt Execution modules through Salt API
local_mine.update | Run Salt Execution modules through Salt API
local_network.connect | Run Salt Execution modules through Salt API
local_network.interface_ip | Run Salt Execution modules through Salt API
local_network.ipaddrs | Run Salt Execution modules through Salt API
local_network.ping | Run Salt Execution modules through Salt API
local_network.subnets | Run Salt Execution modules through Salt API
local_pillar.get | Run Salt Execution modules through Salt API
local_pip.freeze | Run Salt Execution modules through Salt API
local_pip.install | Run Salt Execution modules through Salt API
local_pip.uninstall | Run Salt Execution modules through Salt API
local_pkg.install | Run Salt Execution modules through Salt API
local_pkg.refresh_db | Run Salt Execution modules through Salt API
local_pkg.remove | Run Salt Execution modules through Salt API
local_puppet.disable | Run Salt Execution modules through Salt API
local_puppet.enable | Run Salt Execution modules through Salt API
local_puppet.fact | Run Salt Execution modules through Salt API
local_puppet.noop | Run Salt Execution modules through Salt API
local_puppet.run | Run Salt Execution modules through Salt API
local_puppet.status | Run Salt Execution modules through Salt API
local_puppet.summary | Run Salt Execution modules through Salt API
local_ret.get_fun | Run Salt Execution modules through Salt API
local_ret.get_jid | Run Salt Execution modules through Salt API
local_ret.get_jids | Run Salt Execution modules through Salt API
local_ret.get_minions | Run Salt Execution modules through Salt API
local_saltutil.sync_all | Run Salt Execution modules through Salt API
local_saltutil.sync_grains | Run Salt Execution modules through Salt API
local_saltutil.sync_modules | Run Salt Execution modules through Salt API
local_saltutil.sync_outputters | Run Salt Execution modules through Salt API
local_saltutil.sync_renderers | Run Salt Execution modules through Salt API
local_saltutil.sync_returners | Run Salt Execution modules through Salt API
local_saltutil.sync_states | Run Salt Execution modules through Salt API
local_saltutil.sync_utils | Run Salt Execution modules through Salt API
local_schedule.add | Run Salt Execution modules through Salt API
local_schedule.delete | Run Salt Execution modules through Salt API
local_schedule.disable_job | Run Salt Execution modules through Salt API
local_schedule.enable_job | Run Salt Execution modules through Salt API
local_schedule.run_job | Run Salt Execution modules through Salt API
local_service.available | Run Salt Execution modules through Salt API
local_service.restart | Run Salt Execution modules through Salt API
local_service.start | Run Salt Execution modules through Salt API
local_service.status | Run Salt Execution modules through Salt API
local_service.stop | Run Salt Execution modules through Salt API
local_shadow.del_password | Run Salt Execution modules through Salt API
local_shadow.gen_password | Run Salt Execution modules through Salt API
local_shadow.set_expire | Run Salt Execution modules through Salt API
local_state.highstate | Run Salt Execution modules through Salt API
local_state.single | Run Salt Execution modules through Salt API
local_state.sls | Run Salt Execution modules through Salt API
local_supervisord.add | Run Salt Execution modules through Salt API
local_supervisord.custom | Run Salt Execution modules through Salt API
local_supervisord.remove | Run Salt Execution modules through Salt API
local_supervisord.reread | Run Salt Execution modules through Salt API
local_supervisord.restart | Run Salt Execution modules through Salt API
local_supervisord.start | Run Salt Execution modules through Salt API
local_supervisord.stop | Run Salt Execution modules through Salt API
local_systemd.available | Run Salt Execution modules through Salt API
local_systemd.disable | Run Salt Execution modules through Salt API
local_systemd.enable | Run Salt Execution modules through Salt API
local_systemd.restart | Run Salt Execution modules through Salt API
local_systemd.start | Run Salt Execution modules through Salt API
local_systemd.stop | Run Salt Execution modules through Salt API
local_systemd.systemctl_reload | Run Salt Execution modules through Salt API
local_test.cross_test | Run Salt Execution modules through Salt API
local_test.echo | Run Salt Execution modules through Salt API
local_test.ping | Run Salt Execution modules through Salt API
local_useradd.add | Run Salt Execution modules through Salt API
local_useradd.chshell | Run Salt Execution modules through Salt API
local_useradd.delete | Run Salt Execution modules through Salt API
runner | Run Salt Runner functions through Salt API
runner_cache.clear_all | Run Salt Runner functions through Salt API
runner_cache.clear_grains | Run Salt Runner functions through Salt API
runner_cache.clear_mine | Run Salt Runner functions through Salt API
runner_cache.clear_mine_func | Run Salt Runner functions through Salt API
runner_cache.clear_pillar | Run Salt Runner functions through Salt API
runner_cache.grains | Run Salt Runner functions through Salt API
runner_cache.mine | Run Salt Runner functions through Salt API
runner_cache.pillar | Run Salt Runner functions through Salt API
runner_cloud.action | Run Salt Runner functions through Salt API
runner_cloud.full_query | Run Salt Runner functions through Salt API
runner_cloud.list_images | Run Salt Runner functions through Salt API
runner_cloud.list_locations | Run Salt Runner functions through Salt API
runner_cloud.list_sizes | Run Salt Runner functions through Salt API
runner_cloud.profile | Run Salt Runner functions through Salt API
runner_cloud.query | Run Salt Runner functions through Salt API
runner_cloud.select_query | Run Salt Runner functions through Salt API
runner_jobs.active | Run Salt Runner functions through Salt API
runner_jobs.list_jobs | Run Salt Runner functions through Salt API
runner_manage.down | Run Salt Runner functions through Salt API
runner_manage.status | Run Salt Runner functions through Salt API
runner_manage.up | Run Salt Runner functions through Salt API
runner_manage.versions | Run Salt Runner functions through Salt API
runner_pillar.show_pillar | Run Salt Runner functions through Salt API
runner_pillar.show_top | Run Salt Runner functions through Salt API
runner_thin.generate | Run Salt Runner functions through Salt API

### sensu pack

![sensu icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/sensu/icon.png)

#### Actions

Name | Description
---- | -----------
aggregate_list | List Sensu Aggregate Stats
check_aggregates | Get Sensu check aggregates
check_aggregates_delete | Delete Sensu check aggregates
check_aggregates_issued | Get a specific Sensu check aggregate
check_info | Get Sensu check info
check_list | List Sensu checks
check_request | Schedule a Sensu check request
client_delete | Delete a Sensu client
client_history | Get Sensu client history
client_info | Get Sensu client info
client_info | Get Sensu client info
client_list | List Sensu clients
event_client_list | List Sensu events for a given client
event_delete | Delete a Sensu event
event_info | Get Sensu event info
event_list | List Sensu events
health | Sensu System Health
info | Sensu System Info
silence | Silence a Sensu client or check
unsilence | Unsilence a Sensu client or check

### servicenow pack

![servicenow icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/servicenow/icon.png)

#### Actions

Name | Description
---- | -----------
delete | Delete an entry from a ServiceNow Table
get | Get an entry from a ServiceNow Table
get_non_structured | Run a string GET query on the ServiceNow API
insert | Insert an entry to a ServiceNow Table
update | Update an entry in a ServiceNow Table

### signalr pack

![signalr icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/signalr/icon.png)

#### Sensors

Name | Description
---- | -----------
SignalRHubSensor | Sensor which listens for push notifications raise by signalr

#### Actions

Name | Description
---- | -----------
send_message | Send a message to a SignalR Hub

### slack pack

![slack icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/slack/icon.png)

#### Sensors

Name | Description
---- | -----------
SlackSensor | Sensor which monitors Slack for activity

#### Actions

Name | Description
---- | -----------
api.test | This method helps you test your calling code.
auth.test | This method checks authentication and tells you who you are.
channels.archive | This method archives a channel.
channels.create | This method is used to create a channel.
channels.history | This method returns a portion of messages/events from the specified channel. To read the entire history for a channel, call the method with no latest or oldest arguments, and then continue paging using the instructions below.
channels.info | This method returns information about a team channel.
channels.invite | This method is used to invite a user to a channel. The calling user must be a member of the channel.
channels.join | This method is used to join a channel. If the channel does not exist, it is created.
channels.kick | This method allows a user to remove another member from a team channel.
channels.leave | This method is used to leave a channel.
channels.list | This method returns a list of all channels in the team. This includes channels the caller is in, channels they are not currently in, and archived channels. The number of (non-deactivated) members in each channel is also returned.
channels.mark | This method moves the read cursor in a channel.
channels.rename | This method renames a team channel.
channels.setPurpose | This method is used to change the purpose of a channel. The calling user must be a member of the channel.
channels.setTopic | This method is used to change the topic of a channel. The calling user must be a member of the channel.
channels.unarchive | This method unarchives a channel. The calling user is added to the channel.
chat.delete | This method deletes a message from a channel.
chat.postMessage | This method posts a message to a channel.
chat.update | This method updates a message in a channel.
emoji.list | This method lists the custom emoji for a team.
files.delete | This method deletes a file from your team.
files.info | This method returns information about a file in your team.
files.list | This method returns a list of files within the team. It can be filtered and sliced in various ways.
files.upload | This method allows you to create or upload an existing file.
groups.archive | This method archives a private group.
groups.close | This method closes a private group.
groups.create | This method creates a private group.
groups.createChild | This method takes an existing private group and performs the following steps:
groups.history | This method returns a portion of messages/events from the specified private group. To read the entire history for a group, call the method with no latest or oldest arguments, and then continue paging using the instructions below.
groups.info | This method returns information about a private group.
groups.invite | This method is used to invite a user to a private group. The calling user must be a member of the group.
groups.kick | This method allows a user to remove another member from a private group.
groups.leave | This method is used to leave a private group.
groups.list | This method returns a list of groups in the team that the caller is in and archived groups that the caller was in. The list of (non-deactivated) members in each group is also returned.
groups.mark | This method moves the read cursor in a private group.
groups.open | This method opens a private group.
groups.rename | This method renames a private group.
groups.setPurpose | This method is used to change the purpose of a private group. The calling user must be a member of the private group.
groups.setTopic | This method is used to change the topic of a private group. The calling user must be a member of the private group.
groups.unarchive | This method unarchives a private group.
im.close | This method closes a direct message channel.
im.history | This method returns a portion of messages/events from the specified direct message channel. To read the entire history for a direct message channel, call the method with no latest or oldest arguments, and then continue paging using the instructions below.
im.list | This method returns a list of all im channels that the user has.
im.mark | This method moves the read cursor in a direct message channel.
im.open | This method opens a direct message channel with another member of your Slack team.
oauth.access | This method allows you to exchange a temporary OAuth code for an API access token. This is used as part of the OAuth authentication flow.
post_message | Post a message to the Slack channel.
rtm.start | This method starts a Real Time Messaging API session. Refer to the RTM API documentation for full details on how to use the RTM API.
search.all | This method allows to to search both messages and files in a single call.
search.files | This method returns files matching a search query.
search.messages | This method returns messages matching a search query.
stars.list | This method lists the items starred by a user.
team.accessLogs | This method is used to get the access logs for users on a team.
team.info | This method provides information about your team.
users.admin.invite | Send an invitation to join a Slack Org
users.getPresence | This method lets you find out information about a user's presence. Consult the presence documentation for more details.
users.info | This method returns information about a team member.
users.list | This method returns a list of all users in the team. This includes deleted/deactivated users.
users.setActive | This method lets the slack messaging server know that the authenticated user is currently active. Consult the presence documentation for more details.
users.setPresence | This method lets you set the calling user's manual presence. Consult the presence documentation for more details.

### smartthings pack

![smartthings icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/smartthings/icon.png)

#### Sensors

Name | Description
---- | -----------
SmartThingsSensor | Sensor listening for HTTP events from SmartThings

#### Actions

Name | Description
---- | -----------
command | Send a generic command to a device
disengage_lock | Disengage (lock) a device that can be locked
engage_lock | Engage (lock) a device that can be locked
find_id_by_name | Lookup a specific device ID based on its name/type
get_device_info | Get information on a specific device
list_devices | List devices of a specific type from SmartThings
set_mode | Set current temperature.
set_temperature | Set current temperature.
toggle_lock | Toggle a lock
toggle_switch | Toggle a switch
turn_off_switch | Turn off a light
turn_on_switch | Turn on a switch

### softlayer pack

![softlayer icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/softlayer/icon.png)

#### Actions

Name | Description
---- | -----------
create_instance | Creates a new instance
create_keypair | Creates a keypair by name
delete_keypair | Deletes a keypair by name. If there are mutiple keys with the same name it will only delete the first
destroy_instance | Destroys an instance

### splunk pack

![splunk icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/splunk/icon.png)

#### Actions

Name | Description
---- | -----------
search | Splunk one-shot search

### st2 pack

![st2 icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/st2/icon.png)

#### Actions

Name | Description
---- | -----------
actions.list | Retrieve a list of available StackStorm actions.
call_home | Sends anonymous data install data to a StackStorm write-only S3 dropbox
check_permissions_anon_data | Check if sending anonymous data is allowed.
executions.get | Retrieve details of a single execution.
executions.list | Retrieve a list of executions.
executions.re_run | Re-run an action execution.
kv.delete | Delete value from datastore
kv.get | Get value from datastore
kv.get_object | Deserialize and retrieve JSON serialized object from a datastore
kv.grep | Grep for values in datastore
kv.set | Set value in datastore
kv.set_object | Serialize and store object in a datastore
rules.list | Retrieve a list of available StackStorm rules
sensors.list | Retrieve a list of available StackStorm sensors.
upload_to_s3 | Sends collected data to write-only StackStorm S3 bucket

### time pack

![time icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/time/icon.png)

#### Actions

Name | Description
---- | -----------
get_week_boundaries | Retrieve week boundary timestamps (week start and end) for the provided date.
parse_date_string | Parse the (human readable) date string and return timestamp.

### travis_ci pack

![travis_ci icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/travis_ci/icon.png)

#### Actions

Name | Description
---- | -----------
cancel_build | Cancel a build.
disable_hook | Disable hooks for a git repo.
enable_hook | Enable hook for a git repo.
get_repo | Retrieve details for a provided repository.
list_branches | List all branches for a given repository.
list_builds | List details of all the available builds.
list_hooks | List available hooks for the authenticated user.
list_repos | List repositories for the provided user.
restart_build | Restart a Build

### trello pack

![trello icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/trello/icon.png)

#### Sensors

Name | Description
---- | -----------
TrelloListSensor | Sensor which monitors Trello list for a new actions (events)

#### Actions

Name | Description
---- | -----------
add_board | Create a new board
add_card | Add a new card to a list
add_list | Add a new list to a board
close_board | Close a board
close_card | Close a card
close_list | Close a list belonging to a board
find_board_by_name | Lookup a board ID based on name. Returns one or more IDs
find_card_by_name | Lookup a Card ID based on name. Returns one or more IDs
find_list_by_name | Lookup a list ID based on name. Returns one or more IDs
move_card | Move a card from one board/list to another board/list
view_boards | Return a dictionary of all boards and their IDs
view_cards | View all cards on a board
view_lists | View all lists belonging to a board
view_organizations | List all organizations for user

### twilio pack

![twilio icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/twilio/icon.png)

#### Actions

Name | Description
---- | -----------
send_sms | This sends a SMS using twilio.

### twitter pack

![twitter icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/twitter/icon.png)

#### Sensors

Name | Description
---- | -----------
TwitterSearchSensor | Sensor which monitors twitter timeline for new tweets matching the specified criteria

#### Actions

Name | Description
---- | -----------
direct_message | Direct message a user.
follow | Follow a user.
update_status | Update your status (post a new tweet).

### typeform pack

![typeform icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/typeform/icon.png)

#### Sensors

Name | Description
---- | -----------
TypeformRegistrationSensor | Sensor which monitors for new Typeform registrations

#### Actions

Name | Description
---- | -----------
get_results | Get Typeform registration results

### urbandict pack

![urbandict icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/urbandict/icon.png)

#### Actions

Name | Description
---- | -----------
get_definitions | Retrieve definitions from urbandict for the provided term.

### victorops pack

![victorops icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/victorops/icon.png)

#### Actions

Name | Description
---- | -----------
ack_incident | Acknowledge a triggered event on victorops
open_incident | Triggers the event on VictorOps with the given parameters
recover_incident | Recover a triggered event on victorops

### webpagetest pack

![webpagetest icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/webpagetest/icon.png)

#### Actions

Name | Description
---- | -----------
list_locations | List available testing locations.
random_test | Test a domain on WebPageTest from a random location.
request_test | Test a domain on WebPageTest.

### windows pack

![windows icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/windows/icon.png)

#### Actions

Name | Description
---- | -----------
wmi_query | Run a WMI query on a particular Windows host.

### witai pack

![witai icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/witai/icon.png)

#### Actions

Name | Description
---- | -----------
text_query | Send a text query to Wit.ai API

### xml pack

![xml icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/xml/icon.png)

#### Actions

Name | Description
---- | -----------
parse | Parse XML string and return JSON object.

### yammer pack

![yammer icon](https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/yammer/icon.png)

#### Actions

Name | Description
---- | -----------
authenticate | Requests a OAuth authorization URL from the Yammer API, use this URL to authenticate your app in a browser, use the code in config.yaml
like_message | Like a particular message
list_messages | List all messages globally for the authenticated user
list_messages_from_user | List all messages from my feed for the authenticated user
list_messages_my_feed | List all messages from my feed for the authenticated user
post_message | List all messages from my feed for the authenticated user

## License, and Contributors Agreement

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
work except in compliance with the License. You may obtain a copy of the License in
the LICENSE file, or at
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by
your employer) and you grant a full, complete, irrevocable copyright license to
all users and developers of the project, present and future, pursuant to the
license of the project.
