import requests
import argparse
from time import sleep
import boto.route53

def makeConnection(keyid = None, secret = None, connSource = None, region = "us-west-2"):
    """Makes a connection to AWS Route 53 and returns that connection as an object."""
    if connSource == "user":
        r53 = boto.route53.connect_to_region(region, aws_access_key_id = keyid,
                                             aws_secret_access_key = secret)
    elif connSource == "file":
        r53 = boto.route53.connect_to_region(region)
    else:
        print "Please specify a source for connection credentials."
        exit()
    return r53

def getIpAddress():
    """Gets your IP from WTF Is My IP and returns it as a string."""
    return "%s" % requests.get('http://wtfismyip.com/json').json()['YourFuckingIPAddress']

def getRecord(zone = None, recordName = None, connection = None, root = None):
    """Connects to a Route 53 zone and gets a specified record. Returns record and zone as objects."""
    if not (zone and connection) and not (recordName or root):
        print "Please provide a zone, a record name, and a Route 53 connection object."
        exit()
    z = connection.get_zone("%s." % zone)
    if root:
        rec = z.get_a(zone)
        return rec, z
    recs = z.get_records()
    for rec in recs:
        #I'm so sorry for this next bit. It 
        if rec.name.replace(".%s." % zone, "") == recordName:
            return rec, z
    print "Couldn't find any matching records within zone %s." % zone

def updateRecord(record = None, ipaddr = None, zone = None):
    """Updates a specified record with a new IP, if required."""
    if not (record and ipaddr and zone):
        print "Please provide a record object, IP address, and zone object."
        exit()
    if ipaddr not in record.resource_records:
        status = zone.update_record(record, ipaddr)
        status.update()
        while not ("%s" % status) == "<Status:INSYNC>":
            print "Zone file not updated yet, checking again in 30 seconds."
            sleep(30)
            status.update()
        print "%s is now set to %s." % (record.name, ipaddr)
    else:
        print "IP address is already correct for this record."

def main(args):
    if args.keyid and args.secret:
        r53 = makeConnection(keyid = args.keyid, secret = args.secret, connSource = "user")
    elif args.keyid or args.secret:
        print "Full AWS credentials needed. Did you specify access and secret keys?"
        exit()
    else:
        r53 = makeConnection(connSource = "file")
    ipaddr = getIpAddress()
    r, z = getRecord(zone = args.zone, recordName = args.subdomain, connection = r53, 
                     root = args.root)
    updateRecord(record = r, ipaddr = ipaddr, zone = z)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="""Pulls current IP from
        http://wtfismyip.com/json and updates Amazon Route 53 DNS records. 
        Requires boto to be installed. By default, %(prog)s will utilize your
        system's AWS_CREDENTIAL_FILE environment variable to define your AWS 
        connection credentials for boto configuration.""")
    argparser.add_argument('--keyid', required=False, type=str, help="""
        Used to specify your AWS access key ID. Overridden by -c/--cfg. Must 
        be used alongside --secret.""")
    argparser.add_argument('--secret', required=False, type=str, help="""
        Used to specify your AWS secret access key. Overridden by -c/--cfg. 
        Must be used alongside --keyid.""")
    argparser.add_argument('-r', '--region', required=False, type=str,
        default='us-west-2', help="""Used to specify the AWS/Route 53 region 
        you wish to connect to. Default: us-west-2""")
    argparser.add_argument('-z', '--zone', required=True, type=str, help="""
        Used to specify your Route 53 zone. Use the format "domain.tld" without
         the trailing period. %(prog)s will append the trailing period for you.""")
    argparser.add_argument('-s', '--subdomain', required=False, type=str, help="""
        Used to specify the record you wish to modify within the specified zone.""")
    argparser.add_argument('--root', required=False, action='store_true', default=False,
                           help="""Modify the root-level A record.""")
    args = argparser.parse_args()
    if not (args.subdomain or args.root):
        print "Please specify a subdomain or use the --root option."
        exit()
    main(args = args)