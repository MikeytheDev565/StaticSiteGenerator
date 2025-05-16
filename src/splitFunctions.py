from textnode import TextNode, TextType
from extractlinks import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):


    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Process text nodes
        text = old_node.text
        remaining_text = text
        
        result = []
        
        # While there's text to process and we can find delimiters
        while remaining_text and delimiter in remaining_text:
            # Find opening delimiter
            start_idx = remaining_text.find(delimiter)
            
            # Add text before delimiter as TEXT
            if start_idx > 0:
                result.append(TextNode(remaining_text[:start_idx], TextType.TEXT))
            
            # Look for closing delimiter
            end_idx = remaining_text.find(delimiter, start_idx + len(delimiter))
            if end_idx == -1:
                # No matching closing delimiter
                raise Exception(f"No closing delimiter found for {delimiter}")
            
            # Extract the content between delimiters
            content = remaining_text[start_idx + len(delimiter):end_idx]
            result.append(TextNode(content, text_type))
            
            # Update remaining text
            remaining_text = remaining_text[end_idx + len(delimiter):]
        
            # Add any remaining text
        if remaining_text:
            result.append(TextNode(remaining_text, old_node.text_type))


        new_nodes.extend(result)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        text = old_node.text
        remaining_text = text
        
        extractedLinks = extract_markdown_images(remaining_text)
        
        if not extractedLinks:
            new_nodes.append(old_node)
            continue  # Skip to the next old_node
            
        while extractedLinks:
            image_alt, image_link = extractedLinks.pop(0)
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            removed_section = sections[0]
            
            # Add text before the image
            if removed_section:
                new_nodes.append(TextNode(removed_section, TextType.TEXT))
                
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_link))
            
            # Update remaining_text to be whatever follows the image
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        # Don't forget to add any remaining text after all images are processed
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        text = old_node.text
        remaining_text = text
        
        extractedLinks = extract_markdown_links(remaining_text)
        
        if not extractedLinks:
            new_nodes.append(old_node)
            continue  # Skip to the next old_node
            
        while extractedLinks:
            image_alt, image_link = extractedLinks.pop(0)
            sections = remaining_text.split(f"[{image_alt}]({image_link})", 1)
            removed_section = sections[0]
            
            # Add text before the image
            if removed_section:
                new_nodes.append(TextNode(removed_section, TextType.TEXT))
                
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.LINK, url=image_link))
            
            # Update remaining_text to be whatever follows the image
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        # Don't forget to add any remaining text after all images are processed
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    InText = text
    inTextNode = TextNode(InText, TextType.TEXT)
    nodes = [inTextNode]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_link(nodes)
    
    nodes = split_nodes_image(nodes)
    return nodes 

