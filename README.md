# TikTok Reuploader


This package uses [selenium](https://www.selenium.dev/) with [chromium](https://chromedriver.chromium.org/)

## Requirements
Installed [chrome](https://www.google.com/intl/en/chrome/)


Installed [python3](https://www.python.org/downloads/)

Then type in cmd
`pip install -r requirements.txt`  to install required python packages

> Python needs to be added to the PATH and you have to be in current directory of the project.


## First run

If you are running this for the first time, you have to first run 
`python first_run.py` **(it will automatically download chromedriver)**, simply login to the TikTok and after that you can close the browser


## Examples
You can find example with youtube in file **example.py**
<br></br>
**Another example**
```python
# import upload function
from tiktok import upload_video

path_to_video = "video.mp4" # every video format that tiktok supports 

# then simply call this function
upload_video(
   path = path_to_video,
   description = "Some description",
   tags = [ "some", "tags" ]
)
```

## Note
Also note that you can have only one running instance of the browser because it's using the same profile

<br></br>
**If you have any questions,
you can contact me on discord: `joojn#5485`**