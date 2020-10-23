#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2018 Juergen Etzlstorfer (Dynatrace) <juergen.etzlstorfer@dynatrace.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dynatrace_comment
version_added: "2.3"
author: "Juergen Etzlstorfer (@jetzlstorfer)"
short_description: Comment on Dynatrace detected problems
description:
  - Push a comment to a Dynatrace problem ticket
options:
  tenant_url:
    description:
      - Tenant URL for the Dynatrace Tenant
    required: true
    type: str
  api_token:
    description:
      - Dynatrace API Token
    required: true
    type: str
  problem_id:
    description:
      - Dynatrace Problem ID to add the comment to
    required: true
    type: str
  comment:
    description:
      - Content of comment to push to Dynatrace
    required: true
    type: str
  user:
    description:
      - User that pushes the comments
    required: true
    type: str
  context:
    description:
      - Source where the comment originates from (default Ansible)
    required: false
    type: str
requirements: []
'''

EXAMPLES = '''
- dynatrace_comment:
    tenant_url: https://mytenant.live.dynatrace.com
    api_token: XXXXXXXX
    comment: 'Comment sent from Ansible'
    user: 'user@dynatrace.com'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
# from ansible.module_utils.six.moves.urllib.parse import urlencode
import json

# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            tenant_url=dict(required=True),
            api_token=dict(required=True),
            problem_id=dict(required=True),
            comment=dict(required=True),
            user=dict(required=True),
            context=dict(required=False)
        ),
        supports_check_mode=True
    )

    # build list of params
    params = {}

    # set standard context
    params["context"] = "Ansible"

    for item in ["comment", "user", "context"]:
        if module.params[item]:
            params[item] = module.params[item]

    # If we're in check mode, just exit pretending like we succeeded
    if module.check_mode:
        module.exit_json(changed=True)

    # Send the comment to Dynatrace and attach it to a problem
    dt_url = module.params["tenant_url"] + "/api/v1/problem/details/" + module.params["problem_id"] + "/comments"
    # data = urlencode(params)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Api-Token ' + module.params['api_token']
    }

    # FAIL FOR DEBUG PURPOSES - TO INSPECT PAYLOAD #####
    # module.fail_json(msg=json.dumps(params))
    #

    ####
    # SEND COMMENT EVENT TO DYNATRACE
    ####
    try:
        response, info = fetch_url(module, dt_url, data=json.dumps(params), headers=headers)

        if info['status'] in (200, 201):
            module.exit_json(changed=True)
        elif info['status'] == 401:
            module.fail_json(msg="Token Authentification failed.")
        else:
            module.fail_json(msg="Unable to send comment to Dynatrace: %s" % info)
    except Exception as e:
        module.fail_json(msg="Failure: " + e.message)


if __name__ == '__main__':
    main()
