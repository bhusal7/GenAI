from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from pathlib import Path

def load_single_file(file_path:str):
    """
     Load a single source code file.
    """
    loader = TextLoader(
        file_path=file_path,
        encoding='utf-8'
    )
    documents = loader.load()
    
    return documents
    
    
def load_code_directory(directory_path:str):
    
    documents = []
    
    patterns = [
        "**/*.py",
        "**/*.js",
        "**/*.ts",
        "**/*.java",
        "**/*.cpp",
        "**/*.c",
        "**/*.cs",
        "**/*.go",
        "**/*.rs",
    ]
    
    for pattern in patterns:
        loader = DirectoryLoader(
            path=directory_path,
            glob="**/*.py",
            loader_cls=TextLoader
            )
        documents = loader.load()
    
    return documents