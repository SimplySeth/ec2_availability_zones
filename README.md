# ec2_availability_zones
Ansible module to get availability zones

# Requirements:
- Ansible
- Boto3

# Usage:
```
- hosts: localhost
  connection: local
  tasks:
    - ec2_availability_zones:
        region: 'us-west-2'
```

or

```
- hosts: localhost
  connection: local
  tasks:
    - ec2_availability_zones:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: 'us-west-2'
        state: available
```
