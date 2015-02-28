#!/bin/bash
# Save the current date & time
# Save all currently logged-in users
# Save the system uptime

echo "Saving system state..."
DATE=`date`
LOGGED_USERS=`who`
UPTIME=`uptime`
LOG_FILE="log.txt"

# Displaying saved information to user
echo "System Time:" $DATE >> $LOG_FILE
echo "Logged-in Users:" $LOGGED_USERS >> $LOG_FILE
echo "System Uptime:" $UPTIME >> $LOG_FILE

echo "Saved state to log:" $PWD/$LOG_FILE

# Exit cleanly
exit 0
