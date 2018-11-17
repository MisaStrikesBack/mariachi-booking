# Mariachi Booking Development DB Initialization scripts

This folder contains SQL scripts that will initialize the development & test
databases.

## Allowed sql scripts

The only real job SQL scripts included in this folder **should** be allowed to
do:

* Create the development and test databases.
* Enable any database extension that can't be enabled with Django migrations.

If your'e instead expecting to see data that should be on the database when
first run, consider taking a look instead at [Data Fixtures](https://docs.djangoproject.com/en/2.0/howto/initial-data/#providing-data-with-fixtures).
