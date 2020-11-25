#!/bin/sh

set -ex

echo "* 7-24/1 * * * python /vote/getVotes.py > /vote/cron_votes.log 2>&1 &\n" >> /var/spool/cron/crontabs/root
echo "30 22 * * * python /vote/vote500.py > /vote/cron_votes_500.log 2>&1 &\n" >> /var/spool/cron/crontabs/root
echo "10 23 * * * python /vote/vote500_1.py > /vote/cron_votes_500.log 2>&1 &\n" >> /var/spool/cron/crontabs/root

crond -f

