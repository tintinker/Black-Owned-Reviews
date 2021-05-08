# Black-Owned-Reviews

This should be working now!!  

## Setting up dev environment
Note: `$` indicates a shell command. This assumes you're using a mac with virtualenv already installed  

0. Download [Firefox](https://www.mozilla.org/en-US/firefox/browsers/) if you don't already have it 
1. Clone this repository to a location of your choice  
2. Initialize a virtual environment (we will call it `env`)  
`$ virtualenv env`  
3. Activate the virtual environment  
`$ source env/bin/activate`  
4. Install the requirements  
`(env) $ pip3 install -r requirements.txt`  
5. Generate environment variable for Firefox WebDriver 
`(env) $ python3 firefox_env.py`

You should be good to go!

## Run the scraper
*Important: make sure the virtual environment is activated (you should see (env) in the terminal)*  
If not: `$ source env/bin/activate`  

1. Activate generated environment variable  
`(env) $ source .env.local`   
2. Add Business License Directories in CSV form to the `city_directories` folder  
3. Run the script  
`(env) $ python3 licence_directory.py city_directories/seattle.csv`
Cache files will be generated throughout (ex. `city_directories/seattlecache.csv`, output available in csv form at the end (ex. `city_directories/seattleoutput.csv`)

