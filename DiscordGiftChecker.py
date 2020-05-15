import requests # For making web requests
import random
from multiprocessing import Pool # Multi-Threading
from multiprocessing import freeze_support # Windows Support
import string

proxies = [line.rstrip('\n') for line in open("proxies.txt", 'r')]

def get_random_alphaNumeric_string(stringLength=16):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


def checkCode(code):
    proxyNumber = random.randint(0,len(proxies)) # Get a random proxy from the proxy list
    code = get_random_alphaNumeric_string(16)
    try:
        response = requests.get('https://discord.com/api/v6/entitlements/gift-codes/' + code, proxies={"http": "http://" + proxies[proxyNumber], "https": "https://" + proxies[proxyNumber]})
        if("application_id" in response.text):
            print("[Good Code] " + code)
            workingfile = open("working.txt", "a")
            workingfile.write(get_random_alphaNumeric_string(16) + "\n")
            workingfile.close()
        elif("Unknown" in response.text):
            print("[Bad Code] " + code)
        else:
            print("[Ratelimited Proxy] " + proxies[proxyNumber])
    except Exception as e:
        print("[Bad Proxy]" + proxies[proxyNumber])

def main():
    numThreads = float(input("How many threads would you like to use? "))
    count = int(input("How many codes would you like to check? "))
    freeze_support()
    numCodes = range(count)

    pool = Pool(int(numThreads))
    pool.map(checkCode, numCodes)

    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
