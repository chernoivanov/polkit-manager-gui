import os
from typing import Dict, Union, Optional, Tuple
# module
from polkit_manager_gui.utils.paths import polkit_actions_path
from polkit_manager_gui.utils.xml.parser import XMLParser


def get_policies() -> Dict[str, Dict[str, Union[str, Dict[str, Dict[str, Union[Optional[str], Dict[str, str]]]]]]]:
    """
    Lists .policy files, parses each file with XMLParser object
    Returns a [Dict] consisting of:
        - [str] full path to .policy file
        - [str] vendor parsed from file
        - [Dict] containing:  [Dict] <action>'s <defaults>, [str] description, [str] message
    """
    policies = {}
    polkit_actions_list = os.listdir(polkit_actions_path)
    for policy_file in polkit_actions_list:
        full_policy_file_path = os.path.join(polkit_actions_path, policy_file)
        xml_parser = XMLParser(full_policy_file_path)
        actions_elements, vendor = xml_parser.parse_policy_file()
        actions = {}
        for action_element in actions_elements:
            action_dict, action_id = xml_parser.parse_action_element(action_element)
            actions[action_id] = action_dict
        policies[policy_file] = {"path": full_policy_file_path,
                                 "vendor": vendor,
                                 "actions": actions}
    return policies

def change_actions_defaults(policy: str,
                            action: str,
                            defaults: Dict[str, Union[Dict[str, str], str]]) -> Tuple[bool, Optional[str]]:
    """
    Changes <defaults> elements for given policy file using XMLParser object's method call
    Returns Tuple[bool, Optional[str]]
    """
    xml_parser = XMLParser(os.path.join(polkit_actions_path, policy))
    op_status, possible_err = xml_parser.modify_defaults_elements(action, defaults)
    return op_status, possible_err
