from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLnode, LeafNode, ParentNode
import os, sys
import shutil
from blockToHTML import get_hash_count, markdown_to_html_node
def main():
    basepath = "/"
    
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    
    if os.path.exists("docs"):
        print(os.listdir("docs"))
    to_docs()
    print(os.listdir("docs"))
    generate_pages_recursive(basepath, "./content","template.html", "docs")


def to_docs():
    def copy_static(src_dir, dst_dir):
        # Create destination directory if it doesn't exist
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        
        # Get all items in source directory
        items = os.listdir(src_dir)
        
        for item in items:
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)
            
            # Check if item is a file or directory
            if os.path.isfile(src_path):
                # Copy the file
                shutil.copy(src_path, dst_path)
                print(f"Copied file: {src_path} to {dst_path}")
            else:
                if not os.path.exists(dst_path):
                    print(f"Creating directory before recursion: {dst_path}")
                    os.mkdir(dst_path)

                copy_static(src_path, dst_path)
    src_dir = "./static"
    if os.path.exists("./docs/"):
        shutil.rmtree("./docs/")
    os.mkdir("./docs/")
    dst_dir = "./docs/"
    copy_static(src_dir, dst_dir)

def extract_title(markdown):
    text = markdown
    lines = text.split("\n")
    title = None
    for line in lines:
        if line.startswith("#"):
            if get_hash_count(line) == 1:
                title = line.lstrip("#").strip()
                break
            else:
                raise Exception("No Title")


    return title

def generate_page(basepath, from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as f:
        markdown_file = f.read()
    with open(template_path) as f1:
        template_file = f1.read()
    
    title = extract_title(markdown_file)
    
    htmlString = markdown_to_html_node(markdown_file).to_html()
    html = template_file.replace("{{ Title }}", title).replace('{{ Content }}', htmlString)
    if 'href="/' in html:
        html = html.replace('href="/', f'href="{basepath}')
    if 'src="/' in html:
        html = html.replace('src="/', f'src="{basepath}')


    if os.path.dirname(dest_path) != "":
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_path):
            print(f"found file at {src_path}")


            generate_page(basepath, src_path,template_path, f"{dst_path[:-3]}.html")
        else:
            generate_pages_recursive(basepath, src_path,template_path, dst_path)

    







if __name__ == "__main__":
    main()
