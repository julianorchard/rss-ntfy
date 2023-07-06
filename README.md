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
- lxml-xml parser for BeautifulSoup

```sh
pip install -i requirements.txt
```

### Configuration

Edit the `config.yaml` file:

```yaml
# Example configuration
---

proxitok:
  service: proxitok
  rss-url: https://proxitok.pabloferreiro.es/@{{ user }}/rss
  descriptor: 🎶 TikTok

teddit:
  service: teddit
  rss-url: https://teddit.net/r/{{ sub }}?api&type=rss
  descriptor: 🎩 Reddit post

```

At this point the contents of the handlebar type substitutions (`{{ }}`) don't
matter; this will be replaced with the users/subreddits/thing-you-want-to-follow
in the files in the `rss-ntfy/` folder.

*TODO: this is a not-nice way of doing this, possibly use more yaml*

You can then use a [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) or a [systemd service](https://www.freedesktop.org/software/systemd/man/systemd.service.html) (or, on Windows, a [Task Scheduler](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) task) to run the command periodically.

## License

Under the MIT License. See [license](/LICENSE) file for more information.
