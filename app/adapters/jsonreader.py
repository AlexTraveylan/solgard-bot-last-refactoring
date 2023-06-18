import json
from os import PathLike
from cryptography.fernet import Fernet


def read_json(filePath: PathLike) -> dict[str, any]:
    with open(filePath) as file:
        data = json.load(file)
    return data


# # Générer une clé de cryptage
# key = Fernet.generate_key()

# # Enregistrer cette clé dans un fichier (à ne pas partager publiquement)
# with open("app/core/entrypoint/key.key", "wb") as key_file:
#     key_file.write(key)

# # Charger les données à partir du fichier JSON
# with open("app/core/entrypoint/connect.json", "r") as file:
#     data = json.load(file)

# data_str = json.dumps(data)

# cipher_suite = Fernet(key)
# cipher_text = cipher_suite.encrypt(data_str.encode())

# with open("app/core/entrypoint/config_encrypted.bin", "wb") as file_encrypted:
#     file_encrypted.write(cipher_text)

# # decrypter

# with open("app/core/entrypoint/key.key", "rb") as key_file:
#     key = key_file.read()

# # Charger les données cryptées
# with open("app/core/entrypoint/config_encrypted.bin", "rb") as file_encrypted:
#     cipher_text = file_encrypted.read()

# cipher_suite = Fernet(key)
# plain_text = cipher_suite.decrypt(cipher_text)

# data_decrypted = json.loads(plain_text.decode())

# print(data_decrypted)
