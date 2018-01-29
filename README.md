# AWS Infrastructure
A collection of components for the building of an AWS infrastructure.

# Requirements:
- Ansible
- Boto3

# Usage:
```
- hosts: localhost
  connection: local
  tasks:
    - ec2_availibity_zones:
        region: 'us-west-2'
```

or

```
- hosts: localhost
  connection: local
  tasks:
    - ec2_availibity_zones:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: 'us-west-2'
```
