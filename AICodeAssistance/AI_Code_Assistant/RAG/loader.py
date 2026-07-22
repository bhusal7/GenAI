from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader


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
    """
    Load code files from a directory.
    """
    
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
            glob=pattern,
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            silent_errors=True
            )
        documents = loader.load()
    
    return documents