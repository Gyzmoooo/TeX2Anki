import genanki
from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode, LatexMacroNode
from pylatexenc.latexnodes.parsers import LatexGeneralNodesParser
from pylatexenc.latexnodes.nodes import LatexNodeList
import argparse

parser = argparse.ArgumentParser()

#parser.add_argument("deck", help="The Anki deck's name where to insert the new flashcards")
parser.add_argument("notes", help="The path to the .tex file containing the notes")
#parser.add_argument("-f", "--folder", default="", help="The folder in which the deck will be saved")

args = parser.parse_args()

class MathBlock:
    def __init__(self, block_type, content, title=None, label=None):
        self.block_type = block_type
        self.title = title
        self.content = content
        self.label = label

    def __repr__(self):
        if self.title:
            return f"{self.block_type}(title='{self.title}', label='{self.label}')"
        return f"{self.block_type}(label='{self.label}')"

class Parser:
    def __init__(self, notes_path, env_names=["theorem","proof","lemma","corollary","remark","definition"]):
        self.notes_path = notes_path
        self.env_names = env_names
        self.blocks_list = []

    def tex_2_string(self):
        r"""
        Converts the .tex file specified in the argparse arguments to a Python string

        Returns the string containing the text in the .tex file

        """
        try:
            with open(self.notes_path, "r", encoding="utf-8") as f:
                latex_string = f.read()
            
            return latex_string

        except FileNotFoundError:
            print(f"Error: The file '{self.notes_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def blocks_creator(self, nodes):
        r"""
        Converts the string got from tex_2_string to a list of :py:class:`MathBlock` objects

        Arguments:
        
        - nodes, the return value of the :py:class:`LatexGeneralNodesParser` parser, which is expected to be a
        :py:class:`LatexNode` or :py:class:`LatexNodeList` instance

        Doesn't return anything, it only changes the value of self.blocks_list
        """
        for node in nodes:
            if node.isNodeType(LatexEnvironmentNode) and node.environmentname in self.env_names:
                
                title = None
                if node.nodeargd and node.nodeargd.argnlist:
                    first_arg = node.nodeargd.argnlist[0]
                    if first_arg is not None: title = first_arg.latex_verbatim()

                label = None
                content_nodes = []

                for child_node in node.nodelist:
                    if child_node.isNodeType(LatexMacroNode) and child_node.macroname == 'label':
                        if child_node.nodeargs:
                           label = child_node.nodeargs[0].nodelist.latex_verbatim()
                    else:
                        content_nodes.append(child_node)
                
                content = LatexNodeList(content_nodes).latex_verbatim().strip()

                block = MathBlock(
                    block_type=node.environmentname,
                    title=title,
                    content=content,
                    label=label
                )

                self.blocks_list.append(block)
            
            if hasattr(node, 'nodelist') and node.nodelist is not None:
                self.blocks_creator(node.nodelist)
        

    def parse(self):
        r"""
        The main function of the :py:class:`Parser`. Runs tex_2_string and blocks_creator

        Returns self.blocks_list
        """

        self.latex_string = self.tex_2_string()
        lw = LatexWalker(self.latex_string)
        nodelist, parsing_state = lw.parse_content(LatexGeneralNodesParser())
        self.blocks_creator(nodelist)
        
        return self.blocks_list


class FlashcardCreator:
    def __init__(self, deck_name, deck_folder, notes_parser: Parser):
        self.deck_name = deck_name
        self.deck_folder = deck_folder
        self.blocks_list = notes_parser.blocks_list

        




    

p = Parser(notes_path=args.notes)
p.parse()

fc = FlashcardCreator(9, 3, notes_parser=p)
#fc.culo()
    

'''
if __name__ == "__main__":
    p = Parser(args.deck, args.path, args.folder)
    fc = FlashcardCreator(p)'''