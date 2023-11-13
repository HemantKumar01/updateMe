# updateMe
A script which automatically checks for updates in websites and email you about any changes

# Usage

## Setup
 1. clone this repository
 2. run `pip install-r requirements.txt`
 3. create an empty folder named "tmp".
 4. create auth.env file with values as follows - 

  ```
  EMAIL= <systemEmail> /* the email from which you want to send email. LessSecureApps must be enabled if gmail */
  PASSWORD = <systemEmailPassword> /* password of above email */
  TOEMAIL=<yourEmail> /* email in which you want to recieve notifications*/
  ```
 ## how to use
 
 1. add websites to watch(as many you want) by running `python scrape.py` command (it will prompt for website url).
 2. run `python check.py` command to check and email you about updates(if any)
 3. run `python manageData.py <arg>` to use manageData.py script with <arg> as one of the following arguments-
  
  ```
  arguments-
  -----------
  -reset : re-inits the urls.json(all data) and clears all websites which are in queue to be watched for updates;
  -show : shows urls.json (all data about stored website);
  -help :show all commands;
  ? : short form for -help
  ```
