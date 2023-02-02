# RSS ntfy

Very small RSS notifier using [ntfy](https://ntfy.sh/). I would *highly* recommend using a self hosted ntfy instance, so that you can use whatever ntfy names you want.

It's designed for use alongside certain 'alternative frontend services'. I use it for:

- [Nitter](https://github.com/zedeus/nitter), Twitter alternative
- [Proxitok](https://github.com/pablouser1/ProxiTok), a TikTok frontend

Both of these provide RSS feeds, which are on basically every page plus `/rss`: very handy.

## Usage

### Dependencies

- Python 3
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), `pip install beautifulsoup4`
- [requests](https://requests.readthedocs.io/en/latest/) `python -m pip install requests`

### Setup

I recommend cloning the repo to a remote server (I run it on an Ubuntu server):

```sh
git clone https://github.com/julianorchard/rss-ntfy.git
```

At the moment, there is a global variable called `SERVICES`. Edit this to rename services/add a different URL for a preferred instance of whatever service you're using. 

```python
SERVICES = [{"service": "nitter", "url": "https://nitter.it/"}, 
            {"service": "proxitok", "url": "https://proxitok.pabloferreiro.es/@"}]
```

You can then use a [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) or a [systemd service](https://www.freedesktop.org/software/systemd/man/systemd.service.html) (or, on Windows, a [Task Scheduler](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) task) to run the command periodically.

## License

Under the MIT License. See [license](/LICENSE) file for more information.
