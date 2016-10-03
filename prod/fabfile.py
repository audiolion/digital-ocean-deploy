from os import environ
from fabric.api import *
from fabric.context_managers import cd
from fabric.contrib.files import sed

"""
   Fabric file to upload public/private keys to remote servers
   and set up non-root users. Also prevents SSH-ing in with the
   root user. Fill in the following blank fields then run this
   Fabric script with "fab bootstrap".
"""

# run the bootstrap process as root before it is locked down
env.user = 'root'
env.password = ''

# all IP address or hostnames of the servers you want to put
# your SSH keys and authorized_host files on
env.hosts = ['192.168.1.1']

env.new_user_full_name = 'Ryan Castner'

env.new_user = 'deployer'
env.new_user_group = 'deployers'

# local filesystem directory where your prod_key.pub and
# authorized_keys files are located (they will be scp'd
# to target hosts) don't include a trailing slash
env.ssh_key_dir = '~/.ssh/digitalocean'

"""
    The following functions should not need to be modified to
    complete the bootstrap process.
"""
def bootstrap():
    local('ssh-keygen -R %s' % env.host_string)
    sed('/etc/ssh/sshd_config', '^UsePAM yes', 'UsePAM no')
    sed('/etc/ssh/sshd_config', '^PermitRootLogin yes', 'PermitRootLogin no')
    sed('/etc/ssh/sshd_config', '^#PasswordAuthentication yes', 'PasswordAuthentication no')
    _create_privileged_group()
    _create_privileged_user()
    _upload_keys(env.new_user)
    run('service ssh reload')

def _create_privileged_group():
    run('/usr/sbin/groupadd' + env.new_user_grp)
    run('mv /etc/sudoers /etc/sudoers-backup')
    run('(cat /etc/sudoers-backup ; echo "%' + env.new_user_grp + ' ALL=(ALL) ALL") > /etc/sudoers')
    run('chmod 440 /etc/sudoers')

def _create_privileged_user():
    run('/usr/sbin/useradd -c "%s" -m -g %s %s' % \
        (env.new_user_full_name, env.new_user_grp, env.new_user))
    run('/usr/bin/passwd %s' % env.new_user)
    run('/usr/sbin/usermod -a -G ' + env.new_user_grp + ' ' + env.new_user)
    run('mkdir /home/%s/.ssh' % env.new_user)
    run('chown -R %s /home/%s/.ssh' % (env.new_user, env.new_user))
    run('chgrp -R %s /home/%s/.ssh' % (env.new_user_grp, env.new_user))

def _upload_keys(username):
    local('scp ' + env.ssh_key_dir + '/prod_key.pub ' + env.ssh_key_dir + '/authorized_keys ' + \
          username + '@' + env.host_string + ':~/.ssh')
