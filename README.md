# KG+LLM Task 2: Empulia PA Regulation Analysis

This repository contains a comprehensive Knowledge Graph + Large Language Model (KG+LLM) system for analyzing EmPULIA Public Administration (PA) regulations documents. The project uses LightRAG for knowledge graph extraction and retrieval-augmented generation to process and query documents in Italian.

## 🎯 Main Component

**`langchain_graphrag.ipynb`** - The principal notebook containing the complete implementation of the KG+LLM system for Italian PA law analysis.

## 📁 Project Structure

```
├── langchain_graphrag.ipynb          # Main implementation notebook
├── test_notebooks/                   # Test and experimental notebooks
│   ├── lightrag_lmstudio.ipynb      # LMStudio integration tests
│   ├── KG_Gen.ipynb                 # Knowledge Graph generation tests
│   ├── graphrag_microsoft.ipynb     # Microsoft GraphRAG tests
│   ├── litegraphrag.ipynb           # LightGraphRAG experiments
│   └── Rag_baseline.ipynb           # Baseline RAG implementation
├── test_scripts/
│   ├── ollama_lightrag_test.py      # Ollama LightRAG integration test
│   └── prompt_it.py                 # Italian language prompt
├── data/
│   ├── 2023_0036_Codice_Contratti_Relazione.pdf  # PA regulations document
│   ├── extracted_txt/               # Extracted text files
│   └── evaluation_datasets/         # RAG evaluation datasets
├── databases/                       # Database storage
├── docs/                           # Documentation
└── output_lightrag/                # LightRAG output files
```

## 🚀 Quick Start

### Prerequisites

1. **Python Environment**: Create a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Neo4j Database**: Ensure Neo4j is running locally
   - URI: `neo4j://localhost:7687`
   - Username: `neo4j`
   - Password: `password`

4. **Ollama Setup**: Install and run Ollama for local LLM inference
   ```bash
   # Install Ollama (follow instructions at https://ollama.ai)
   ollama pull gemma3:4b
   ollama pull nomic-embed-text:latest
   ```

### Running the Main Notebook

1. Start Jupyter Lab:
   ```bash
   jupyter lab
   ```

2. Open `langchain_graphrag.ipynb` and run the cells sequentially.

## 🔧 Core Features

### Knowledge Graph Extraction
- **Entity Recognition**: Extracts Italian PA-specific entities (ENTE_PUBBLICO, NORMA, ARTICOLO, OBBLIGO, etc.)
- **Relationship Mapping**: Identifies relationships between legal entities
- **Graph Storage**: Uses Neo4j for persistent knowledge graph storage

### Retrieval-Augmented Generation (RAG)
- **Multiple Query Modes**: 
  - `Graph`: graph based retrieval
  - `Vector`: Vector based retrieval
  - `Hybrid`: Hybrid  vector-graph based retrieval
- **Italian Language Support**: Custom prompts and entity types for Italian PA law
- **Streaming Responses**: Real-time response generation

### Evaluation Framework
- **RAGAS Evaluation**: Comprehensive evaluation of RAG performance
- **Multiple Datasets**: Various evaluation datasets for different RAG approaches
- **Performance Metrics**: Detailed analysis of retrieval and generation quality

## 📊 Test Components

The following files are test implementations and experiments:

- **`lightrag_lmstudio.ipynb`**: Tests LightRAG with LMStudio
- **`KG_Gen.ipynb`**: Knowledge Graph generation experiments
- **`graphrag_microsoft.ipynb`**: Microsoft GraphRAG implementation tests
- **`litegraphrag.ipynb`**: LightGraphRAG framework experiments
- **`Rag_baseline.ipynb`**: Baseline RAG implementation for comparison
- **`ollama_lightrag_test.py`**: Ollama integration test script

## 🛠️ Configuration

### Environment Variables
Create a `.env` file with the following variables:
```env
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
LLM_MODEL=gemma3:4b
EMBEDDING_MODEL=nomic-embed-text:latest
LLM_BINDING_HOST=http://localhost:11434
EMBEDDING_BINDING_HOST=http://localhost:11434
TIMEOUT=300
EMBEDDING_DIM=768
MAX_EMBED_TOKENS=8192
VERBOSE_DEBUG=false
```

### Italian Language Support
The system includes custom Italian prompts for PA regulation analysis:
- **Entity Types**: ENTE_PUBBLICO, NORMA, ARTICOLO, OBBLIGO, DIRITTO, DATA, SANZIONE, PROCEDURA
- **Custom Prompts**: Tailored for Italian legal document analysis
- **Domain-Specific**: Optimized for Public Administration terminology

## 📈 Evaluation Results

The repository includes comprehensive evaluation datasets:
- `base_rag_evaluation_dataset.csv`: Baseline RAG performance
- `hybrid_graphrag_evaluation_dataset.csv`: Hybrid GraphRAG results
- `graphrag_evaluation_dataset.csv`: GraphRAG specific evaluations
- Various RAGAS evaluation result files

## 🔍 Key Technologies

- **LightRAG**: Knowledge graph extraction and RAG framework
- **Neo4j**: Graph database for knowledge storage
- **Ollama**: Local LLM inference
- **LMStudio**: Local LLM inference
- **LangChain**: LLM orchestration
- **Pandas**: Data manipulation and analysis
- **Jupyter**: Interactive development environment



## 📄 License

This project is for research and educational purposes. 
