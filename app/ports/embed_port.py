class EmbedPort:
    def title(self) -> str:
        raise NotImplementedError

    def description(self) -> str:
        raise NotImplementedError

    def embed_fields(self) -> list[tuple[str, str]]:
        raise NotImplementedError
