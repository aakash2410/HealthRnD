import os

class Config:
    """
    Configuration switches for local development vs AWS deployment.
    """
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    if ENVIRONMENT == "development":
        # Local Setup
        POSTGRES_URI = "postgresql://admin:password123@localhost:5432/healthcare_bkg"
        NEO4J_URI = "bolt://localhost:7687"
        REDIS_URI = "redis://localhost:6379/0"
        S3_ENDPOINT = "http://localhost:9000"
    else:
        # AWS Production Setup
        POSTGRES_URI = os.getenv("AWS_RDS_URI")
        NEO4J_URI = os.getenv("AWS_NEPTUNE_URI")
        REDIS_URI = os.getenv("AWS_ELASTICACHE_URI")
        S3_ENDPOINT = None  # Use default AWS endpoint

    # DPDP Compliance Settings
    DATA_RETENTION_YEARS = 1
    ENFORCE_DATA_DELETION = True
