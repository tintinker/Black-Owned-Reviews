# Black-Owned-Reviews

Will update this to be more extensive!!  

Add cities to labels/citylist.txt  
Create virtual environment  
Install requirements.txt  
Run `cd labels`   
Edit start.py with options: `run_city(city, overwrite_cities=True, overwrite_labels=False, min_results=40, debug=True, data_file='citydata.json')`  
Note for @Irena: if you can run with `min_results > 60` to test if the places API will give you more results that would be awesome
Run `PATH=$PATH:. python3 start.py` Note the PATH part is important so that selenium can find the chrome driver executable  
Output in data/citydata.json  
