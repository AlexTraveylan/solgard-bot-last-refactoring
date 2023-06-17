from abc import ABC, abstractmethod


class EmbedPort(ABC):
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    def embed_fields(self) -> list[tuple[str, str]]:
        raise NotImplementedError
