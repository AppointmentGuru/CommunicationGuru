class SomeObject:
    foo='bar'

MAILGUN_EMAIL = {
  "X-Mailgun-Sid": "WyI3MDlkYSIsICJpbmZvQDM4LmNvLnphIiwgImY0OWQ0MCJd",
  "domain": "appointmentguru.co",
  "message-headers": "[[\"Sender\", \"support@appointmentguru.co\"], [\"Date\", \"Thu, 28 Sep 2017 08:46:51 +0000\"], [\"X-Mailgun-Sending-Ip\", \"209.61.151.242\"], [\"X-Mailgun-Sid\", \"WyI3MDlkYSIsICJpbmZvQDM4LmNvLnphIiwgImY0OWQ0MCJd\"], [\"Received\", \"by luna.mailgun.net with HTTP; Thu, 28 Sep 2017 08:46:50 +0000\"], [\"Message-Id\", \"<20170928084650.52111.137F1AF584D57071@appointmentguru.co>\"], [\"X-Mailgun-Track-Clicks\", \"true\"], [\"To\", \"info@38.co.za\"], [\"From\", \"support@appointmentguru.co\"], [\"Subject\", \"test: 0.5043658103934473\"], [\"Mime-Version\", \"1.0\"], [\"Content-Type\", [\"multipart/alternative\", {\"boundary\": \"fb37391436f348bb8d48d6bca69ab477\"}]]]",
  "Message-Id": "<20170928084650.52111.137F1AF584D57071@appointmentguru.co>",
  "recipient": "info@38.co.za",
  "event": "delivered",
  "timestamp": "1506588412",
  "token": "24f2ce97c240bb13e6297faff35da5726fee48c754d7523679",
  "signature": "dd095fd7117542b376c4800142a020197e924224e34630c5bf9bcd674695faf8",
  "body-plain": ""
}

MAILGUN_EMAIL_NO_MESSAGE_ID = {
  "X-Mailgun-Sid": "WyI3MDlkYSIsICJpbmZvQDM4LmNvLnphIiwgImY0OWQ0MCJd",
  "domain": "appointmentguru.co",
  "message-headers": "[[\"Sender\", \"support@appointmentguru.co\"], [\"Date\", \"Thu, 28 Sep 2017 08:46:51 +0000\"], [\"X-Mailgun-Sending-Ip\", \"209.61.151.242\"], [\"X-Mailgun-Sid\", \"WyI3MDlkYSIsICJpbmZvQDM4LmNvLnphIiwgImY0OWQ0MCJd\"], [\"Received\", \"by luna.mailgun.net with HTTP; Thu, 28 Sep 2017 08:46:50 +0000\"], [\"Message-Id\", \"<20170928084650.52111.137F1AF584D57071@appointmentguru.co>\"], [\"X-Mailgun-Track-Clicks\", \"true\"], [\"To\", \"info@38.co.za\"], [\"From\", \"support@appointmentguru.co\"], [\"Subject\", \"test: 0.5043658103934473\"], [\"Mime-Version\", \"1.0\"], [\"Content-Type\", [\"multipart/alternative\", {\"boundary\": \"fb37391436f348bb8d48d6bca69ab477\"}]]]",
  "Message-Id": "123",
  "recipient": "info@38.co.za",
  "event": "delivered",
  "timestamp": "1506588412",
  "token": "24f2ce97c240bb13e6297faff35da5726fee48c754d7523679",
  "signature": "dd095fd7117542b376c4800142a020197e924224e34630c5bf9bcd674695faf8",
  "body-plain": ""
}

ZOOMCONNECT_STATUS_UPDATE = {
  "dataField": "cli:1691,app:13478,pra:363,pro:11272,",
  "messageId": "5a757c7b7736b6c1d340a0db",
  "campaign": "practitioner-363",
  "nonce-date": "20180203111524",
  "nonce": "bbf12a28-368d-45b3-acfa-42c7a458834a",
  "status": "DELIVERED",
  "checksum": "571df5cafaab4fde15de429435ce7537a3ae5259"
}

ZOOMCONNECT_CONNECT_REPLY = {
  "date": "201802031121",
  "messageId": "5a757f2a7736b6c1d340a1a4",
  "from": "+27832566533",
  "to": "INF-WnV8e3c2tsHTQKDb",
  "nonce-date": "20180203112647",
  "message": "Testing again. ",
  "nonce": "701ed8ab-ff84-4f49-a17f-79b293955c75",
  "checksum": "f4fca6b5bdbc1cfbf54c783b1db1862d5f5b3316"
}

