"""Configuration management for the Insurance Claims Agent"""
import json
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    """Get config value from env vars, Streamlit secrets, or config.json fallback."""
    # 1. Environment variable (highest priority)
    val = os.getenv(key)
    if val:
        return val
    # 2. Streamlit Cloud secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default


class Config:
    """Application configuration"""

    def __init__(self):
        # Load config.json if exists
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, "r") as f:
                self.config_data = json.load(f)
        else:
            self.config_data = {}

    # API Configuration
    @property
    def openai_api_key(self) -> str:
        return _get_secret("OPENAI_API_KEY") or self.config_data.get("API_KEY", "")

    @property
    def openai_base_url(self) -> str:
        return _get_secret("OPENAI_BASE_URL") or self.config_data.get("OPENAI_API_BASE", "https://api.openai.com/v1")

    # Model Configuration
    @property
    def model_name(self) -> str:
        return _get_secret("MODEL_NAME", "gpt-4o-mini")

    @property
    def embedding_model(self) -> str:
        return _get_secret("EMBEDDING_MODEL", "text-embedding-3-small")

    # ChromaDB Configuration
    @property
    def chroma_persist_directory(self) -> str:
        return _get_secret("CHROMA_PERSIST_DIR", "./chroma_db")

    @property
    def chroma_collection_name(self) -> str:
        return _get_secret("CHROMA_COLLECTION", "insurance_policies")

    # Data paths
    @property
    def policy_pdf_path(self) -> str:
        return _get_secret("POLICY_PDF_PATH", "./data/policy.pdf")

    @property
    def coverage_csv_path(self) -> str:
        return _get_secret("COVERAGE_CSV_PATH", "./data/coveragedata.csv")

# Global config instance
config = Config()
