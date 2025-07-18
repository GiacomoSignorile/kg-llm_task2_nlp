import asyncio
import os
import inspect
import logging
import logging.config
from prompt_it import PROMPTS_IT
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc, logger, set_verbose_debug
from lightrag.kg.shared_storage import initialize_pipeline_status

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=False)

WORKING_DIR = "./output_lightrag"
os.environ["NEO4J_URI"] = "neo4j://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "giacomo3234" 

def configure_logging():
    """Configure logging for the application"""

    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "lightrag"]:
        logger_instance = logging.getLogger(logger_name)
        logger_instance.handlers = []
        logger_instance.filters = []

    log_dir = os.getenv("LOG_DIR", os.getcwd())
    log_file_path = os.path.abspath(os.path.join(log_dir, "lightrag_ollama_demo.log"))

    print(f"\nLightRAG compatible demo log file: {log_file_path}\n")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    log_max_bytes = int(os.getenv("LOG_MAX_BYTES", 10485760)) 
    log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", 5)) 

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(levelname)s: %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "file": {
                    "formatter": "detailed",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "maxBytes": log_max_bytes,
                    "backupCount": log_backup_count,
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "lightrag": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )

    logger.setLevel(logging.INFO)

    set_verbose_debug(os.getenv("VERBOSE_DEBUG", "false").lower() == "true")


if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    rag = None  
    try:
        rag = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=ollama_model_complete,
            llm_model_name=os.getenv("LLM_MODEL", "llama3.2:3b"),
            llm_model_max_token_size=8192,
            llm_model_kwargs={
                "host": os.getenv("LLM_BINDING_HOST", "http://localhost:11434"),
                "options": {"num_ctx": 8192},
                "timeout": int(os.getenv("TIMEOUT", "300")),
            },
            embedding_func=EmbeddingFunc(
                embedding_dim=int(os.getenv("EMBEDDING_DIM", "768")),
                max_token_size=int(os.getenv("MAX_EMBED_TOKENS", "8192")),
                func=lambda texts: ollama_embed(
                    texts,
                    embed_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest"),
                    host=os.getenv("EMBEDDING_BINDING_HOST", "http://localhost:11434"),
                ),
            ),
            #graph_storage="Neo4JStorage",
            addon_params={
                "language": PROMPTS_IT["DEFAULT_LANGUAGE"],
                "entity_types": PROMPTS_IT["DEFAULT_ENTITY_TYPES"],
                "entity_extraction_prompt": PROMPTS_IT["entity_extraction"],
                "entity_extraction_examples": PROMPTS_IT["entity_extraction_examples"],
            }
        )

        await rag.initialize_storages()
        await initialize_pipeline_status()

        return rag

    except Exception as ex:
        print(f"An error occurred during RAG initialization: {ex}")
        raise


async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)


async def main():
    try:
        # Clear old data files
        files_to_delete = [
            "graph_chunk_entity_relation.graphml",
            "kv_store_doc_status.json",
            "kv_store_full_docs.json",
            "kv_store_text_chunks.json",
            "vdb_chunks.json",
            "vdb_entities.json",
            "vdb_relationships.json",
        ]

        for file in files_to_delete:
            file_path = os.path.join(WORKING_DIR, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleting old file:: {file_path}")

        rag = await initialize_rag()

        test_text = ["This is a test string for embedding."]
        embedding = await rag.embedding_func(test_text)
        embedding_dim = embedding.shape[1]
        print("\n=======================")
        print("Test embedding function")
        print("========================")
        print(f"Test dict: {test_text}")
        print(f"Detected embedding dimension: {embedding_dim}\n\n")

        with open("./extracted_txt/combined_output.txt", "r", encoding="utf-8") as f:
            await rag.ainsert(f.read())

        print("\n=====================")
        print("Query mode: naive")
        print("=====================")
        resp = await rag.aquery(
            "What are the top themes in this story?",
            param=QueryParam(mode="naive", stream=True),
        )
        if inspect.isasyncgen(resp):
            await print_stream(resp)
        else:
            print(resp)

        # # Perform local search
        # print("\n=====================")
        # print("Query mode: local")
        # print("=====================")
        # resp = await rag.aquery(
        #     "What are the top themes in this story?",
        #     param=QueryParam(mode="local", stream=True),
        # )
        # if inspect.isasyncgen(resp):
        #     await print_stream(resp)
        # else:
        #     print(resp)

        # # Perform global search
        # print("\n=====================")
        # print("Query mode: global")
        # print("=====================")
        # resp = await rag.aquery(
        #     "What are the top themes in this story?",
        #     param=QueryParam(mode="global", stream=True),
        # )
        # if inspect.isasyncgen(resp):
        #     await print_stream(resp)
        # else:
        #     print(resp)

        # # Perform hybrid search
        # print("\n=====================")
        # print("Query mode: hybrid")
        # print("=====================")
        # resp = await rag.aquery(
        #     "What are the top themes in this story?",
        #     param=QueryParam(mode="hybrid", stream=True),
        # )
        if inspect.isasyncgen(resp):
            await print_stream(resp)
        else:
            print(resp)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if rag:
            await rag.llm_response_cache.index_done_callback()
            await rag.finalize_storages()


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
    print("\nDone!")
