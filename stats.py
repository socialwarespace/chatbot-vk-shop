from vk_acc import prs as vk

def load_messages():
    messages = []
    count = 1
    while len(messages) < count:
        resp = vk.method("messages.get", {"count": 200,
                                          "offset": len(messages),
                                          "out": 1})
        messages += resp['items']
        count = resp['count']
    return messages
