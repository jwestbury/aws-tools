import requests
import argparse

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="""Pulls current IP from
        http://wtfismyip.com/json and updates Amazon Route 53 DNS records.""")

    argparser.add_argument('-c', '--cfg', action='store_true', required=False,
        help="""If specified, %(prog)s will utilize your system's
        AWS_CREDENTIAL_FILE environment variable to define the boto config. 
        Otherwise, you must specify your AWS access key ID and your 
        AWS secret access key.""")
    argparser.add_argument('--keyid', required=false, type=str, help="""
        Used to specify your AWS access key ID. Overridden by -c/--cfg. Must 
        be used alongside --secret.""")
    argparser.add_argument('--secret', required=false, type=str, help="""
        Used to specify your AWS secret access key. Overridden by -c/--cfg. 
        Must be used alongside --keyid.""")

    args = argparser.parse_args()

    main(args = args)