from textnode import TextType

class HTMLnode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        returningString = ""
        for each in self.props:
            returningString += f' {each}="{self.props[each]}"'
        
        return returningString





    def __repr__(self):
        return f"HtmlNOde({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLnode):
    def __init__(self,value,tag=None, props=None ):
        super().__init__(value=value,tag=tag,props=props)
    def to_html(self):
        if self.value== None:
            raise ValueError()
        if self.tag == None:
            return self.value
        if self.tag == "img":
            return f"<img {self.props_to_html()}/>"
        if self.tag == "a":
            return f'<a{self.props_to_html()}>{self.value}</a>'
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLnode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("NO Tag needs to have a tag!!!")
        if self.children == None:
            raise ValueError("No CHILDREN! NEEDS CHIDLREN!!!!")
       # Start with opening tag
        html = f"<{self.tag}>"
        
        # Add all children's HTML
        for child in self.children:
            html += child.to_html()
            
        # Add closing tag
        html += f"</{self.tag}>"



        return html

def text_node_to_html_node(text_node):

    if text_node.text_type == TextType.TEXT:
        return LeafNode(text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(text_node.text, tag="b")
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(text_node.text, tag="i")
    if text_node.text_type == TextType.CODE:
        return LeafNode(text_node.text, tag="code")
    if text_node.text_type == TextType.LINK:
        return LeafNode(text_node.text, tag="a",props={"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode( " ",tag="img", props={"src":text_node.url, "alt":text_node.text})



