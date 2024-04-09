"""
This module contains the HtmlNode class.
"""

class HtmlNode:
    """This class represents a node in the HTML tree."""
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """This method should return a string that represents the HTML of the node."""
        raise NotImplementedError()

    def props_to_html(self):
        """This method should return a string that represents the HTML attributes of the node."""
        if self.props is None:
            return ""
        res = ""
        for key, value in self.props.items():
            res += f" {key}=\"{value}\""
        return res

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HtmlNode):
    """This class represents a leaf node in the HTML tree."""
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value not provided")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HtmlNode):
    """This class represents a parent node in the HTML tree."""
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag not provided")
        if self.children is None:
            raise ValueError("Children not provided")
        res = ""

        for child in self.children:
            if child.tag is None:
                res += child.value
            else:
                res += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
        
