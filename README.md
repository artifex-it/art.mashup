art.mashup
==========

Defines three Plone new ArcheTypes to show external web page, XML file or a web-service result query


TODO

- tests
- better documentation

## Short documentation in italian ##

Vengono definiti 3 nuovi ArcheType (per mostrare il contenuto di una pagina esterna, di un documento XML e interrogare un web-service), tutti servono per interrogare siti esterni e mostrare i risultati ottenuti all'interno del template Plone.

Il primo i tratta di una pagina con una serie di campi aggiuntivi:

- l'URL della pagina esterna (in realtà un elenco selezionabile tramite un parametro da passare alla pagina Plone)
- l'encoding della pagina esterna se deve essere fatta una conversione di codifica
- i tag HTMLviniziali della pagina esterna che contengono ciò che vuoi mostrate nella pagina Plone, possono essere più di uno
- alcune opzioni per modificare il comportamento predefinito
- un eventuale elenco di stringhe che devono essere cercate e sostituite nella pagina originale.
