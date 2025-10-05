import genanki
from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode, LatexMacroNode
from pylatexenc.latexnodes.parsers import LatexGeneralNodesParser
from pylatexenc.latexnodes.nodes import LatexNodeList
import argparse
import random
import re
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument("deck", help="The Anki deck's name where to insert the new flashcards")
parser.add_argument("notes", help="The path to the .tex file containing the notes")
parser.add_argument("-f", "--folder", default="C:\\Users\\Focus\\Desktop\\Flashcard", help="The folder in which the deck will be saved")

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

class FlashcardCreator:
    def __init__(self, deck_name, notes_path, deck_folder, env_names=["theorem","proof","lemma","corollary","definition", "proposition"]):
        self.deck_name = deck_name
        self.notes_path = notes_path
        self.deck_folder = deck_folder
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
        Converts the string got from tex_2_string to a list of :py:class:`MathBlock` objects. Runs
        recursively to check for nested nodes.

        Arguments:
        
        - nodes, the return value of the :py:class:`LatexGeneralNodesParser` parser, which is expected to be a
        :py:class:`LatexNode` or :py:class:`LatexNodeList` instance

        Doesn't return anything, it only changes the value of self.blocks_list. 
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

                if label == "Anki":
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
        Runs tex_2_string and blocks_creator in order to parse the .tex file and return a list of 
        :py:class:`MathBlock` objects.
        """
        self.latex_string = self.tex_2_string()
        lw = LatexWalker(self.latex_string)
        nodelist, parsing_state = lw.parse_content(LatexGeneralNodesParser())
        self.blocks_creator(nodelist)
        
        return self.blocks_list
    
    def format_answer(self, block: MathBlock):
        r"""
        Runs tex_2_string and blocks_creator in order to parse the .tex file and return a list of 
        :py:class:`MathBlock` objects.
        """

        answer = ''
        title = str(block.title)[1:-1]

        if block.block_type == "theorem": transl_type = "Teorema"
        if block.block_type == "lemma": transl_type = "Lemma"
        if block.block_type == "corollary": transl_type = "Corollario"
        if block.block_type == "proposition": transl_type = "Proposizione"
        if block.block_type == "proof": transl_type = "Dimostrazione"
        if block.block_type == "definition": transl_type = "Definizione"
        
        #answer = "[latex] \\textbf{" + f"{transl_type}" + "}" + f' di {title}. ' + '\\textit{' + f'{block.content}' + '} [/latex]'
        answer = '[latex]' +  f'{block.content}' + '[/latex]'
        answer = re.sub(r"\[itemsep=.*?\]", "", answer)
        answer = re.sub(r"\\coloneqq", "=", answer)

        return answer, transl_type


fc = FlashcardCreator(deck_name=args.deck, notes_path=args.notes, deck_folder=args.folder)

if __name__ == "__main__":
    fc = FlashcardCreator(deck_name=args.deck, notes_path=args.notes, deck_folder=args.folder)
    fc.parse()

    model = genanki.Model(
    random.randrange(1 << 30, 1 << 31), # Model ID
    'Simple Model', # Model Name
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Question}}', # Front format of the card
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}', # Back format of the card
        },
    ])

    now = datetime.now()
    time = now.strftime("%Y-%m-%d_%H-%M-%S")
    name = args.deck + f"_{time}"

    deck = genanki.Deck(
    random.randrange(1 << 30, 1 << 31), # Deck ID
    name) # Deck Name

    cards_data = []
    for block in fc.blocks_list:

        q = f"[latex] {fc.format_answer(block)[1]}: {block.title[1:-1]} [/latex]" if block.title != None else '[latex] Dimostrazione [/latex]'
        cards_data.append((q, fc.format_answer(block)[0]))

    for question, answer in cards_data:
        note = genanki.Note(
            model=model,
            fields=[question, answer]
        )
        deck.add_note(note)

    genanki.Package(deck).write_to_file(args.folder + f'\\{name}.apkg')

    print(f"'{name}.apkg' deck created succesfully!")
