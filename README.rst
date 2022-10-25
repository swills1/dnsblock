# dnsblock

**What is dnsblock:**
dnsblock is a simple Python library used to automatically generate zone files from maintained Blocklists for various recurisve DNS resolvers.

**What is a Blocklist:**
A blocklist is a maintained list of hostnames known to track, advertise, engage in malicious activiy, etc.
These lists are constantly updated / maintained and available online by various people and groups.

**What does dnsblock do:**
The dnsblock library allows a user to build a master list of Blocklists they follow and then automatically pull in every entry from each blocklist and generate a zone file based on whatever recursive DNS server they happen to use. Examples being - Unbound and DNSMasq.

With dnsblock, you can build a master text file consisting of numerous Blocklists.
The library will query every Blocklist, pull in every entry thay isn't a comment, and then generate a zone file that works with your specific recursive DNS server.

This benefits you in several ways:
1. You don't have to go to each Blocklist and pull out the entires and then build a zone file.
2. dnsblock uses threading and can process multiple blocklists very quickly
3. You can set up a Cron Job, Systemd Timer, or Scheduled Task to automatically rebuild your zone file as Blocklists are updated.
4. dnsblock also collects all urls that could and could not be reached. Helping you maintain which Blocklists are no longer maintained or having an issue.
5. The library also allows you to pull in a count of entries from each blocklist and a total count of all combined Blocklist entries.
6. The library allows a high level of customization in regard to generating zone files while being very simple to use.

**What else can dnsblock do:**
The library also has cli commands that allow you to accomplish basic tasks such as get entry counts, or generate a one off zone file based on specific urls.

**Usage:**

**Documentation:**