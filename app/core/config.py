import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "136.119.189.155")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "sebas")
DB_PASSWORD = os.getenv("DB_PASSWORD", "sebas2025*")
DB_NAME = os.getenv("DB_NAME", "bodega")

# Build Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Application Configuration
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
