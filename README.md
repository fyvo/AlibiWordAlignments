# AlibiWordAlignments:

This is a collection of French novels manually aligned at the sentential and
subsentential level according to the "divisive" alignment methodology documented in:

[Yong Xu and François Yvon (2016). Novel annotation schemes for sentential 
and sub-sentential alignments of bi-texts. Proceedings of 10th Language 
Resources and Evaluation Conference (LREC 2016). Portorož (Slovenia)](https://aclanthology.org/L16-1099/)

The alignment guidelines are documented in the companion file AlignmentGuidelines.pdf in the doc directory.

This resource has been produced in the course of the ALIBI Project (2016-2017)
funded by the French "Délégation Générale à la Langue Française et aux langues
de France" (DGLFLF).

## DATA SOURCES ##

This collection of datasets contain the following texts both in French and English:
* Blue Beard - La Barbe Bleue,  Les Contes de ma mère l'Oye by Charles Perrault
* Master cat - Le Chat Botté,  Les Contes de ma mère l'Oye by Charles Perrault
* The Last Lesson - La Dernière Classe, Les contes du lundi by Alphonse Daudet
* The Inn - L'Auberge, Le Horla by Guy de Maupassant
* The Vision of Charles XI - Vision de Charles XI, Colomba et autres contes et nouvelles by Prosper Mérimée 

## DATA PREPROCESSING ##

The raw texts were extracted from Wikisource. They were tokenized and segmented in
sentences using statmt tools - see http://www.statmt.org/europarl/

POS tagging and parsing were obtained using Stanford POS Tagger and Parser.
see https://nlp.stanford.edu/software/tagger.shtml
and https://nlp.stanford.edu/software/lex-parser.html for more information.

## FILE NAMING CONVENTIONS ##

### Divisive alignments 
The dat subdirectory contains divisive alignments. There are 3 files for each bi-text :
* <FrenchName>-Normalized.html:  Normalized text extracted from Wikisource
* <EnglishName>-Normalized.html: Normalized text extracted from Wikisource
* <EnglishName>_<FrenchName>.xml.ali: Alignments in "TransRead" Format. This format is documented (in French) in the companion file AlignmentFormat.pdf. It crucially enables (a) to express bilingual correspondances between HTML files; (b) to express correspondances at various levels of annotations (sentences, phrases, words, etc)

### Flat alignments
A flat word alignment is also derived for each input text, using simple rules. The corresponding files are in the [ali](./ali) subdirectory.

## LICENCE ##

The annotations and database rights of this database are licensed under a
Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

The underlying texts have been mostly collected from the wikisource
web site https://fr.wikisource.org/ (French) and https://en.wikisource.org/
For restrictions and terms of use see: 
https://en.wikisource.org/wiki/Wikisource:Copyright_policy

## CONTACT INFORMATION ##

For more information, please contact: francois (point) yvon [at] sorbonne (tiret) universite (point) fr


