St2 Logstash Filters & Dashboard
==========

####Introduction

Logstash provides a convenient way to view and search your St2 audit logs.

####Setup filter

Copy all of the .conf files from the filters folder in to /etc/logstash/conf.d:

    cp filters/*.conf /etc/logstash/conf.d/

Then restart Logstash:

    service logstash restart

Your St2 audit logs should start getting indexed by ElasticSearch shortly.  You will then be able to see them through your default dashboard.

####Setup dashboard

The easiest way to install the dashboard is through the Kibana UI.  

1. Click the 'load' button in the upper right corner
2. Click 'Advanced'
3. Click 'Choose File' and pick the dashboard you wish to load

Alternatively, you can copy the dashboard to the app/dashboards directory of Logstash.  By default on Ubuntu, that is here:

    /var/www/kibana/app/dashboards/
