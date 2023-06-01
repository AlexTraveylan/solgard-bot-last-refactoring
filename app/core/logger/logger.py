import logging


class Logger:
    _instance = None
    _handlers_set = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, name="Solgard_bot", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self._handlers_set:
            # créez un format pour les messages de logs
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            # créez un gestionnaire de fichiers qui écrit les logs dans un fichier
            file_handler = logging.FileHandler(f"app/adapters/logs/logs/{name}.log")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)

            # Créez un gestionnaire de flux qui écrit les logs dans la sortie standard (console)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(formatter)

            # Ajoutez les deux gestionnaires au logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

            self._handlers_set = True

    def get_logger(self):
        return self.logger
