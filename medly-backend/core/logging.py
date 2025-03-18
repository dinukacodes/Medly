import logging

def setup_logging(config):
    logging.basicConfig(
        level=config["level"],
        format=config["format"],
        handlers=[logging.FileHandler(config["file"]), logging.StreamHandler()]
    )