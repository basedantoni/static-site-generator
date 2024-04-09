"""
Test the Main class.
"""
import unittest

from textnode import TextNode
from htmlnode import LeafNode

from main import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type
)


class TestMain(unittest.TestCase):
    """Test the Main class."""
    def test_node_to_html_node(self):
        """Test the text_node_to_html_node function."""
        text_node = TextNode("This is a text node", "text", None)
        link_text_node = TextNode("This is a link node", "link", "https://www.boot.dev")

        self.assertEqual(text_node_to_html_node(text_node).to_html(), "This is a text node")
        self.assertEqual(type(text_node_to_html_node(text_node)), LeafNode)
        self.assertEqual(text_node_to_html_node(link_text_node).to_html(), "<a href=\"https://www.boot.dev\">This is a link node</a>")
        self.assertEqual(type(text_node_to_html_node(link_text_node)), LeafNode)

    def test_split_nodes_delimiter(self):
        """Test the split_nodes_delimiter function"""
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ]
        )

        node = TextNode("This is *text* with two *italic* words", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes, [
                TextNode("This is ", "text"),
                TextNode("text", "italic"),
                TextNode(" with two ", "text"),
                TextNode("italic", "italic"),
                TextNode(" words", "text"),
            ]
        )

    def test_extract_markdown_images(self):
        """Test the test_extract_markdown_images function"""
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])
    
    def test_extract_markdown_links(self):
        """Test the test_extract_markdown_links function"""
        text = "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_links(text), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_split_nodes_image(self):
        """Test the split_nodes_image function"""
        node = TextNode(
            "This is text with an ![image](https://storage.png) and another ![second image](https://storage.png)",
            "text",
        )
        node2 = TextNode(
            "This is text with an ![image](https://storage.png) and another ![second image](https://storage.png) and one more ![third image](https://storage.png) trailing",
            "text",
        )

        self.assertEqual(len(split_nodes_image([node])), 4)
        self.assertEqual(split_nodes_image([node]), [TextNode("This is text with an ", "text", None), TextNode("image", "image", "https://storage.png"), TextNode(" and another ", "text", None), TextNode("second image", "image", "https://storage.png")])
        self.assertEqual(len(split_nodes_image([node2])), 7)
        self.assertEqual(split_nodes_image([node2]), [TextNode("This is text with an ", "text", None), TextNode("image", "image", "https://storage.png"), TextNode(" and another ", "text", None), TextNode("second image", "image", "https://storage.png"), TextNode(" and one more ", "text", None), TextNode("third image", "image", "https://storage.png"), TextNode(" trailing", "text", None)])
    
    def test_split_nodes_link(self):
        """Test the split_nodes_link function"""
        node = TextNode(
            "This is text with an [link](https://storage.png) and another [second link](https://storage.png)",
            "text",
        )
        node2 = TextNode(
            "This is text with an [link](https://storage.png) and another [second link](https://storage.png) and one more [third link](https://storage.png) trailing",
            "text",
        )

        self.assertEqual(len(split_nodes_link([node])), 4)
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text with an ", "text", None), TextNode("link", "link", "https://storage.png"), TextNode(" and another ", "text", None), TextNode("second link", "link", "https://storage.png")])
        self.assertEqual(len(split_nodes_link([node2])), 7)
        self.assertEqual(split_nodes_link([node2]), [TextNode("This is text with an ", "text", None), TextNode("link", "link", "https://storage.png"), TextNode(" and another ", "text", None), TextNode("second link", "link", "https://storage.png"), TextNode(" and one more ", "text", None), TextNode("third link", "link", "https://storage.png"), TextNode(" trailing", "text", None)])

    def test_text_to_textnodes(self):
        """Test the text_to_textnodes function"""
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)

        for node in text_nodes:
            self.assertEqual(type(node), TextNode)
        self.assertEqual(text_nodes, [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ]
        )

    def test_markdown_to_blocks(self):
        """Test the markdown_to_blocks function"""
        markdown = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """

        self.assertEqual(len(markdown_to_blocks(markdown)), 3)

        markdown2 = """
        # This is a heading 1

        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items

        1. This is a ordered list
        2. with ordered items
        """

        self.assertEqual(len(markdown_to_blocks(markdown2)), 5)

    def test_markdown_to_empty_blocks(self):
        """Test the markdown_to_blocks function"""
        markdown = """


        """

        self.assertEqual(len(markdown_to_blocks(markdown)), 0)
        
    def test_block_to_block_type(self):
        """Test the block_to_block_type function"""
        text = """
        # Heading 1

        This is **bolded** paragraph

        - This is another paragraph with *italic* text and `code` here
        - This is the same paragraph on a new line

        1. THis is an ordered list
        2. with ordered items
        3. this is not ordered

        ```php
        codeblock
        ```

        > Here is a quote

        * This is a list
        * with items
        """
        blocks = markdown_to_blocks(text)
        block_types = []

        for block in blocks:
            block_types.append(block_to_block_type(block))

        self.assertEqual(block_types, ["heading", "paragraph", "unordered_list", "ordered_list", "code", "quote", "unordered_list"])

if __name__ == "__main__":
    unittest.main()
