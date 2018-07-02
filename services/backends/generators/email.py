
def email_reply(id="123"):
    return {
        "message-id": id,
        "sender": "joe@soap.com",
        "recipient": "jane@soap.com",
        "subject": "re: hello",
        "body-plain": "reply email message"
    }