from tree_sitter import Language, Parser
from git import Repo
import shutil
from pathlib import Path


def install_parser(repo_url: str, parser_name: str):
    """Install a parser from a git repo

    Example:
        install_parser("https://github.com/JoranHonig/tree-sitter-cairo.git", "tree-sitter-cairo")
    """
    here = Path(__file__).parent
    if (here / parser_name).exists():
        shutil.rmtree((here / parser_name).__str__())

    try:
        Repo.clone_from(repo_url, here / parser_name)
    except Exception as e:
        raise ValueError("Failed to clone repo", e)

    repo_path = str(here / f"{parser_name}")
    target_path = str(here / "build" / f"{parser_name}.so")

    try:
        Language.build_library(target_path, [repo_path])
    except Exception as e:
        raise ValueError("Failed to build library", e)

    shutil.rmtree((here / parser_name).__str__())


def load_language(parser_name, language):
    """Load a language that's installed

    Example:
        install_parser("https://github.com/JoranHonig/tree-sitter-cairo.git", "tree-sitter-cairo")
        load_language("tree-sitter-cairo", "cairo")
    """
    here = Path(__file__).parent
    if not (here / "build" / f"{parser_name}.so").exists():
        raise FileNotFoundError(f"Parser {parser_name} not installed")

    return Language((here / "build" / f"{parser_name}.so").__str__(), language)
