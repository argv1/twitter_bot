# Simple Twitter Bot
======================

## Purpose
Simple selenium prove of concept twitter bot to follow users by selenium webdriver. Please be aware this script does not use tweepy.

## Usage
run pip to ensure all requirements are fulfilled
 
```bash
pip3 install -r requirements.txt
```

You also need ChromeDriver, which you can download [here](https://chromedriver.chromium.org/downloads) and store the execuable in the script folder.

If you prefer Firefox, download geckodriver [here](https://github.com/mozilla/geckodriver/releases).
and adjust the following two line in main.py
```python
browser = base_path / 'geckodriver.exe'
...
self.driver = webdriver.Firefox(executable_path=browser)
```

now you can run the script:
```bash
main.py
```

## Future
Since I move to OOP, I will probably add some more features like mass liking by hashtag.
Feel free to improve and fork this small script.

## License
This code is licensed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). 
For more details, please take a look at the [LICENSE file](https://github.com/argv1/twitterbot/blob/master/LICENSE).

