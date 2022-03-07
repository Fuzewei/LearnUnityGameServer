#!/bin/bash
currentdir=$(pwd)
echo $currentdir
logPath="$currentdir"/logs
echo $logPath
rm -rf $logPath
exit 1

