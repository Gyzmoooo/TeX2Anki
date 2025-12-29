# Tex2Anki

Tex2Anki is a specialized tool designed to bridge the gap between LaTeX-based academic notes and active recall study habits. It automatically extracts mathematical environments—such as theorems, definitions, and proofs—from your .tex files and converts them into an Anki flashcard deck (.apkg).

---

## 🚀 Features

* Automatic Extraction: Scans LaTeX files for specific environments including theorem, proof, lemma, corollary, definition, and proposition.
* Targeted Processing: Only environments tagged with \label{Anki} are converted into cards, giving you full control over what gets exported.
* LaTeX Support: Wraps content in [latex] tags compatible with Anki's native rendering.
* Customizable Output: Define your deck name and output directory directly from the command line.
* Italian Localization: Automatically translates environment types for the flashcard front (e.g., "theorem" becomes "Teorema").

---

## 🛠️ Installation

### Prerequisites
* Python 3.13.7
* Conda or Pip

### Setup with Conda
Note: Before running the command, ensure you remove the 'prefix' line at the bottom of environment.yml to avoid path conflicts on different machines.

```bash
conda env create -f environment.yml
conda activate Tex2Anki
```

### Setup with Pip

```bash
pip install -r requirements.txt
```
---

## 📖 How to Use

### 1. Prepare your LaTeX file
To tell the script which parts of your notes to turn into flashcards, add \label{Anki} inside the desired environment.

Example:
```latex
\begin{theorem}[Pythagorean Theorem]
\label{Anki}
In a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides: $a^2 + b^2 = c^2$.
\end{theorem}
```

### 2. Run the script
Execute the script using the following command structure:

```bash
python main.py "Deck Name" "path/to/your/notes.tex" -f "output/folder/path"
```

### Command Line Arguments
| Argument | Description | Required |
| :--- | :--- | :--- |
| `deck` | The name of the Anki deck to be created. | Yes |
| `notes` | The file path to your `.tex` source file. | Yes |
| `-f`, `--folder` | The directory where the `.apkg` file will be saved. | No |

---

## 📦 Dependencies
The project relies on several key libraries:
* [cite_start]`genanki`: For generating the `.apkg` files[cite: 1].
* [cite_start]`pylatexenc`: For parsing and handling LaTeX nodes[cite: 1].
* [cite_start]`PyYAML`: For configuration management[cite: 1].
* [cite_start]`frozendict`: For immutable dictionary support[cite: 1].

---

## 📝 Note on Output
The script generates a deck with a unique timestamp to avoid overwriting previous exports. The resulting cards use a "Simple Model" with two fields: Question and Answer.
