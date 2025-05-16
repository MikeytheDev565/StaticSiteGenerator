from BlockNode import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import *
from splitFunctions import text_to_textnodes
from textnode import TextNode, TextType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    HTMLnode_list = []
    for block in blocks:
        blockType = block_to_block_type(block)
        

        if blockType == BlockType.heading:
            hash_count = get_hash_count(block)
            content = block[hash_count:].strip()
            children = text_to_children(content)
            
            HTMLnode_list.append(ParentNode(f"h{hash_count}", children))
            continue
        if blockType == BlockType.code:
            # Extract content between ``` delimiters
            # Strip the ``` from beginning and end of the block
            # Some blocks might start with ```\n and end with \n```
            content = block.strip()
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            if not content.endswith("\n"):
                content += "\n"

            
            # Create a TextNode with the raw content (no markdown parsing)
            code_text_node = TextNode(content, TextType.TEXT)
            # Convert to HTMLNode
            code_html_node = text_node_to_html_node(code_text_node)
            # Wrap in a pre tag
            pre_node = ParentNode("pre", [ParentNode("code", [code_html_node])])
            HTMLnode_list.append(pre_node)
            continue
        if blockType == BlockType.quote:
            # Remove the > prefix from each line
            lines = block.split("\n")
            content = " ".join([line[1:].strip() if line.startswith(">") else line.strip() for line in lines])
            
            # Process inline markdown in the quote content
            children = text_to_children(content)
            
            # Create blockquote node
            quote_node = ParentNode("blockquote", children)
            HTMLnode_list.append(quote_node)
            continue
        if blockType in [BlockType.ordered_list, BlockType.unordered_list]:
            tag = "ol" if blockType == BlockType.ordered_list else "ul"
            
            # Split into list items
            list_items = block.strip().split("\n")
            li_nodes = []
            
            for item in list_items:
                # Remove the list marker and trim
                if blockType == BlockType.unordered_list:
                    # For unordered lists (- item)
                    if item.startswith("- "):
                        content = item[2:].strip()
                    else:
                        content = item.strip()
                else:  
                    # For ordered lists (1. item)
                    parts = item.split(". ", 1)
                    if len(parts) > 1 and parts[0].isdigit():
                        content = parts[1].strip()
                    else:
                        content = item.strip()
                
                # Process inline markdown in the list item
                children = text_to_children(content)
                
                # Create list item node
                li_node = ParentNode("li", children)
                li_nodes.append(li_node)
            
            # Create the list container node (ol or ul)
            list_node = ParentNode(tag, li_nodes)
            HTMLnode_list.append(list_node)
            continue
        if blockType == BlockType.paragraph:
            text = " ".join(block.strip().split("\n"))
            children = text_to_children(text)
            HTMLnode_list.append(ParentNode(f"p", children))
            continue
            
        

    return ParentNode("div", HTMLnode_list)



    
def get_hash_count(block):
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    return hash_count

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for textnode in text_nodes:
        children.append(text_node_to_html_node(textnode))
    return children