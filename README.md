# Instagram Unfollowers Bot
The purpose of this script is to automate the process of determining all unfollowers (i.e. Instagram users that you follow, but they do not follow you back) on your Instagram account.

## Requirements

#### Selenium Python Module
Install the module via `pip3` as such: `pip3 install selenium`
* __NOTE:__ Would recommend installing the module in a virtual environment to avoid module conflicts.

#### Chrome Webdriver 
1. Determine the version of Google Chrome that you're using via `chrome://settings/help` (paste into the search bar):<br />
<a href="https://ibb.co/26cKSPt"><img src="https://i.ibb.co/Jdrkq27/Chrome-Version.png" alt="Chrome-Version" border="0"></a><br />

2. Then go to https://chromedriver.chromium.org/downloads:<br />
<a href="https://ibb.co/0ygcDBS"><img src="https://i.ibb.co/Qv2fb8R/Chrome-Driver-Version.png" alt="Chrome-Driver-Version" border="0"></a><br />
And find your browser version listed and click on it (if the version is not listed, then update Chrome):<br />
<a href="https://ibb.co/2Zgjw0C"><img src="https://i.ibb.co/mN6Hmr2/Chrome-Version-Zip-Files.png" alt="Chrome-Version-Zip-Files" border="0"></a><br />
Then download the appropriate `.zip` file according to your OS.

3. Unzip the `.zip` file and move the  `chromedriver` file:<br />
<a href="https://ibb.co/g6Txf95"><img src="https://i.ibb.co/yVyrZPw/Chrome-Driver-File.png" alt="Chrome-Driver-File" border="0"></a><br />
into the `/usr/local/bin` directory:<br />
<a href="https://imgbb.com/"><img src="https://i.ibb.co/xhwj9j7/chromedriver-file-new-location.png" alt="chromedriver-file-new-location" border="0"></a><br />

#### `secrets.py` file
1. The Python3 script imports the `username` variable and `password` variable from a `secrets.py` file, so this Python file should be created in the same directory as the `InstagramUnfollowers.py` file.
2. Both `username` and `password` variables are strings, where `username` is your username to log into Instagram and `password` is the password to your Instagram account, so using your favorite editor, fill in that information for the `secrets.py` file like below (inbetween each of the " "):<br />
<a href="https://imgbb.com/"><img src="https://i.ibb.co/1q3Th5C/image.png" alt="image" border="0"></a><br />

## Execution of `InstagramUnfollowers.py` file
Using your terminal, go to the directory/path where `InstagramUnfollowers.py` lives and execute the file as: `./InstagramUnfollowers.py`

## A few NOTES
1. This script assumes that there is NO additional step to "sign in" after inputting your username and password such as Two Factor Authentication (2FA) on your account; otherwise, the script will fail.
2. The script will fail if either the username or password is wrong.
3. Do NOT interact with the automated web browser (e.g. clicking on links, etc.), so let the script do its thing; otherwise, an error will happen (i.e. some elements will not be found because a different page was loaded).
4. The output of the script is sent to stdout (gets displayed on the terminal), where each row represents an Instagram user that is NOT following you.
5. The script takes a while because of the `time.sleep()` function, which needs to wait for a page to load (to ensure that the elements are loaded) and this is dependent on your internet connection, so if the script fails because a page took too long to load, you can modify all `time.sleep()` instances.
6. At any point, if the scripts fails (e.g. exceptions, etc. which will populate the terminal), then it is okay to click the 'X' to exit the automated Chrome browser. :sweat_smile:
7. If everything goes well, then your unfollowers will get displayed to stdout, and the Chrome browser will close by itself.
