"""
Main module
"""
import os, shutil, re

from textnode import (
    markdown_to_html_node
)

def copy_content(src_path, dest_path="./public"):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    if not os.path.exists(src_path):
        return

    if os.path.isfile(src_path):
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copy2(src_path, dest_path)
    else:
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        for item in os.listdir(src_path):
            src_item_path = os.path.join(src_path, item)
            dest_item_path = os.path.join(dest_path, item)
            copy_content(src_item_path, dest_item_path)

def extract_title(markdown):
    heading = re.search(r"(#{1} .*)", markdown)
    if not heading:
        raise Exception("No heading")
    return heading.group(0).lstrip('# ')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path, 'r')
    markdown = markdown_file.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    template_file = open(template_path, 'r+')
    template = template_file.read()

    content_with_title = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    complete_filename = os.path.join(dest_path, "index.html")
    html_file = open(complete_filename, "w")
    html_file.write(content_with_title)

    markdown_file.close()
    template_file.close()
    html_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dest_dir = os.path.dirname(dest_dir_path)

    if os.path.isfile(dir_path_content):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        generate_page(dir_path_content, template_path, dest_dir)
    else:
        files = os.listdir(dir_path_content)
        for file in files:
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            src_item_path = os.path.join(dir_path_content, file)
            dest_item_path = os.path.join(dest_dir_path, file)
            generate_pages_recursive(src_item_path, template_path, dest_item_path)


def main():
    """Main function"""
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
