# de-ice
Push notifications if de-icing of car is required

Saves the forecasts from [yr](https://yr.no) through their xml API.   
The forcasts are saved every hour and are stored in a file called ```forecasts.json```.   
This is done with the script ```forecaster.py```

Then at wanted time, the script ```pusher.py``` processes the forecasts, checks the temperatures for the previous hours (argument ```num_hours``` in ```def __init__()```).

Depending if the temperatures has been below 0 degrees celsius, the script pushes to a [Pushover](https://pushover.net/) app.

## Setup
Python external dependencies are ```xmltodict```.
Can be installed with pip:   
```pip3 install xmltodict```

### Credentials
Set up your pushover credentials in the file ```credentials.json``` from you pushover app.

### Cron
2 cron jobs are required for this to work

My setup is to run this on my raspberry pi.

One for ```forecaster.py``` that for me runs every hour   
```@hourly python3 /home/pi/projects/de-ice/forecaster.py```

One for ```pusher.py``` that runs at wanted time. For me at 6:00 every day   
```0 6 * * * python3 /home/pi/projects/de-ice/pusher.py```


## Contact
If you have any questions on how to set it up or other comments.   
Please contact me at [michael.sorsater@gmail.com](mailto:michael.sorsater@gmail.com)
