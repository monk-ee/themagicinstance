#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
__author__ = 'Monkee Magic <magic.monkee.magic@gmail.com>'
__version__ = '0.0.1'
__license__ = 'GPLv3'
__source__ = 'http://github.com/monk-ee/themagicinstance'

"""
slicethree.py - create an instance.

Copyright (C) 2014 Lyndon Swan <magic.monkee.magic@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2

import boto3

client = boto3.client('cloudformation')

template = Template()

keyname_param = template.add_parameter(Parameter(
        "KeyName",
        Description="Name of an existing EC2 KeyPair to enable SSH "
                    "access to the instance",
        Type="String",
        Default="MyKeyName",
))

name_param = template.add_parameter(Parameter(
        "Name",
        Description="Name of the Instance ",
        Type="String",
        Default="SliceThree",
))

customer_param = template.add_parameter(Parameter(
        "Customer",
        Description="Customer",
        Type="String",
        Default="Magic",
))

environment_param = template.add_parameter(Parameter(
        "Environment",
        Description="Environment",
        Type="String",
        Default="Development",
))

ec2_instance = template.add_resource(ec2.Instance(
        "SliceThree",
        ImageId="ami-f5f41398",
        InstanceType="t2.nano",
        InstanceProfileRole="applicationInstance",
        KeyName=Ref(keyname_param),
        SecurityGroupIds="sg-a45645ae",
        SubnetId="subnet-a56576",
        Tags=[
            {
                'Key': 'Name',
                'Value': Ref(name_param)
            },
            {
                'Key': 'Customer',
                'Value': Ref(customer_param)
            },
            {
                'Key': 'Environment',
                'Value': Ref(envrionment_param)
            }
        ]
))

template.add_output([
    Output(
            "InstanceId",
            Description="InstanceId of the newly created EC2 instance",
            Value=Ref(ec2_instance),
    )
])


try:
    response = client.create_stack(
            StackName='SliceThree',
            TemplateBody=template.to_json(),
            DisableRollback=False,
            TimeoutInMinutes=1,
            OnFailure='ROLLBACK',
            Tags=[
                {
                    'Key': 'Environment',
                    'Value': 'Development'
                },
                {
                    'Key': 'Name',
                    'Value': 'SliceThree'
                },
                {
                    'Key': 'Customer',
                    'Value': 'Magic'
                },
            ]
    )
except Exception as e:
    print("Something went wrong", e)