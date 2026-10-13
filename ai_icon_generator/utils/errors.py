"""Domain exceptions. Keep them narrow; don't subclass Exception broadly."""

from __future__ import annotations


class StudioError(Exception):
    """Base for all studio-raised errors."""


class PromptSyntaxError(StudioError):
    """The user's prompt could not be parsed."""


class PresetNotFoundError(StudioError):
    """The requested preset YAML does not exist."""


class ModelNotFoundError(StudioError):
    """The requested backend id is not in the registry."""


class ModelIntegrityError(StudioError):
    """A model file failed sha256 verification."""