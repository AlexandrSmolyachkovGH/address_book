class ServiceError(Exception):
    """Base class for service-level business errors."""

    ...


class RepoError(Exception):
    """Base class for repository-level errors."""

    ...
