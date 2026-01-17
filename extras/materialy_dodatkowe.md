<b> - Bold text
<strong> - Important text
<i> - Italic text
<em> - Emphasized text
<mark> - Marked text
<small> - Smaller text
<del> - Deleted text
<ins> - Inserted text
<sub> - Subscript text
<sup> - Superscript text


Hierarchia selektorów (od najmniejszego do największego priorytetu):
 1. Elementy (np. div, p) → najmniej specyficzne.
 2. Klasy (np. .example) → średni priorytet.
 3. Identyfikatory (np. #example) → wysoki priorytet.
 4. Style inline (np. style="color: red;") → najwyższy priorytet.
 5. Reguła !important (np. color: red !important;) → nadpisuje wszystko.

wagi dla arkuszy styli
Specyficzność jest obliczana na podstawie “wag”:
	•	Identyfikator (id): #id → specyficzność: 100.
	•	Klasa: .class → specyficzność: 10.
	•	Element HTML: div, p → specyficzność: 1.
Aby strona poprawnie wyświetlała się przy zmianie szerokości okna

Paleta kolorów rgb\
https://doneta.pl/blog/paleta-kolorow-rgb/