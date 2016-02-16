Typeform Integration
====================

This integration pack provides a sensor to query a Typeform form for new submissions.

### Prerequisites
In order to track state, it depends on a MySQL database.

```
CREATE DATABASE community;

USE community;

CREATE TABLE user_registration(
			id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
			email VARCHAR(255) NOT NULL,
			last_name VARCHAR(32),
			first_name VARCHAR(32),
			source VARCHAR(255),
			newsletter TINYINT UNSIGNED,
			referer VARCHAR(128),
			date_land TIMESTAMP,
			date_submit TIMESTAMP,
			date_invited TIMESTAMP);

ALTER TABLE user_registration ADD UNIQUE(email);
GRANT ALL PRIVILEGES ON community.* to 'CHANGEME'@'localhost' IDENTIFIED BY 'CHANGEME';
```

### Sensors
This pack ships with a sensor that checks the Typeform API for submissions to a given form, then compares that list against a MySQL database.  If the submission is not yet in the database, it submits a trigger with the information from the submission.  Currently the sensor is limited to a specific format of the form.  Required fields in the config file are:

* api_key - You can find this from the admin page on the Typeform site:
    * https://admin.typeform.com/account
* form_id - This ID is displayed when you go to the URL for your form.  The format looks like this:
    * https://[USERNAME].typeform.com/to/[FORM_ID]

PLEASE NOTE: the fields used in registration_sensor.py for user information are unique to your form.  E.g. EMAIL_FIELD = "email_7723200" which is listed in the provided registration_sensor.py file will not work for you.  To get the field names you need to use first create the form you want people to fill out, fill out a sample form, and then modify this URL with your information to get a JSON response with the correct field names:
https://api.typeform.com/v0/form/[FORM_ID]?key=[API_key]&completed=true

### Actions
In case you are interested in getting the list of submissions on demand, instead of running them from the sensor, you can use this action.

* typeform.get_results - This will read the api_key from the config file, but it can also be passed in at the time of execution as a parameter.
    * form_id - This is the only required parameter for this action.
