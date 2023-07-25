from abc import ABC, abstractmethod


class EmbedPort(ABC):
    """
    An abstract base class for creating an EmbedPort. This class is designed to set an Embed object for the discord library.
    """

    @abstractmethod
    def title(self) -> str:
        """
        Abstract method that is meant to return the title of the Embed object when implemented in a subclass.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def description(self) -> str:
        """
        Abstract method that is meant to return the description of the Embed object when implemented in a subclass.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    def embed_fields(self) -> list[tuple[str, str]]:
        """
        Returns a list of tuples for the Embed object's fields. Each tuple contains a field name and value.
        By default, it returns an empty list. This method can be overridden in subclasses as needed.

        Returns:
            list[tuple[str, str]]: A list of tuples for the Embed object's fields. Each tuple contains a field name and value.
        """
        return []
