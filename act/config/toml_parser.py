import toml


class config:
    def __init__(self, file_path, username):
        dict_toml = toml.load(open(file_path))

        self.auth_type = dict_toml["requirements"]["auth_type"]
        self.auth_param = dict_toml["requirements"]["auth_param"]
        self.target_url = dict_toml["requirements"]["target_url"]
        self.endpoint_url = dict_toml[username]["endpoint_url"]
        self.user_id = dict_toml[username]["user_id"]
        self.password = dict_toml[username]["password"]
