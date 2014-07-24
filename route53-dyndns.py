import requests
import argparse

def makeConnection(keyid = None, secret = None, region = "us-west-2"):
    print ""

def main(args):
    if args.keyid and args.secret:
        makeConnection(keyid = args.keyid, secret = args.secret)
    elif args.keyid or args.secret:
        print "Full AWS credentials needed. Did you specify access and secret keys?"
        exit()
    else:
        makeConnection()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="""Pulls current IP from
        http://wtfismyip.com/json and updates Amazon Route 53 DNS records. 
        Requires boto to be installed. By default, %(prog)s will utilize your
        system's AWS_CREDENTIAL_FILE environment variable to define your AWS 
        connection credentials for boto configuration.""")

    argparser.add_argument('--keyid', required=false, type=str, help="""
        Used to specify your AWS access key ID. Overridden by -c/--cfg. Must 
        be used alongside --secret.""")
    argparser.add_argument('--secret', required=false, type=str, help="""
        Used to specify your AWS secret access key. Overridden by -c/--cfg. 
        Must be used alongside --keyid.""")
    argparser.add_argument('-r', '--region', required=false, type=str, help="""
        Used to specify the AWS/Route 53 region you wish to connect to. Default:
             us-west-2""")

    args = argparser.parse_args()

    main(args = args)