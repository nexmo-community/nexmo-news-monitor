# Nexmo News Monitor

This is a simple Python application that monitors a site of your choice for a specific keyword using the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) library. If found, it sends you an SMS using Nexmo's [Messages API](https://developer.nexmo.com/messages/overview).

## Dependencies

The application has been created using Python 3 and has `PyJWT` and `beautifulsoup4` as dependencies. Install them using `pip`:

```
pip3 install PyJWT
pip3 install beautifulsoup4
```

## Configuration

Copy `example.env` to `.env`.

[Create a Messages API application](https://developer.nexmo.com/messages/code-snippets/create-an-application#how-to-create-a-messages-and-dispatch-application-using-the-dashboard) and make a note of the `application_id` and the location of the `private.key` file that was downloaded. Place the `private.key` file in the root of the project directory.

Configure the following in `.env`:

* `MESSAGES_APPLICATION_ID`: The `application_id`.
* `MESSAGES_KEY_FILE`: The file that contains your private key, e.g. `private.key`.
* `TO_NUMBER`: The mobile phone number that you want to send alerts to.
* `FROM_NUMBER`: Either the Nexmo virtual number or an alphanumeric string, e.g. `NEWSMONITOR`.
* `SITE_NAME`: The name of your site, e.g. `COOL NEWS`.
* `SITE_URL`: The site URL. You can also use a local HTML file here for testing and one is provided for you. (`coolnews.html`).
* `POLL_INTERVAL`: How often you want the script to check the site, in seconds.
* `SEARCH_KEYWORD`: The search term.

## Execution

Run the script:

```
python3 monitor.py
```

The script runs in a continuous loop, downloading a new version of the website every `POLL_INTERVAL` seconds and checking for the `SEARCH_KEYWORD`.

If it finds an occurence of the `SEARCH_KEYWORD` it sends an SMS to the `TO_NUMBER` you specified and breaks out of the loop.

## Notes

* At the time of writing, the Messages API is not supported in the Nexmo Python client library. The application uses the provided `SMSClient` class to send SMS messages.
* The application currently runs in a loop but would probably be better suited to a `cron` job or similar.
* This only shows very basic use of the Beautiful Soup library. You can do so much more with it. Perhaps try and extend the application to search for the keyword in headings only? See the [Beautiful Soup docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).


