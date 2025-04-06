import os
from typing import Dict, List, Tuple
# module
from polkit_manager_gui.utils.paths import polkit_authority_path


def parse_polkit_localauthority() -> Dict[str, List[Tuple[str, List, Dict[str, str]]]]:
    """
    Parses .pkla files in all available dirs in /var/lib/polkit-1/localauthority path
    and returns Dict with contents of those files
    """
    actions_pkla_dict = {}
    localauthority_dirs = os.listdir(polkit_authority_path)
    for la_dir in sorted(localauthority_dirs):
        full_path = os.path.join(polkit_authority_path, la_dir)
        pkla_files = os.listdir(full_path)
        for pkla_file in sorted(pkla_files):
            extracted_pkla = []
            with open(os.path.join(full_path, pkla_file), "r") as file:
                extracted_pkla = file.readlines()
            policy_block = []
            grouped_extracted_pkla = []
            try:
                if extracted_pkla[-1] != "\n":
                    extracted_pkla.append("\n")
            except IndexError:
                pass
            for line in extracted_pkla: 
                if not line == "\n":
                    policy_block.append(line)
                else:
                    grouped_extracted_pkla.append(policy_block)
                    policy_block = []
            for block in grouped_extracted_pkla:
                actions = []
                name = None
                identity = None
                defaults = {}
                for line in block:
                    if line.startswith("Action"):
                        actions = line.split("=")[-1].split(";")
                    elif line.startswith("["):
                        name = line.rstrip()
                    elif line.startswith("Identity"):
                        identity = line.split("=")[-1].split(";")
                    elif line.startswith("ResultAny"):
                        defaults["allow_any"] = line.split("=")[-1].rstrip() 
                    elif line.startswith("ResultInactive"):
                        defaults["allow_inactive"] = line.split("=")[-1].rstrip()
                    elif line.startswith("ResultActive"):
                        defaults["allow_active"] = line.split("=")[-1].rstrip()
                actions = [action.rstrip() for action in actions]
                actions = [action for action in actions if action]
                if actions:
                    for action in actions:
                        action = action.rstrip()
                        if actions_pkla_dict.get(action):
                            value_list = actions_pkla_dict[action]
                            value_list.append((name, identity, defaults, pkla_file))
                            actions_pkla_dict[action] = value_list
                        else:
                            actions_pkla_dict[action] = [(name, identity, defaults, pkla_file)]
    return actions_pkla_dict
