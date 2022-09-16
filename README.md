# Teamsniper
Teamsniper is a tool for fetching keywords in a Microsoft Teams such as (passwords, emails, database, etc.). 


# Usage

**Help Options**

```
usage: Teamsniper.py [-h] [-d DATABASE] [-a AUTHTOKEN] [-s SEARCH]

Teamsniper is a tool for fetching the given keyworks in Microsoft Teams.

options:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        Sqlite Database for the Cookies, default: AppData\Microsoft\Teams\Cookies,
                        AppData\Microsoft\Teams\Local Storage\leveldb
  -a AUTHTOKEN, --Authtoken AUTHTOKEN
                        Auth-Token File Location, by default the auth token key will be extracted from the Sqlite
                        Database.
  -s SEARCH, --search SEARCH
                        Keywords, by default: Password. You can add multiple keywords ex: Passwords,Admin,Database
```
In Teamsniper you have all the power to give it the database if it in the different path. by using -d / --database then the database location  
Example:   
```bash
python .\Teamsniper.py -d /root/Desktop/Cookies
```
Also, you can pass the auth-key directly by using -a / --authtoken then the auth token file location.  
Example:  
```bash
python .\Teamsniper.py -a /root/Desktop/AuthKey
```
Also, you can set your keywords to by using -s option.
```bash
python .\Teamsniper.py -s "Password,Mail,Database"
```

And the final output should be in a output.txt file.
**output**
```Bash
PS C:\Teamsniper> python .\Teamsniper.py -a Authkey -s "Password,Mail"
[+] Auth-key added to headers
[+] Keyword: Password
[+] Results found: 3
[+] saved output.
[+] Keyword: Mail
[+] Results found: 2
[+] saved output.
```

# Credits
1. [@billtoulas](https://twitter.com/billtoulas) for posting about the unencrypted (Cleartext) way of storing the cookies.
2. [@HackingLZ](https://twitter.com/HackingLZ) the CTO of TrustedSec for sharing this on twitter. 

