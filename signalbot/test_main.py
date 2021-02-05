import signalbot.__main__


def test_main_init_program():
    assert signalbot.__main__.init_program() is None


def test_main_parse_message_sentmessage():
    json = '{"envelope":{"source":"+31630030905","sourceDevice":1,"timestamp":1612267167202,"syncMessage":{"sentMessage":{"timestamp":1612267167202,"message":"Test","expiresInSeconds":0,"viewOnce":false,"mentions":[],"attachments":[],"groupInfo":{"groupId":"FmtNZAff32cV5sin4iJKcrikFd67H1LbkLsdXaSVPkI=","type":"DELIVER"},"destination":null}}}}'
    assert signalbot.__main__.parse_message(json) is None


def test_main_parse_message_datamessage():
    json = '{"envelope":{"source":"+31645606468","sourceDevice":1,"timestamp":1612267985986,"dataMessage":{"timestamp":1612267985986,"message":"!hn","expiresInSeconds":60,"viewOnce":false,"mentions":[],"attachments":[],"groupInfo":{"groupId":"OcX1j1sAF3e8yGDuFxd/sC+XKJL8TbBTOhCREc4CNXI=","type":"DELIVER"}}}}'
    assert signalbot.__main__.parse_message(json) is None
