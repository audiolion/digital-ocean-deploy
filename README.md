# Digital Ocean VPS Setup

## Instructions for Automated VPS Setup with Fabric
Go through fabfile and change appropriate settings
```
env.password = ''
env.hosts = ['192.186.1.1', ...]
env.new_user_full_name = ''
env.ssh_key_dir = '~/...'
```

If you dont have an ssh_key_dir, create a new ssh key pair, naming it prod_key in the directory of your choosing and edit the path to the `env.ssh_key_dir` above

Install fabric (using a virtualenv is recommended, python2.7 required to use fabric)
`pip install fabric==1.10.2`

Run setup script, ensuring you have plugged in your server settings, executing the following from your local command line:
`fab bootstrap`
You will be prompted for the new user and then the script will connect to the server again with that user to complete the setup

## Instructors for Ansible Playbook

Install Ansible `pip install ansible==1.9.2`, using `python2.7` and a `virtualenv` is highly recommended
