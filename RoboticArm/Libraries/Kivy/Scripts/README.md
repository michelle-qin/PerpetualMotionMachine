# Raspberry Pi Scripts

The scripts in this directory support the continuous running and maintainence of a project which has been deployed to the field.  This document describes how to install and run each script.  NOTE: These scripts are designed to help keep applications running and maintained without human interaction. You should fully understand what they do before installing.

launcher.sh : This script will launch the main UI (e.g. main.py)of your project. This script first checks to see if the application is already running, if so, it does nothing.  Otherwise, it will launch the application.  If you are running the application is running in the field, the launcher script should be executed in a cron job (see instructions below) to periodically check to see if the application is still running.  If the application has crashed, it will automatically restart it.

updater.sh : This script allows for a project to be updated remotely. The script checks if changes were made to a specific GitHub branch of the project (this branch SHOULD NOT be the master branch). If the script detects changes, the changes are pulled and installed in the project directory. This script should be run either when the Raspberry Pi boots or when the application is run (assume the application is launched infrequently).

## launcher.sh

### Defaults

The launcher assumes that your project is installed in the **/home/pi/Documents** directory and the process name is **main.py**.

If you want to override the default values, you can set the following environment variables:

export DPEA_REPO_ROOT="/home/pi/git"

export DPEA_PROCESS="main.py \-\- \-\-fan \-\-begin"

**NOTE: Use full paths, do not use ~/git**

### Executing the script

To execute the launcher script in a command shell:

     . launcher.sh <Project Directory Name>

for example:

     . launcher.sh InfinityMirrorPi

### Add the script to a Cron Job

A cron job allows a script to be run at a certain time interval: every minute, hour, day, etc. This is useful if you want to use the launcher script to periodically check if you process is not running (e.g. it crashed) and automatically restart the process. To run the launcher script in a cron job do the following:

To edit the cron file, execute the following command in the terminal:

    crontab -e

Add the following line to the bottom of the cron file:

    */5 * * * * sudo su - pi launcher.sh <Project Directory Name>

This will execute the launcher script every 5 minutes.  For more information on how to configure the time your cron job is executed refer to the following link:

https://corenominal.org/2016/05/12/howto-setup-a-crontab-file/


## updater.sh

The update script assumes that your project is installed in the **/home/pi/Documents** directory.

If you want to override the default value, you can set the following environment variables:

export DPEA_REPO_ROOT="/home/pi/git"

**NOTE: Use full paths, do not use ~/git**

### GitHub Username and Password

This script requires a username and password for GitHub. You can either set them on the system (the best solution), hardcode them in the script or set an environment variable.

export DPEA_GITHUB_USERNAME=<USERNAME>
export DPEA_GITHUB_PASSWORD=<PASSWORD>

### Executing the script

To execute the updater script in a command shell:

     . updater.sh <Project Directory Name>

for example:

     . updater.sh InfinityMirrorPi


