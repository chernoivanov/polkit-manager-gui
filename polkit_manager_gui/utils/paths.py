import os


active_user = os.getlogin()

active_user_home_path = os.path.join("/home", active_user)

etc_path = os.path.join("/etc", "polkit-manager-gui")
if not os.path.exists(etc_path):
    os.mkdir(etc_path)

size_pos_settings_path = os.path.join(etc_path, "size-pos-settings.ini")

polkit_actions_path = os.path.join("/usr", "share", "polkit-1", "actions")

polkit_authority_path = os.path.join("/var", "lib", "polkit-1", "localauthority")
