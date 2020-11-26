#!/bin/sh

set -ex

echo "15 7-23/1 * * * killall python & python /vote/getVotes.py > /vote/cron_votes.log 2>&1 &" >> /var/spool/cron/crontabs/root
echo "30 22 * * * python /vote/vote500.py > /vote/cron_votes_500.log 2>&1 &" >> /var/spool/cron/crontabs/root
echo "0 23 * * * python /vote/vote500_1.py > /vote/cron_votes_500.log 2>&1 &" >> /var/spool/cron/crontabs/root

crond -f

