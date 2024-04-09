"""
Test the HtmlNode class.
"""
import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    """Test the HtmlNode class."""
    def test_eq(self):
        """Test the equality of two HtmlNode objects."""
        node = HtmlNode("h1", "heading1", [], {})
        node2 = HtmlNode("h1", "heading1", [], {})
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)

    def test_default(self):
        """Test the default values of the HtmlNode class."""
        node = HtmlNode("h1", "heading1")
        node2 = HtmlNode("h1", "heading1")
        self.assertEqual(node.children, None)
        self.assertEqual(node2.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node2.props, None)

    def test_not_equal(self):
        """Test the inequality of two HtmlNode objects."""
        node = HtmlNode("h2", "heading2")
        node2 = HtmlNode("h1", "heading1")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        """Test the props_to_html method."""
        node = HtmlNode("h2", "heading2", [], {"class": "header", "href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " class=\"header\" href=\"https://www.google.com\" target=\"_blank\"")

    def test_repr(self):
        """Test the __repr__ method."""
        node = HtmlNode("h2", "heading2", [], {"class": "header", "href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), f"HtmlNode(tag={node.tag}, value={node.value}, children={node.children}, props={node.props})")

    def test_leaf_node(self):
        """Test the LeafNode class."""
        node = LeafNode("h2", "heading2", {"class": "header", "href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<h2 class=\"header\" href=\"https://www.google.com\" target=\"_blank\">heading2</h2>")

    def test_leaf_node_no_tag(self):
        """Test the LeafNode class with no tag."""
        node = LeafNode(value="heading2")
        self.assertEqual(node.to_html(), "heading2")

    def test_leaf_node_no_value(self):
        """Test the LeafNode class with no value."""
        node = LeafNode("h2", None)
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_to_html(self):
        """Test the to_html method of the ParentNode class."""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node2 = ParentNode(
            "html",
            [
                LeafNode("b", "Bold text", {"class": "text-white"}),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode(
                    "body", 
                    [
                        LeafNode(None, "Normal text"),
                    ]
                ),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertEqual(node2.to_html(), "<html><b class=\"text-white\">Bold text</b>Normal text<i>italic text</i><body>Normal text</body></html>")


if __name__ == "__main__":
    unittest.main()
