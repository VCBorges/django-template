import uuid

from django.db import models


class CleanOnSaveMixin:
    def save(
        self,
        force_insert: bool | None = False,
        force_update: bool | None = False,
        using=None,
        update_fields: list[str] | None = None,
    ) -> None:
        self.full_clean()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    REPR_FIELDS = []

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ({", ".join([f'{field}="{getattr(self, field)}"' for field in self.REPR_FIELDS])})>'
