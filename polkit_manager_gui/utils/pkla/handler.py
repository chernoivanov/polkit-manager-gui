import os
import re
from typing import Tuple, Dict, List, Union
# module
from polkit_manager_gui.utils.paths import polkit_authority_path


def remove_explicit_privelege(file: str, name: str, action: str) -> Tuple[bool, str]:
    """
    Removes explicit priveleges
    """
    localauthority_dirs = os.listdir(polkit_authority_path)
    suitable_file = None
    for la_dir in sorted(localauthority_dirs):
        full_path = os.path.join(polkit_authority_path, la_dir)
        pkla_files = os.listdir(full_path)
        for pkla_file in sorted(pkla_files):
            if file == pkla_file:
                file_lines = []
                with open(os.path.join(full_path, pkla_file), "r") as _pkla_file:
                    file_lines = _pkla_file.readlines()
                for line in file_lines:
                    if line.startswith("["):
                        if line.rstrip() == f"[{name}]":
                            suitable_file = os.path.join(polkit_authority_path, la_dir, pkla_file)
    # working with file where action is written
    suitable_file_lines = []
    try:
        with open(suitable_file, "r") as _pkla_file:
            suitable_file_lines = _pkla_file.readlines()
    except TypeError as error:
        return False, str(error)
    # check if there are any entries beside the one we're looking for
    rule_entries = sum(1 for line in suitable_file_lines if line.startswith("["))
    if rule_entries > 1:
        # look for certain name, get slice in <suitable_file>
        start_index = suitable_file_lines.index(f"[{name}]\n")
        suitable_file_lines_slice = suitable_file_lines[start_index + 1:]
        slice_to_remove = [f"[{name}]\n"]
        for _index, _line in enumerate(suitable_file_lines_slice):
            if _line.startswith("["):
                break
            elif _index == len(suitable_file_lines_slice):
                break
            else:
                slice_to_remove.append(_line)
        suitable_file_lines = slice_to_remove
    actions = []
    for line in suitable_file_lines:
        if line.startswith("Action"):
            actions = line.split("=")[-1].split(";")
            actions = actions[:-1] if actions[-1] == "\n" else actions
    if len(actions) == 1 and rule_entries == 1:  # there is single configuration with single action
        # delete file
        try:
            os.remove(suitable_file)
            return True, ""
        except Exception as error:
            return False, str(error)
    if len(actions) == 1 and rule_entries > 1:  # there are multiple configuratons with suitable single action 
        # remove the slice
        try:
            if not suitable_file_lines[-1] == "\n":
                suitable_file_lines.append("\n")
            file_lines = []
            with open(suitable_file, "r") as _pkla_file:
                file_lines = _pkla_file.readlines()
            if file_lines[-1] != "\n":
                file_lines.append("\n")
            sub_st_index = 0
            sub_cnt_index = 0
            sub_fin_index = 0
            sub_l = []
            for index, line in enumerate(file_lines):
                if sub_cnt_index < len(suitable_file_lines):
                    if file_lines[index] == suitable_file_lines[sub_cnt_index]:
                        if not sub_cnt_index:
                            sub_st_index = index
                        sub_l.append(line)
                        sub_cnt_index += 1
                if sub_l == suitable_file_lines:
                    sub_fin_index = index + 1
                    break
            sliced_file_lines = file_lines[:sub_st_index] + file_lines[sub_fin_index:]
            with open(suitable_file, "w") as _pkla_file:
                _pkla_file.writelines(sliced_file_lines)
            return True, ""
        except Exception as error:
            return False, str(error)
    if len(actions) > 1: # there may be multiple configurations and suitable action is within multiple other actions
        try:
            for _action in actions:
                regex_action = re.search(_action.rstrip(), action)
                if regex_action:
                    action_index = 0
                    actions_option = []
                    for index, line in enumerate(suitable_file_lines):
                        if line.startswith("Action"):
                            action_index = index
                            actions_option = line.split("=")[-1].split(";")
                            actions_option.remove(_action)
                    suitable_file_lines[action_index] = f"Action={';'.join(actions_option)}\n"
            with open(suitable_file, "w") as _pkla_file:
                _pkla_file.writelines(suitable_file_lines)
            return True, ""
        except Exception as error:
            return False, str(error)


def name_pkla_file(priority: str, policy: str, path: str = polkit_authority_path) -> str:
    """
    Creates name for brand new .pkla file
    If priority is not met in any of dir names where files are stored, new dir will be created
    """
    listdir = os.listdir(path)
    local_authority_priority_path = None
    for _dir in listdir:
        if _dir.startswith(str(priority)):
            local_authority_priority_path = _dir
    if not local_authority_priority_path:
        # pmg lower stands for polkit manager gui
        local_authority_priority_path = f"{priority}-pmg.d"
        os.makedirs(os.path.join(path, local_authority_priority_path))
    file = ".".join(policy.split(".")[:-1])
    return f"{path}/{local_authority_priority_path}/{file}.pkla"


def create_pkla_file(name: str,
                     action: str,
                     defaults: Dict[str, Union[Dict[str, str], str]],
                     group_user_objects: List) -> List[str]:
    """
    Creates contents for new .pkla file
    """
    file_contents_list = []
    # naming config
    configuration_string = f"[{name}]\n"
    file_contents_list.append(configuration_string)
    # <Identity>
    identities = []
    for _type, _name in group_user_objects:
        if _type == 0:
            id_type = "unix-user"
        elif _type == 1:
            id_type = "unix-group"
        identities.append(f"{id_type}:{_name}")
    identity_string = f"Identity={';'.join(identities)}\n"
    file_contents_list.append(identity_string)
    # <Action>
    action_string = f"Action={action}\n"
    file_contents_list.append(action_string)
    # <Result...>
    default_any = defaults.get("allow_any")
    if default_any:
        result_any_string = f"ResultAny={default_any}\n"
        file_contents_list.append(result_any_string)
    default_inactive = defaults.get("allow_inactive")
    if default_inactive:
        result_inactive_string = f"ResultInactive={default_inactive}\n"
        file_contents_list.append(result_inactive_string)
    default_active = defaults.get("allow_active")
    if default_active:
        result_active_string = f"ResultActive={default_active}\n"
        file_contents_list.append(result_active_string)
    return file_contents_list
