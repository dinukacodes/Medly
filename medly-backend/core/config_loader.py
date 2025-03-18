import yaml

def load_config():
    with open("config/api_config.yaml", "r") as f:
        api_config = yaml.safe_load(f)
    with open("config/agent_config.yaml", "r") as f:
        agent_config = yaml.safe_load(f)
    with open("config/workflow_config.yaml", "r") as f:
        workflow_config = yaml.safe_load(f)
    return {
        "api": api_config,
        "agents": agent_config,
        "workflow": workflow_config,
        "logging": api_config["logging"]  # Nested under api_config
    }