#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'maintainer'
}

DOCUMENTATION = '''
---
module: ec2_avail_zones

short_description: Grab availability zone info.

version_added: "2.4"

description:
    - "A module to grab all information about availability zones for a certain region"

options:
    aws_access_key:
        description:
            - AWS Access Key
        required: false
    aws_secret_key:
        description:
            - AWS Secret Key
        required: false
    region:
        description:
            - What region you wish to query.
        required: true

extends_documentation_fragment:
    - ec2

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Get Info
- name: With Keys
  ec2_avail_zones:
    aws_access_key: "AccessKey"
    aws_secret_key: "SecretKey"
    region: "RegionName"

# Without keys
- name: Without Keys
  ec2_avail_zones:
    region: "RegionName"

'''

RETURN = '''
message:
    description: Returns a list of dictionaries.
'''

from ansible.module_utils.basic import AnsibleModule
try:
    import boto3
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

def main():
    if not HAS_BOTO:
        module.fail_json(msg='boto3 required for this module')

    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        region=dict(type='str', required=True),
        aws_access_key=dict(type='str', required=False),
        aws_secret_key=dict(type='str', required=False),
        aws_session_token=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        zones=list()
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )


    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    if not module.params['region']:
        module.fail_json(msg="Region not specified.")

    try:
        ec2 = boto3.setup_default_session(region_name=module.params['region'])
        if module.params['aws_session_token'] and module.params['aws_access_key'] and module.params['aws_secret_key']:
            ec2 = boto3.client('ec2',
                aws_access_key_id=module.params['aws_access_key'],
                aws_secret_access_key=module.params['aws_secret_key'],
                aws_session_token=module.params['aws_session_token'])
        elif module.params['aws_access_key'] and module.params['aws_secret_key']:
            ec2 = boto3.client('ec2',
                aws_access_key_id=module.params['aws_access_key'],
                aws_secret_access_key=module.params['aws_secret_key'])
        else:
            ec2 = boto3.client('ec2')

        filters = [{'Name':'state','Values':['available']}]
        result['zones'] = ec2.describe_availability_zones(Filters=filters)['AvailabilityZones']
        result['changed'] = True
    except Exception as e:
        result['changed'] = False
        module.fail_json(msg=e.message)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
