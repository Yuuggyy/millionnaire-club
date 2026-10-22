from django.contrib import admin

from .models import Commande, CommandeItem, AppelServeur


class ItemsInline(admin.TabularInline):
    model = CommandeItem
    extra = 0
    readonly_fields = ("nom_produit", "prix_unit", "quantite")


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "numero_table", "statut", "montant_total", "restaurant_slug", "created_at")
    list_filter = ("statut", "restaurant_slug")
    list_editable = ("statut",)
    search_fields = ("numero_table",)
    readonly_fields = ("created_at",)
    inlines = (ItemsInline,)


@admin.register(AppelServeur)
class AppelAdmin(admin.ModelAdmin):
    list_display = ("__str__", "restaurant_slug", "traite", "created_at")
    list_filter = ("traite", "restaurant_slug")
    list_editable = ("traite",)
