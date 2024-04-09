"""
Defines the TextNode class for representing text nodes.
"""
import re

from htmlnode import LeafNode, HtmlNode, ParentNode


class TextNode:
    """Represents a text node with text, type, and URL."""

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


TEXT_TYPE_TEXT = "text"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_IMAGE = "image"
TEXT_TYPE_LINK = "link"

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"

TEXT_TYPES = [TEXT_TYPE_TEXT, TEXT_TYPE_CODE, TEXT_TYPE_BOLD, TEXT_TYPE_ITALIC, TEXT_TYPE_IMAGE, TEXT_TYPE_LINK]


def text_node_to_html_node(text_node):
    """Convert a text node into a leaf node"""
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Create list of nodes from inline text"""
    new_nodes = []

    for node in old_nodes:
        if text_type not in TEXT_TYPES:
            new_nodes.append(node)
        elif node.text_type != text_type and node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(node)
        else:
            split = node.text.split(delimiter)
            new_nodes.extend(
                TextNode(text, text_type if i % 2 else TEXT_TYPE_TEXT)
                for i, text in enumerate(split)
            )
    return new_nodes

def extract_markdown_images(text):
    """Extract markdown images from a string"""
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    """Extract markdown links from a string"""
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    """Split markdown image from TextNode"""
    images = []
    new_nodes = []

    for node in old_nodes:
        if len(node.text) == 0:
            continue
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)

        last_entry = ""

        for i in range(0, len(images)):
            split_image = node.text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            if i == len(images) - 1:
                new_nodes.append(TextNode(split_image[0].replace(last_entry, ""), TEXT_TYPE_TEXT))
                new_nodes.append(TextNode(images[i][0], TEXT_TYPE_IMAGE, images[i][1]))

                if split_image[1] != "":
                    new_nodes.append(TextNode(split_image[1], TEXT_TYPE_TEXT))
            else:
                new_nodes.append(TextNode(split_image[0].replace(last_entry, ""), TEXT_TYPE_TEXT))
                new_nodes.append(TextNode(images[i][0], TEXT_TYPE_IMAGE, images[i][1]))

            last_entry = f"{split_image[0]}![{images[i][0]}]({images[i][1]})"

    return new_nodes


def split_nodes_link(old_nodes):
    """Split markdown link from TextNode"""
    links = []
    new_nodes = []

    for node in old_nodes:
        if len(node.text) == 0:
            continue
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)

        last_entry = ""

        for i in range(0, len(links)):
            split_image = node.text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if i == len(links) - 1:
                new_nodes.append(TextNode(split_image[0].replace(last_entry, ""), TEXT_TYPE_TEXT))
                new_nodes.append(TextNode(links[i][0], TEXT_TYPE_LINK, links[i][1]))

                if split_image[1] != "":
                    new_nodes.append(TextNode(split_image[1], TEXT_TYPE_TEXT))
            else:
                new_nodes.append(TextNode(split_image[0].replace(last_entry, ""), TEXT_TYPE_TEXT))
                new_nodes.append(TextNode(links[i][0], TEXT_TYPE_LINK, links[i][1]))

            last_entry = f"{split_image[0]}[{links[i][0]}]({links[i][1]})"

    return new_nodes

def text_to_textnodes(text):
    """Convert text into a list of textnodes"""
    text_node = TextNode(text, TEXT_TYPE_TEXT)
    old_nodes = split_nodes_delimiter([text_node], "**", TEXT_TYPE_BOLD)
    old_nodes = split_nodes_delimiter(old_nodes, "*", TEXT_TYPE_ITALIC)
    old_nodes = split_nodes_delimiter(old_nodes, "`", TEXT_TYPE_CODE)
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes)

    return old_nodes

def markdown_to_blocks(markdown):
    """Split markdown text into blocks, removing leading/trailing whitespace and extra newlines."""
    blocks = [block.strip() for block in markdown.strip().split("\n\n")]
    return [block for block in blocks if block]

def ordered_list_helper(text):
    ordered_list_num = 1
    res = True

    for t in text.split("\n"):
        trimmed_t = t.strip()
        regex = rf"^({ordered_list_num}\. )((.|\n)*?)(?=([\d]+\.)|($))"
        if not re.search(regex, trimmed_t):
            res = False
        
        ordered_list_num += 1

    return res

def block_to_block_type(markdown):
    if re.search(r"^(#{1,6} \w+)", markdown):
        return BLOCK_TYPE_HEADING
    if re.search(r"^(`{3})(.|\n)*\1$", markdown):
        return BLOCK_TYPE_CODE
    if re.search(r"^(>{1} \w+)", markdown):
        return BLOCK_TYPE_QUOTE
    if re.search(r"^((\*|-){1} \w+)", markdown):
        return BLOCK_TYPE_UNORDERED_LIST
    if re.search(r"^(1\. )((.|\n)*?)(?=([\d]+\.)|($))", markdown):
        if ordered_list_helper(markdown):
            return BLOCK_TYPE_ORDERED_LIST
        else:
            return BLOCK_TYPE_PARAGRAPH
    
    return BLOCK_TYPE_PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def convert_block_to_html_nodes(block):
    text_nodes = text_to_textnodes(block)

    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

def block_to_blockquote(block):
    html_nodes = convert_block_to_html_nodes(block)
    for node in html_nodes:
        if node.tag == None:
            node.value = node.value.strip(r"^(>{1} \w+)")
    return ParentNode("blockquote", html_nodes)

def block_to_unordered_list(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def block_to_ordered_list(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def block_to_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def block_to_heading(block):
    split = block.split('#')
    heading_type = len(split) - 1

    html_nodes = convert_block_to_html_nodes(block)
    for node in html_nodes:
        if node.tag == None:
            node.value = node.value.strip(r"^(#{1,6} \w+)")

    return ParentNode(f"h{heading_type}", html_nodes)

def block_to_paragraph(block):
    html_nodes = convert_block_to_html_nodes(block)

    return ParentNode("p", html_nodes, None)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    content = []

    for block in blocks:
        if block_to_block_type(block) == BLOCK_TYPE_PARAGRAPH:
            p = block_to_paragraph(block)
            content.append(p)
        if block_to_block_type(block) == BLOCK_TYPE_CODE:
            code = block_to_code(block)
            content.append(code)
        if block_to_block_type(block) == BLOCK_TYPE_QUOTE:
            blockquote = block_to_blockquote(block)
            content.append(blockquote)
        if block_to_block_type(block) == BLOCK_TYPE_HEADING:
            heading = block_to_heading(block)
            content.append(heading)
        if block_to_block_type(block) == BLOCK_TYPE_UNORDERED_LIST:
            ulist = block_to_unordered_list(block)
            content.append(ulist)
        if block_to_block_type(block) == BLOCK_TYPE_ORDERED_LIST:
            olist = block_to_ordered_list(block)
            content.append(olist)
    return ParentNode("div", content, None)

