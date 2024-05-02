import os
from pathlib import Path
from typing import Iterator, List, Literal, Optional, Union

from langchain_core.document_loaders import BaseLoader, Blob
from langchain_core.documents import Document

from .layout_analysis_parsers import UpstageLayoutAnalysisParser

DEFAULT_PAGE_BATCH_SIZE = 10

OutputType = Literal["text", "html"]
SplitType = Literal["none", "element", "page"]


def validate_api_key(api_key: str) -> None:
    """
    Validates the provided API key.

    Args:
        api_key (str): The API key to be validated.

    Raises:
        ValueError: If the API key is empty or None.

    Returns:
        None
    """
    if not api_key:
        raise ValueError("API Key is required for Upstage Document Loader")


def validate_file_path(file_path: Union[str, Path, List[str], List[Path]]) -> None:
    """
    Validates if a file exists at the given file path.

    Args:
        file_path (Union[str, Path, List[str], List[Path]): The file path(s) to be
                                                            validated.

    Raises:
        FileNotFoundError: If the file or any of the files in the list do not exist.
    """
    if isinstance(file_path, list):
        for path in file_path:
            validate_file_path(path)
        return
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")


def get_from_param_or_env(
    key: str,
    param: Optional[str] = None,
    env_key: Optional[str] = None,
    default: Optional[str] = None,
) -> str:
    """Get a value from a param or an environment variable."""
    if param is not None:
        return param
    elif env_key and env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif default is not None:
        return default
    else:
        raise ValueError(
            f"Did not find {key}, please add an environment variable"
            f" `{env_key}` which contains it, or pass"
            f"  `{key}` as a named parameter."
        )


class UpstageLayoutAnalysisLoader(BaseLoader):
    """Upstage Layout Analysis.

    To use, you should have the environment variable `UPSTAGE_DOCUMENT_AI_API_KEY`
    set with your API key or pass it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain_upstage import UpstageLayoutAnalysis

            file_path = "/PATH/TO/YOUR/FILE.pdf"
            loader = UpstageLayoutAnalysis(
                        file_path, split="page", output_type="text"
                     )
    """

    def __init__(
        self,
        file_path: Union[str, Path, List[str], List[Path]],
        output_type: Union[OutputType, dict] = "html",
        split: SplitType = "none",
        api_key: Optional[str] = None,
        use_ocr: bool = False,
        exclude: list = ["header", "footer"],
    ):
        """
        Initializes an instance of the Upstage document loader.

        Args:
            file_path (Union[str, Path, List[str], List[Path]): The path to the document
                                                                to be loaded.
            output_type (Union[OutputType, dict], optional): The type of output to be
                                                             generated by the parser.
                                                             Defaults to "html".
            split (SplitType, optional): The type of splitting to be applied.
                                         Defaults to "none" (no splitting).
            api_key (str, optional): The API key for accessing the Upstage API.
                                     Defaults to None, in which case it will be
                                     fetched from the environment variable
                                     `UPSTAGE_DOCUMENT_AI_API_KEY`.
            use_ocr (bool, optional): Extract text from images in the document.
                                      Defaults to False. (Use text info in PDF file)
            exclude (list, optional): Exclude specific elements from
                                                     the output.
                                                     Defaults to ["header", "footer"].
        """
        self.file_path = file_path
        self.output_type = output_type
        self.split = split
        self.api_key = get_from_param_or_env(
            "UPSTAGE_DOCUMENT_AI_API_KEY", api_key, "UPSTAGE_DOCUMENT_AI_API_KEY"
        )
        self.use_ocr = use_ocr
        self.exclude = exclude

        validate_file_path(self.file_path)
        validate_api_key(self.api_key)

    def load(self) -> List[Document]:
        """
        Loads and parses the document using the UpstageLayoutAnalysisParser.

        Returns:
            A list of Document objects representing the parsed layout analysis.
        """

        if isinstance(self.file_path, list):
            result = []

            for file_path in self.file_path:
                blob = Blob.from_path(file_path)

                parser = UpstageLayoutAnalysisParser(
                    self.api_key,
                    split=self.split,
                    output_type=self.output_type,
                    use_ocr=self.use_ocr,
                    exclude=self.exclude,
                )
                result.extend(list(parser.lazy_parse(blob, is_batch=True)))

            return result

        else:
            blob = Blob.from_path(self.file_path)

            parser = UpstageLayoutAnalysisParser(
                self.api_key,
                split=self.split,
                output_type=self.output_type,
                use_ocr=self.use_ocr,
                exclude=self.exclude,
            )
            return list(parser.lazy_parse(blob, is_batch=True))

    def lazy_load(self) -> Iterator[Document]:
        """
        Lazily loads and parses the document using the UpstageLayoutAnalysisParser.

        Returns:
            An iterator of Document objects representing the parsed layout analysis.
        """

        if isinstance(self.file_path, list):
            for file_path in self.file_path:
                blob = Blob.from_path(file_path)

                parser = UpstageLayoutAnalysisParser(
                    self.api_key,
                    split=self.split,
                    output_type=self.output_type,
                    use_ocr=self.use_ocr,
                    exclude=self.exclude,
                )
                yield from parser.lazy_parse(blob, is_batch=True)
        else:
            blob = Blob.from_path(self.file_path)

            parser = UpstageLayoutAnalysisParser(
                self.api_key,
                split=self.split,
                output_type=self.output_type,
                use_ocr=self.use_ocr,
                exclude=self.exclude,
            )
            yield from parser.lazy_parse(blob)
