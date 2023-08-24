
### imgdt
### v0.0.2
### MikiTwenty
class stdoformat:
    TEXT = '\33[37m'
    SUCCESS = '\33[92m'
    WARNING = '\33[93m'
    LOADING = '\33[94m'
    INFO = '\33[0m'
    ERROR = '\33[91m'

def log(message, msgtype=stdoformat.TEXT):
    if msgtype == stdoformat.TEXT:
        print(f"\n{msgtype}>> {message}")
    elif msgtype == stdoformat.SUCCESS:
        print(f"{msgtype}[COMPLETED] | {message}")
    elif msgtype == stdoformat.ERROR:
        print(f"{msgtype}[ERROR] | {message}")
    elif msgtype == stdoformat.LOADING:
        print(f"{msgtype}{message}", end='\r')
    elif msgtype == stdoformat.INFO:
        print(f"{msgtype} - {message}", end='')