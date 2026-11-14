"""Run the complete Extract, Transform, Load workflow."""

import logging
import os

from dotenv import load_dotenv

from etl.extract import extract_posts
from etl.load import load_posts
from etl.transform import transform_posts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    api_url = os.getenv(
        "API_URL", "https://jsonplaceholder.typicode.com/posts"
    )
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "etl_demo"),
        "user": os.getenv("DB_USER", "etl_user"),
        "password": os.getenv("DB_PASSWORD", "etl_password"),
        "connect_timeout": 10,
    }

    logger.info("Starting ETL pipeline")
    raw_records = extract_posts(api_url)
    transformed_records, rejected_count = transform_posts(raw_records)
    loaded_count = load_posts(transformed_records, db_config)

    logger.info(
        "Pipeline completed: extracted=%d, loaded=%d, rejected=%d",
        len(raw_records),
        loaded_count,
        rejected_count,
    )


if __name__ == "__main__":
    main()
