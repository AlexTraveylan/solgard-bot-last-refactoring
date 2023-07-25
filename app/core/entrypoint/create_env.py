import json
import os
from cryptography.fernet import Fernet


class CreateEnv:
    """
    A class used to encrypt configuration data and write it to an environment file.
    Use it to deploy your application without show your config.json.

    Attributes
    ----------
    config_path : str
        The file path to the configuration data.
    env_path : str
        The file path to the environment file.
    """

    def __init__(self, config_path: str) -> None:
        """
        Constructs the necessary attributes for the CreateEnv object.

        Parameters
        ----------
        config_path : str
            The file path to the configuration data.
        """
        self.config_path = config_path
        self.env_path = ".env"

    def _load_config(self) -> str:
        """
        Reads and returns the configuration data from the config file as a string.

        Returns
        -------
        str
            The configuration data as a string.
        """
        with open(self.config_path, "r") as file:
            data = json.load(file)

        data_str = json.dumps(data)

        return data_str

    def _encrypt_data(self, data_uncrypted: str) -> tuple[bytes, bytes]:
        """
        Encrypts the input string and returns the encryption key and encrypted data.

        Parameters
        ----------
        data_uncrypted : str
            The string data to encrypt.

        Returns
        -------
        tuple[bytes, bytes]
            The encryption key and encrypted data.
        """
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(data_uncrypted.encode())

        return key, cipher_text

    def _write_env(self, key: bytes, encrypted_data: bytes):
        """
        Encrypts the input string and returns the encryption key and encrypted data.

        Parameters
        ----------
        data_uncrypted : str
            The string data to encrypt.

        Returns
        -------
        tuple[bytes, bytes]
            The encryption key and encrypted data.
        """
        mode = "w"
        if os.path.exists(self.env_path):
            mode = "a"
        with open(self.env_path, mode) as env_file:
            env_file.write("PYTHONPATH=.\n")
            env_file.write("BOT_KEY=your_bot_key_here\n")
            env_file.write(f"KEY='{key.decode()}'\n")
            env_file.write(f"CONFIG_ENCRYPTED={encrypted_data.decode()}\n")

    def run(self):
        """
        Encrypts the config data and writes it to the environment file.
        """
        data_str = self._load_config()
        key, cipher_text = self._encrypt_data(data_str)
        self._write_env(key=key, encrypted_data=cipher_text)

    def decrypt(self, key: str, config_encrypted: str):
        """
        Decrypts the encrypted config data with the given key.

        Parameters
        ----------
        key : str
            The encryption key.
        config_encrypted : str
            The encrypted configuration data.

        Returns
        -------
        dict
            The decrypted configuration data.
        """
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(config_encrypted)

        data_decrypted = json.loads(plain_text.decode())

        return data_decrypted


if __name__ == "__main__":
    CreateEnv("app/core/entrypoint/connect.json").run()
