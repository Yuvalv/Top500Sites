# Top500Sites

This Project get the 500 sites from https://moz.com/top500 
Send ping every 5 seconds to anyone of them
Storing the latency data of the pong
The result presenting in the HTML page

## Description:
The server-side wrote in Python (using flask)
the server starts to collect data (make ping) when the server start
The server return JSON of updated latency data every HTTP call
The HTML client calls the server every 7 seconds and presents the data on the graph

## Problems:
1)I use free MongoDB, so I have a connection limitation problem and performance 
So limit by the code to 10 sites (details in  get_data_from_site_and_store methods in site.py)
2)some of the site the www prefix missing so after the exception threw the system fix it and ping again
but if you were looking at the console you will see exception - I need to fix it (to hide the exception)

## Installation:
all the server is under the folder Top500Sites
you need to install all the module from the "requirements.txt" file
You need to run app.py with flask:
1)go to code dir (in cmd)
2)set FLASK_APP=app.py
3)flask run

the Html file is "top500.html."
