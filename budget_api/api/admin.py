from django.contrib import admin

from .models import Categoria, Lancamento, Origem, SubCategoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(SubCategoria)
class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "descricao")
    list_filter = ("categoria",)
    search_fields = ("nome", "categoria__nome")
    autocomplete_fields = ["categoria"]  # For easier selection in admin


@admin.register(Origem)
class OrigemAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = (
        "data_transacao",
        "get_descricao_display_admin",
        "valor",
        "tipo_transacao",
        "status_conciliacao",
        "categoria",
        "sub_categoria",
        "origem",
        "referencia_mes",
    )
    list_filter = (
        "status_conciliacao",
        "tipo_transacao",
        "categoria",
        "origem",
        "data_transacao",
        "referencia_mes",
    )
    search_fields = (
        "descricao_original",
        "descricao_editada",
        "categoria__nome",
        "sub_categoria__nome",
        "origem__nome",
    )
    readonly_fields = ("hash_transacao", "data_upload")
    autocomplete_fields = [
        "categoria",
        "sub_categoria",
        "origem",
    ]  # For easier selection

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "data_transacao",
                    "valor",
                    "descricao_original",
                    "tipo_transacao",
                )
            },
        ),
        (
            "Conciliação e Detalhes",
            {  # Changed group name for clarity
                "fields": (
                    "status_conciliacao",
                    "referencia_mes",
                    "descricao_editada",
                    "categoria",
                    "sub_categoria",
                    "origem",
                )
            },
        ),
        (
            "Metadados da Transação",
            {  # Changed group name
                "fields": ("data_upload", "hash_transacao"),
                "classes": ("collapse",),  # Collapsed by default
            },
        ),
    )

    def get_descricao_display_admin(self, obj):
        return obj.get_descricao_display()

    get_descricao_display_admin.short_description = (
        "Descrição"  # Sets column header in admin
    )
    get_descricao_display_admin.admin_order_field = (
        "descricao_editada"  # Allows sorting by this effective field
    )


# Ensure the 'api' app itself has an admin.py, even if models are in submodules,
# Django picks it up from app_label.admin.
# This file (api/admin.py) is the correct place.
