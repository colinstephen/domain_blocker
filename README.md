# Domain Blocker

A simple Python command line script that appends domains to the system hosts file in order to block them. Requires root privileges.

## Usage

```
root$ domain_blocker.py [-h] -from_file FROM_FILE [-hosts_file HOSTS_FILE]
```

Use optional argument `-h` to show command line help.

## Required Files

`FROM_FILE` should be a text file containing domain names to block, one per line. Domains that are already blocked will be ignored so they do not need to be removed from this file. In addition the script adds `www` versions of all domains, so these are not needed in the source file.

`HOSTS_FILE` should be the system hosts file used for resolving domains. On most systems this will be `/etc/hosts` (which points to `/private/etc/hosts` on Macs) and this is the defualt.

## What It Does

Each new domain in the `FROM_FILE` and its `www`-variant is appended to the `HOSTS_FILE` as a redirect to IP `127.0.0.1`.

## Motivation

To get work done, maintain a list of any domains that you never want to waste time browsing on your work computer, in a text file. Point this script to the file, for example in a scheduled CRON job that runs with root privileges. You will then be blocked from accessing any of the sites.

```
# crontab
# update every 10 mins
*/10 * * * * /path/to/domain_blocker.py -from_file /path/to/domains.txt
```

### Hint

This works best on a *locked-down* computer where you can't just use sudo to edit the hosts file to reverse the changes. I recommend working under a regular user account without sudo privileges, and giving your impossible-to-memorise admin account password to a friend or leaving it at the office/home as appropriate. This works wonders for your productivity.
