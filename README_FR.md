# Corpus ALIBI - Alignements de textes bilingues #

Ce corpus contient un ensemble de nouvelles initialement écrites en français
et alignées manuellement au niveau des phrases et des segments de phrases
selon le protocole d'annotation divisif documenté dans:

[Yong Xu and François Yvon (2016). Novel annotation schemes for sentential 
and sub-sentential alignments of bi-texts. Proceedings of 10th Language 
Resources and Evaluation Conference (LREC 2016). Portorož (Slovenia).]((https://aclanthology.org/L16-1099/))

Les consignes d'alignement sont documentées en anglais dans le fichier
AlignmentGuidelines.pdf joint à cette distribution.

Cette ressource a été produite dans le cadre du projet ALIBI financé par
la Délégation Générale à la Langue Française et aux langues de France du
Ministère de la Culture.

## SOURCES DE DONNEES ##

Cette collection de textes comprend les nouvelles suivantes en français et en
anglais:
* Blue Beard - La Barbe Bleue,  Les Contes de ma mère l'Oye par  Charles Perrault
* Master cat - Le Chat Botté,  Les Contes de ma mère l'Oye par Charles Perrault
* The Last Lesson - La Dernière Classe, Les contes du lundi par Alphonse Daudet
* The Inn - L'Auberge, Le Horla by Guy de Maupassant
* The Vision of Charles XI - Vision de Charles XI, Colomba et autres contes et
   nouvelles par Prosper Mérimée 

## PRETRAITEMENTS DES DONNEES ##

Les textes bruts ont été collectés sur Wikisource. Ils ont été subséquemment tokenisés
et segmentés au niveau de la phrase en utilisant les outils "Europarl".
Voir see http://www.statmt.org/europarl/

Les annotations morphosyntaxiques et syntaxiques ont été calculées automatiquement par
les outils Stanford POS Tagger et Stanford Parser.
voir https://nlp.stanford.edu/software/tagger.shtml
voir https://nlp.stanford.edu/software/lex-parser.html pour de plus amples informations.

## CONVENTIONS DE NOMMAGE DES FICHIERS ##

Il y a 3 fichiers pour chaque bitexte:
* <NomFrancais>-Normalized.html		Texte normalisé extrait de wikisource
* <NomAnglais>-Normalized.html 	   	Texte normalisé extrait de wikisource
* <NomAnglais>_<NomFrancais>.xml.ali 	Alignements au format "Transread". Ce format est documenté dans le fichier AlignmentFormat.pdf joint à cette distributino. Ce format    permet (a) d'exprimer des correspondances bilingues entre fichiers HTML; (b) d'exprimer des correspondances à plusieurs niveaux d'annotations.

## LICENCE ##

Les annotations et les alignements sont distribués sous la licence internationale
Creative Commons Attribution-ShareAlike 4.0.

Une copie de cette licence est jointe à cette ressource. Voir également
<http://creativecommons.org/licenses/by-sa/4.0/>.

Les textes sous jacents ont été collectés depuis le site Wikisource
https://fr.wikisource.org/ (French) and https://en.wikisource.org/
Les restrictions suivantes s'appliquent à ces textes:
https://fr.wikisource.org/wiki/Aide:Droit_d’auteur

## CONTACT ##

Pour plus d'information, contacter francois (point) yvon [ at] limsi (point) fr
