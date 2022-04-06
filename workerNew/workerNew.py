import requests
def send_email(email_address):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox20108458b5c0424a9d8a6a7c382e7cab.mailgun.org",
		auth=("api", "2169a3420c6eecfe3956a081528b4138-38029a9d-274c22c0"),
		data={"from": "Excited User <mailgun@sandbox20108458b5c0424a9d8a6a7c382e7cab.mailgun.org>",
			"to": email_address,
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})

    # if resp.status_code != 200:
    #     return 0
    # return 1        