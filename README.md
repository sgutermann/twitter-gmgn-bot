# twitter-gmgn-bot

Simple Bot for posting GM and GN post automatically with basic usage of a llama Model. 
This may not be what you expect, but it is what I arrived at after doing some testing. 
Main objective was to test the twitter API as well as use a small simple llama model in my basement,
sitting on a VM (4 Cores and 16 GB Ram) to do some simple work. I added the weather feature just for fun.

## get setup

Get your machine setup and install the needed python modules (check the import of the script, I did not do a requirements file). 
Hey, give me a break I am new to this, I installed it via apt on my debian machine.

If you are on debian or ubuntu try:

`curl -fsSL https://ollama.com/install.sh | sh`

or better yet, visit the website and check the install yourself. The llama I used was the smalles one I could find:

`ollama pull llama3.2:1b`

test it:

`ollama run llama3.2:1b`

## get running

Obviously clone my repo. I had it installed under "/var/opt/" so I hope I do not have too many direkt paths in the script,
but you might want to check that first.

If you have all your X (aka Twitter) API credentials dropped into the twitterbot.env file you may want to test your connection.
This seemed to be taking some time in my case as I was not clear on APIv2 and APIv1 differences at first.

Use the testpost.yp for that, it will help :)

### cron jobs

The script is setup to run on basic Linux cron Jobs.

To schedule posts (GM) Post at 8:00 AM your cron could look like this:

0 8 * * * python3 /path/to/twitterbot.py GM "/path/to/images" "Berlin" "#solana"

For a (GN) Post at 11:00 PM it might look like this:

0 23 * * * python3 /path/to/twitterbot.py GN "/path/to/images" "Berlin" "#memecoins"

This setup ensures flexibility, allowing you to configure each post with a location for weather, images, and hashtags dynamically.

Note: The script always expects the 4 (four) parameters, so if you do not want pictures or weather just use "none"


