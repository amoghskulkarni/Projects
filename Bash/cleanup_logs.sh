#!/bin/bash
# Script to clean up logs in /var/logs

LOG_DIR=/var/log
ROOT_UID=0     
# Default number of lines saved 
LINES=50
# Can't change directory?
E_XCD=86
# Non-root exit error
E_NOTROOT=87

# Run as root
if [ "$UID" -ne "$ROOT_UID" ]
then 
    echo "Please run this script as root!"
    exit $E_NOTROOT
fi

if [ -n "$1" ]
# Test for command line arguments
then
    lines=$1
else
    # Choose default lines to save if no args
    lines=$LINES
fi

cd $LOG_DIR

if [ `pwd` != "$LOG_DIR" ]
then
    echo "Error changing directory"
    exit $E_XCD
fi

# Save $lines of messages to a temp file
tail -n $lines messages > mesg.temp
mv mesg.temp messages

cat /dev/null > wtmp
echo "Cleaned up logs!"

# Indicate success by returning zero
exit 0
