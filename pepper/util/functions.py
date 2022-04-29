import os
import structlog

logger = structlog.get_logger(__name__)


def create_new_site(site_dir: str) -> None:
    directories = ["content", "static", "templates"]
    # files = ["__init__.py"]

    if not os.path.exists(site_dir):
        os.makedirs(site_dir)

    for directory in directories:
        target_path = os.path.join(site_dir, directory)
        os.makedirs(target_path)
        logger.info("Directory created", target_path=target_path)
