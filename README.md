# Black-Owned-Reviews

This should be working now!!  

## Setting up dev environment [Local Computer]
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

## Setting up the dev environment [Amazon EC2]
1. Install firefox on the EC2 Instace using [this tutorial](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-2-install-gui/)  
2. Download geckodriver from [here](https://github.com/mozilla/geckodriver/releases) and copy using `scp` to the EC2 instance  
3. Install git and clone the `ec2` branch of the repository to the EC2 Instance
4. Make sure the locations of firefox and geckodriver match the ones described in `.env.local`
5. Intall `tmux` on the instance. See [here](https://medium.com/@waya.ai/deep-learning-aws-ec2-tmux-3b96777016e2) for usage


You should be good to go!

## Run the scraper [Local Computer]
*Important: make sure the virtual environment is activated (you should see (env) in the terminal)*  
If not: `$ source env/bin/activate`   

1. Activate generated environment variable   
`(env) $ source .env.local`     
2. Add Business License Directories in CSV form to the `city_directories` folder   
3. Add functions to parse the address, name, and filter the rows to `parsers.py`. See file for examples  
4. Add the city name(s) & associated group(s) of parsing functions to `lst` in `start.py`  
5. Run `start.py`   
Cache files will be generated throughout (ex. `city_directories/seattlecache.csv`, output available in csv form at the end (ex. `city_directories/seattleoutput.csv`)

## Run the scraper [Amazon EC2]
On local computer:   
1. Switch to ec2 branch   
Follow steps 2-4 from above   
5. Push changes to `ec2` branch   
On Amazon EC2  
6. Get the ip address of the ec2 instance from the aws dev view and connect using the pem file: `ssh -i "~/.ssh/blackowned.pem" ec2-user@xxx-##-##-##-###.us-east-#.compute.amazonaws.com`  
7. Pull changes to `ec2` branch  
8. Copy city data file to city_directories folder on ec2 (don't use git for this as it'll be too big)
9. Run `tmux attach` to check for currently running jobs  
10. Start a new job: `source .env.local && python3 start.py`  
11. Put the job in the background: `ctrl+b d`  
12. Logout, periodically check log, and copy finished csv when done   
13. Resave csv as xlsx and plug into Tableau graphs  

