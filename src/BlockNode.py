from enum import Enum

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = 'ordered_list'


def markdown_to_blocks(markdown):
    result = []
    splitMD = markdown.split("\n\n")
    for splits in splitMD:
        strippedSplit = splits.strip()
        
        if strippedSplit:

            result.append(strippedSplit)
    
    
    
    return result
    
def block_to_block_type(block):
    
    if is_heading(block):
        return BlockType.heading
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
    if is_quote_block(block):
        return BlockType.quote
    if is_ordered_list(block):
        return BlockType.ordered_list
    if is_unordered_list(block):
        return BlockType.unordered_list





    return BlockType.paragraph
def is_quote_block(block):
    lines = block.split('\n')
    return all(line.startswith('>') for line in lines)

def is_ordered_list(block):
    lines = block.split('\n')
    for i, line in enumerate(lines):
        line = line.lstrip() 
        # Check if line starts with the correct number followed by ". "
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            return False
    return True
def is_unordered_list(block):
    lines = block.split('\n')
    return all(line.startswith('- ') for line in lines)

def is_heading(block):
    if not block.startswith("#") or len(block) < 2:
        return False
    
    # Count consecutive # characters at beginning
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    
    # Check count and space requirement
    if 1 <= hash_count <= 6 and len(block) > hash_count and block[hash_count] == ' ':
        return True
    return False
