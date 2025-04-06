import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict, Optional, Union


class XMLParser():
    def __init__(self, file: str) -> None:
        self.file = file
        self.element_tree, self.root_node = self._get_et_and_root()

    def _get_et_and_root(self) -> Tuple[Optional[ET.ElementTree], Optional[ET.Element]]:
        """
        Parses file to get Element Tree and its' root element
        Returns [Tuple] consisting of [Optional[ET.ElementTree]] and [Optional[ET.Element]]
        """
        try:
            element_tree = ET.parse(self.file)
            root_node = element_tree.getroot()
        except ET.ParseError() as err:
            pass  # handle error
            return None, None
        return element_tree, root_node
    
    def parse_policy_file(self) -> Tuple[Optional[List[ET.Element]], Optional[str]]:
        """
        Iterates through root node (if found)
        Returns [Tuple] consisting of [Optional[List]] of <action> and [Optional[str]] with <vendor>'s tag text
        """
        actions, vendor = [], None
        if self.root_node:
            for child_node in self.root_node.iter():
                if child_node.tag == "action":
                    actions.append(child_node)
                elif child_node.tag == "vendor":
                    vendor = child_node.text
        return actions, vendor
    
    def parse_action_element(self, action: ET.Element) -> Tuple[Dict[str, Union[Dict[str, str], str]], str]:
        """
        Parses all found <action> elements for its' attributes (<defaults>, <description> and <message>)
        Returns [Tuple] consisting of [Dict] with <action>'s attributes and [str] with <action>'s id
        """
        defaults = {}
        description, message = None, None
        action_child_elements = list(action)
        for child_element in action_child_elements:
            child_attribute_dict = child_element.attrib.items()
            if child_element.tag == "description" and not child_attribute_dict:
                description = child_element.text
            if child_element.tag == "message" and not child_attribute_dict:
                message = child_element.text
            if child_element.tag == "defaults":
                defaults_child_elements = list(child_element)
                for defaults_child_element in defaults_child_elements:
                    defaults[defaults_child_element.tag] = defaults_child_element.text
        action_dict = {"defaults": defaults,
                       "description": description,
                       "message": message}
        return action_dict, action.attrib.get("id")
    
    def modify_defaults_elements(self,
                                 action_id: str,
                                 defaults: Dict[str, Union[Dict[str, str], str]]) -> Tuple[bool, Optional[str]]:
        """
        Modifies some <action>'s <defaults> elements (based on provided action's id)
        Returns Tuple[bool, Optional[str]]
        """
        # needed to handle failure
        if self.root_node:
            try:
                for child_node in self.root_node.iter():
                    if child_node.tag == "action" and child_node.attrib.get("id") == action_id:
                        for action_node in list(child_node):
                            if action_node.tag == "defaults":
                                for default in list(action_node):
                                    default.text = defaults[default.tag]
            except Exception as err:
                return False, str(err)
        self.element_tree.write(self.file)
        return True, None
