#!/usr/bin/env python3

from configparser import ConfigParser
import sys
import os

def setup():
    global config, filename
    config = ConfigParser()
    filename = os.getenv('HOME')+"/.aws/credentials"
    if not os.path.exists(filename):
        print("Error. '{}' not found.".format(filename))
        sys.exit(1)
    config.read(filename)

def list_all():
    setup()
    for profile in config.sections():
        print(profile)

def show_default():
    setup()
    default_aws_access_key_id = config.get('default', 'aws_access_key_id')
    for section in config.sections():
        for k, v in config.items(section):
            if v == default_aws_access_key_id:
                print(section)
                sys.exit(0)

def set_default(profile):
    setup()
    if profile not in config.sections():
        print("Error. Profile '{}' not found.".format(profile))
        sys.exit(1)
    config.remove_section('default')
    config.add_section('default')
    config.set('default', 'aws_access_key_id', config.get(profile, 'aws_access_key_id'))
    config.set('default', 'aws_secret_access_key', config.get(profile, 'aws_secret_access_key'))
    if config.get(profile, 'aws_session_token', fallback=False):
        config.set('default', 'aws_session_token', config.get(profile, 'aws_session_token'))
    with open(filename, 'w') as configfile:
        config.write(configfile)
        configfile.close()

if __name__ == "__main__":
    e = "Options: 'list_all', 'show_default', 'set_default [profile]'"
    if len(sys.argv) < 2:
        print(e)
        sys.exit(1)
    if "set" in sys.argv[1] and len(sys.argv) > 2:
        set_default(sys.argv[2])
    elif "show" in sys.argv[1]:
        show_default()
    elif "list" in sys.argv[1]:
        list_all()
    else:
        print(e)
        sys.exit(1)
