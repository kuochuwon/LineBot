#!/bin/sh
# script to unidle heroku installation for the use with cronjob
# usage in crontab:
# */5 11-15 * * 1-5 /usr/local/bin/uptimer.sh http://www.example.com
# The command /usr/local/bin/uptimer.sh http://www.example.com will execute every 5th minute of 11am through 3pm Mondays through Fridays in every month.
# resources: http://www.cronchecker.net
echo url to unidle: $1
echo [UPTIMER]: waking up at:
date
curl $1
echo [UPTIMER]: awake at:
date