import json
import os
from cryptography.fernet import Fernet


class CreateEnv:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.env_path = ".env"

    def _load_config(self) -> str:
        with open(self.config_path, "r") as file:
            data = json.load(file)

        data_str = json.dumps(data)

        return data_str

    def _encrypt_data(self, data_uncrypted: str) -> tuple[bytes, bytes]:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(data_uncrypted.encode())

        return key, cipher_text

    def _write_env(self, key: bytes, encrypted_data: bytes):
        mode = "w"
        if os.path.exists(self.env_path):
            mode = "a"
        with open(self.env_path, mode) as env_file:
            env_file.write("PYTHONPATH=.\n")
            env_file.write("BOT_KEY=your_bot_key_here\n")
            env_file.write(f"KEY='{key.decode()}'\n")
            env_file.write(f"CONFIG_ENCRYPTED={encrypted_data.decode()}\n")

    def run(self):
        data_str = self._load_config()
        key, cipher_text = self._encrypt_data(data_str)
        self._write_env(key=key, encrypted_data=cipher_text)

    def decrypt(self, key: str, config_encrypted: str):
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(config_encrypted)

        data_decrypted = json.loads(plain_text.decode())

        return data_decrypted


if __name__ == "__main__":
    CreateEnv("app/core/entrypoint/connect.json").run()
