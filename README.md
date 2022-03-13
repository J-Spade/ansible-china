# ansible stuff

## Initial Setup
### ssh config
The inventory file was written on the assumption that you've already set up an ssh config with forwarding and all that good stuff. For things to work correctly, all of the hostnames need to resolve correctly, and your IT username needs to be configured as the default user. If you can connect to a unix host- for instance, wuhan- simply by typing `ssh wuhan`, then your configuration will work with the ansible inventory.

In addition to the ssh host configuration, you'll need to have an ssh key added to the `~/.ssh/authorized_keys` file for your IT user account on each of the unix hosts. Assuming you've already generated a key pair, you can do this for each host with `ssh-copy-id`.

### ssh-agent
If you've password-protected your ssh private key (which you should have), you'll want to start ssh-agent so that you don't have to constantly type your password while ansible does its thing. Starting an ssh-agent session and adding your ID is simple:
```
~/ansible$ eval `ssh-agent`
~/ansible$ ssh-add
```

## Converting from CSV
The ansible playbooks expect a `users.json` file containing a formatted list of users with their associated groups and passwords. To convert a CSV file- for instance, `users.csv`- into the correct format, run:
```~/ansible$ python3 convert_userlist.py users.csv```
The `users.json` file will be created and will be ready to go.

## Running Playbooks
To run a playbook, use `ansible-playbook`. You'll need to specify the playbook being run, and the inventory file containing the host information (`inv_china.yaml`). Each of the playbooks is configured to ask for your IT user password (without a prefix), and handles authenticating with the remote hosts. For these to work, your account needs to be able to use the `sudo` command on all of the hosts (if it can't, the host is misconfigured and needs the IT group added to sudoers.)

**Note:** In order to verify a playbook without actually making changes on the remote hosts, add the `--check` flag to the command line.

### Example: Add Users
This command will add/update users and passwords for every unix host on the network (except the kali machines):
```
~/ansible$ ansible-playbook add_users.yaml -i inv_china.yaml
```

**Note:** This command fails if a user is associated with group that does not yet exist on the host. If the new userlist includes new groups, first run the group playbook:
```
~/ansible$ ansible-playbook add_groups.yaml -i inv_china.yaml
```

### Example: Set Samba Credentials
This command will add/update samba credentials on all of the samba servers (**note**: the users must have accounts on the host already)
```
~/ansible$ ansible-playbook add_samba_users.yaml -i inv_china.yaml
```

### Example: Updating a Specific Host/Subnet
You can filter the inventory down by adding a `--limit` argument to the command.

For instance, this will add new users to the telecom domain only:
```
~/ansible$ ansible-playbook add_users.yaml -i inv_china.yaml --limit telecom
```

You can also specify a single host- for example, to update the samba credentials on a newly-configured host:
```
~/ansible$ ansible-playbook add_samba_users.yaml -i inv_china.yaml --limit suzhou
```
