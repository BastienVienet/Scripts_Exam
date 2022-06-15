#! /bin/bash

ps -e
echo "Which PID would you like to kill ?"
read userPID
kill $userPID
