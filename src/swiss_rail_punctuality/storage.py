import os 
from pathlib import Path 

from azure.storage.blob import ContainerClient 

ACCOUNT_URL = "https://swissrailyunus.blob.core.windows.net" 
CONTAINER = "processed" 

def _container() -> ContainerClient: 
    return ContainerClient(ACCOUNT_URL, CONTAINER, credential=os.environ["AZURE_SAS_TOKEN"])     


def exists(day: str) -> bool: 
    return _container().get_blob_client(f"{day}.parquet").exists() 


def upload(path: Path) -> None: 
    with path.open("rb") as f: 
        _container().upload_blob(path.name, f) 
        
