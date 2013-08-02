import json
from sys import exit, stdout, argv

file1 = None
out = stdout
if len(argv) == 2:
    file1 = argv[1]
elif len(argv) == 3:
    file1 = argv[1]
    outfilestream = open(argv[2], "w")
else:
    print("""Usage: {0} In-File [OutFile]""".format(argv[0]))
    exit(1)

def readNextJsonMessage(handle, assertMsg=None):
    """
    Decode the first non-empty line from handle as json.
    If assertMsg is given raise an Error if the msg-attribute did not match or no Message was found.
    Also skip every Ping messages
    """
    s = "\n"
    while(s == "\n"):
        s = handle.readline()
        if s == "":
            if assertMsg is not None:
                raise "EOF instead of {0}".format(assertMsg)
            return None
    message = json.loads(s)
    if assertMsg is not None and message['msg'] != assertMsg:
        raise "{0} instead of {1}".format(message['msg'], assertMsg)
    return message

def writeMessage(message):
    outfilestream.write(json.dumps(message))
    outfilestream.write("\n\n\n")

with open(file1, "r") as handle:
    #Updates from 0.95.1 to 0.96.0
    m = readNextJsonMessage(handle, "ServerInfo")
    if m['version'] != "0.95.1":
        print("Can not update from that version.")
        exit(1)
    else:
        m['version'] = "0.96.0"
        writeMessage(m)

    m = readNextJsonMessage(handle)
    while m != None:
        if m['msg'] == "NewEffects":
            for e in m['effects']:
                if 'SummonUnit' in e:
# From
# {"SummonUnit":{"target":{"color":"black","position":"2,1"},"unit":{"cardTypeId":96,"isToken":false}}}
# To
# {"SummonUnit":{"target":{"color":"white","position":"2,0"},"card":{"id":16252046,"typeId":113,"tradable":true,"isToken":false,"level":0}}}
                    e['SummonUnit']['card'] = {
                        'id': 0,
                        'typeId': e['SummonUnit']['unit']['cardTypeId'],
                        'tradable': True,
                        'isToken': e['SummonUnit']['unit']['isToken'],
                        "level":0
                    }
                    del e['SummonUnit']['unit']
        writeMessage(m)
        m = readNextJsonMessage(handle)


