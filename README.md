# 📊 LLM\_marketing

Questo progetto esplora l’utilizzo di modelli linguistici di grandi dimensioni (LLM) per l’analisi di un questionario reale somministrato in Malesia da Starbucks. L'obiettivo è confrontare le risposte generate da due LLM (Gemma e Llama) con quelle reali, applicando tecniche di inferenza e bootstrapping.

## 📁 Struttura del progetto

### `inferenza/`

Contiene tutto il necessario per eseguire l’inferenza dei modelli LLM.

#### Sottocartelle e file principali:

* `dataset/survey.csv`: contiene il questionario Starbucks Malesia.
* `bin/inference.py`: **codice principale** per avviare l’esperimento.
* `engine.py`: implementazione della metodologia **bootstrapping**.
* `prompts.py`: prompt in linguaggio Python utilizzati durante l’inferenza.
* `experiments/`: contiene due sottocartelle, una per ciascun modello LLM:

  * `Gemma/`
  * `Llama/`
    All’interno sono presenti:
  * Codici eseguiti per la generazione.
  * Risultati ottenuti, ovvero:

    * `meta_lama_3_3_70b_instruct_answers.csv`
    * `google_gemma_3_27b_it_answers.csv`

⚠️ **Nota**: Per eseguire l’esperimento è necessario:

* Impostare una chiave di autenticazione per il provider **Novita**, **oppure**
* Modificare `engine.py` per usare un altro provider compatibile.

### `analisi_dati/`

Contiene le analisi statistiche basate sulle risposte fornite dagli LLM e dai dati reali.

#### Esperimenti:

* `esperimento_1/`
* `esperimento_2/`
* `esperimento_3/`

Ogni cartella include:

* `prompt_X.md`: descrizione del prompt in linguaggio naturale.
* `prompts_X.py`: prompt in linguaggio Python.
* `survey_adattata_numericamente.csv`: versione modificata del questionario per confronto (categorie "Altro" rare rimosse).
* Risposte dei modelli (`*_answers.csv`).
* Notebook per analisi:

  * `grafici_distribuzioni.ipynb`: analisi della distribuzione delle singole variabili.
  * `grafici_correlazione_reali.ipynb`: associazione nel dataset reale.
  * `grafici_correlazione_gemma.ipynb`: associazione secondo Gemma.
  * `grafici_correlazione_llama.ipynb`: associazione secondo Llama.
* Grafici salvati:

  * `confronto_plot.pdf`: distribuzioni variabili.
  * `associazione_reale.pdf`, `associazione_llama_X.pdf`, `associazione_gemma_X.pdf`: analisi di correlazione.

## 🚀 Come eseguire l'esperimento

1. Configura l’ambiente Python con i pacchetti necessari.
2. Inserisci la chiave API del provider **Novita** (o modifica `engine.py` per usare un altro API).
3. Esegui lo script `inferenza/bin/inference.py` con le opzioni necessarie per generare le risposte.
4. Analizza i risultati con i notebook nella cartella `analisi_dati/`.
