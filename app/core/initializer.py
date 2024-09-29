from typing import Dict
import sys
import glob
import pyarrow.parquet as pq
from os.path import dirname, basename, isfile
from dependency_injector.containers import DynamicContainer
from fastapi import FastAPI

from app.core.containers import (ContainerService)
from app import controllers
from app.core.database import engine
from app.models.conversation import Conversation
from app.services.conversation_service import conversation_service
from app.core.logger import logger


def init(app: FastAPI):
    """Load 3rd parties libs init config, After FastApi"""
    app.containers = start_containers()
    __load_conversations()

def __load_conversations():
    dataset = pq.ParquetDataset('./static/parquet/conversation/')
    table = dataset.read()
    dataFrame = table.to_pandas()
    for index, row in dataFrame.iterrows():
        conversation = conversation_service.get(_id=row['id_conversation'])
        if conversation is None:
            conversation = Conversation()
            conversation.id_conversation = row["id_conversation"]
            conversation.question = row["question"]
            conversation.answer = row["answer"]
            conversation.sequences_conversation = row["sequence_conversation"]
            conversation.id_tag = row["id_tag"]
            conversation_service.create_conversation(conversation)
            logger.info(f'Conversation created: {conversation.id_conversation}')

def columns(file_path: str, file_content_name):
    print(f"  ### {file_content_name} ###")
    parquet_file = pq.ParquetFile(file_path)
    schema = parquet_file.schema
    columnas = schema.names
    print("Columnas:", columnas)

def start_containers() -> Dict[str, DynamicContainer]:
    """
    wire the containers declared in 'containers' list with the
    controllers located in 'from app import controllers'.
    """
    containers: Dict[str, ...] = {
        "service_container": ContainerService(),
    }

    paths = glob.glob(dirname(controllers.__file__) + "/*.py")
    modules = [f"{controllers.__name__}.{basename(f)[:-3]}"
               for f in paths if isfile(f) and not f.endswith('__init__.py')]
    for container in containers.values():
        container.wire(modules=[sys.modules[m] for m in modules])
    return containers
