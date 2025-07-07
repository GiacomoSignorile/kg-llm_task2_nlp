from __future__ import annotations
from typing import Any

# We will create a new dictionary to hold our Italian prompts.
PROMPTS_IT: dict[str, Any] = {}

# --- Default Settings for Italian ---
PROMPTS_IT["DEFAULT_LANGUAGE"] = "Italiano"
PROMPTS_IT["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS_IT["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS_IT["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

# --- Domain-Specific Entity Types for Italian PA Law ---
# These are the custom entity types you want to extract.
PROMPTS_IT["DEFAULT_ENTITY_TYPES"] = [
    "ENTE_PUBBLICO", "NORMA", "ARTICOLO", "OBBLIGO",
    "DIRITTO", "DATA", "SANZIONE", "PROCEDURA"
]

# --- Main Extraction Prompt (Translated and Adapted) ---
PROMPTS_IT["entity_extraction"] = """---Obiettivo---
Dato un documento di testo e una lista di tipi di entità, identifica tutte le entità di quei tipi dal testo e tutte le relazioni tra le entità identificate.
Usa {language} come lingua di output.

---Passaggi---
1. Identifica tutte le entità. Per ogni entità identificata, estrai le seguenti informazioni:
- entity_name: Nome dell'entità, usa la stessa lingua del testo di input.
- entity_type: Uno dei seguenti tipi: [{entity_types}]
- entity_description: Descrizione completa degli attributi e delle attività dell'entità.
Formatta ogni entità come ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. Dalle entità identificate nel passaggio 1, identifica tutte le coppie (entità_sorgente, entità_destinazione) che sono *chiaramente correlate* tra loro.
Per ogni coppia di entità correlate, estrai le seguenti informazioni:
- source_entity: nome dell'entità sorgente, come identificato nel passaggio 1
- target_entity: nome dell'entità destinazione, come identificato nel passaggio 1
- relationship_description: spiegazione del motivo per cui pensi che l'entità sorgente e quella destinazione siano correlate
- relationship_strength: un punteggio numerico che indica la forza della relazione tra l'entità sorgente e quella destinazione
- relationship_keywords: una o più parole chiave di alto livello che riassumono la natura della relazione, concentrandosi su concetti o temi piuttosto che su dettagli specifici.
Formatta ogni relazione come ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identifica le parole chiave di alto livello che riassumono i concetti, i temi o gli argomenti principali dell'intero testo.
Formatta le parole chiave a livello di contenuto come ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Restituisci l'output in {language} come una singola lista di tutte le entità e le relazioni identificate nei passaggi 1 e 2. Usa **{record_delimiter}** come delimitatore di record.

5. Quando hai finito, restituisci {completion_delimiter}

######################
---Esempi---
######################
{examples}

#############################
---Dati Reali---
######################
Entity_types: [{entity_types}]
Testo:
{input_text}
######################
Output:"""

# --- Few-Shot Examples (Crucial for Quality) ---
# These are new examples tailored to your Italian PA domain.
PROMPTS_IT["entity_extraction_examples"] = [
    """Esempio 1:

Entity_types: [ENTE_PUBBLICO, NORMA, PROCEDURA]
Testo:

Output:
("entity"{tuple_delimiter}"Amministrazioni Pubbliche pugliesi"{tuple_delimiter}"ENTE_PUBBLICO"{tuple_delimiter}"Le Amministrazioni Pubbliche pugliesi sono gli enti che possono utilizzare l'Albo dei Fornitori per le procedure di appalto."){record_delimiter}
("entity"{tuple_delimiter}"Albo dei Fornitori"{tuple_delimiter}"NORMA"{tuple_delimiter}"L'Albo dei Fornitori è uno strumento per l'identificazione di imprese e professionisti qualificati per la Regione Puglia."){record_delimiter}
("entity"{tuple_delimiter}"trattativa diretta"{tuple_delimiter}"PROCEDURA"{tuple_delimiter}"La trattativa diretta è una delle procedure per cui le Amministrazioni Pubbliche possono selezionare operatori economici dall'Albo."){record_delimiter}
("entity"{tuple_delimiter}"procedure negoziate"{tuple_delimiter}"PROCEDURA"{tuple_delimiter}"Le procedure negoziate sono un metodo di appalto per cui le Amministrazioni possono invitare imprese qualificate presenti nell'Albo."){record_delimiter}
("relationship"{tuple_delimiter}"Amministrazioni Pubbliche pugliesi"{tuple_delimiter}"Albo dei Fornitori"{tuple_delimiter}"Le Amministrazioni Pubbliche pugliesi utilizzano l'Albo dei Fornitori per le loro procedure di approvvigionamento."{tuple_delimiter}"utilizzo strumento, appalti pubblici"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"trattativa diretta"{tuple_delimiter}"Albo dei Fornitori"{tuple_delimiter}"L'Albo dei Fornitori è una fonte per selezionare operatori per una trattativa diretta."{tuple_delimiter}"selezione operatori, procedura appalto"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"appalti pubblici, albo fornitori, procedure amministrative, puglia"){completion_delimiter}
#############################""",
    """Esempio 2:

Entity_types: [NORMA, SANZIONE, ENTE_PUBBLICO]
Testo:

Output:
("entity"{tuple_delimiter}"Albo dei Fornitori"{tuple_delimiter}"NORMA"{tuple_delimiter}"L'Albo dei Fornitori è un elenco di soggetti qualificati per la Regione Puglia."){record_delimiter}
("entity"{tuple_delimiter}"Pubblica Amministrazione"{tuple_delimiter}"ENTE_PUBBLICO"{tuple_delimiter}"La Pubblica Amministrazione è l'ente con cui i fornitori devono essere in grado di negoziare per essere iscritti all'Albo."){record_delimiter}
("entity"{tuple_delimiter}"sospensione dall'Albo"{tuple_delimiter}"SANZIONE"{tuple_delimiter}"La sospensione è una sanzione applicabile a un fornitore dall'organo di gestione dell'Albo."){record_delimiter}
("entity"{tuple_delimiter}"cancellazione dall'Albo"{tuple_delimiter}"SANZIONE"{tuple_delimiter}"La cancellazione è una sanzione definitiva che rimuove un fornitore dall'Albo."){record_delimiter}
("relationship"{tuple_delimiter}"Albo dei Fornitori"{tuple_delimiter}"Pubblica Amministrazione"{tuple_delimiter}"L'iscrizione all'Albo richiede la capacità di negoziare con la Pubblica Amministrazione."{tuple_delimiter}"requisito iscrizione, capacità negoziale"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"sospensione dall'Albo"{tuple_delimiter}"Albo dei Fornitori"{tuple_delimiter}"La sospensione è una sanzione che riguarda direttamente l'iscrizione all'Albo dei Fornitori."{tuple_delimiter}"sanzione, gestione albo"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"sanzioni, albo fornitori, requisiti, pubblica amministrazione"){completion_delimiter}
#############################"""
]

# You can translate other prompts like 'summarize_entity_descriptions' if you use them,
# but the extraction prompt is the most important one to start with.