import json
import os

class UserConfigHandler:
    def __init__(self):
        self.config_path = "data/user_config.json"
        self._load()
        self.config_schema = {
            "config_id": 0,
            "period": "9mo",
            "interval": "1d",
            "volume": True,
            "rsi": False,
            "macd": False,
            "sma_periods": None
        }

    def _load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def _check(self, user_id):
        if str(user_id) not in self.data:
            self.data[str(user_id)] = [self.config_schema]
            self._save()

    def get_configs(self, user_id, config_id=None):
        self._check(user_id)
        if config_id is not None:
            for c in self.data[str(user_id)]:
                if c["config_id"] == config_id:
                    return c
        return self.data[str(user_id)]

    def add_config(self, user_id, config, config_id=1):
        self.config_schema = {
            "config_id": 0,
            "period": "9mo",
            "interval": "1d",
            "volume": True,
            "rsi": False,
            "macd": False,
            "sma_periods": None
        }
        user_id = str(user_id)
        configs = self.get_configs(user_id)

        if len(configs) >= 4:
            raise ValueError("Maximum of 4 configs (1 default + 3 custom) reached.")

        config_id = max(c["config_id"] for c in configs) + 1
        config["config_id"] = config_id
        for n in config.keys():
            self.config_schema[n] = config[n]
        configs.append(self.config_schema)
        self.data[user_id] = configs
        self._save()

    def update_config(self, user_id, config_id, new_values):
        user_id = str(user_id)
        configs = self.get_configs(user_id)

        for c in configs:
            if c["config_id"] == config_id:
                c.update(new_values)
                self._save()
                return True
        raise ValueError("Config ID not found.")

    def delete_config(self, user_id, config_id):
        if config_id == 0:
            raise ValueError("Cannot delete default config.")
        user_id = str(user_id)
        configs = self.get_configs(user_id)
        self.data[user_id] = [c for c in configs if c["config_id"] != config_id]
        self._save()
