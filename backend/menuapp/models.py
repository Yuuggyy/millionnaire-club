from django.db import models


class Commande(models.Model):
    """Commande envoyée depuis le menu flipbook d'une table."""
    restaurant_slug = models.CharField(max_length=50, default="millionnaire")
    numero_table = models.CharField(max_length=20)
    demandes_speciales = models.TextField(blank=True, default="")
    montant_total = models.FloatField(default=0)
    statut = models.CharField(max_length=20, default="recue")  # recue / en_cours / terminee
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Table {self.numero_table} — {self.montant_total}$ ({self.created_at:%d/%m %Hh%M})"


class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, related_name="items", on_delete=models.CASCADE)
    nom_produit = models.CharField(max_length=200)
    prix_unit = models.FloatField(default=0)
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantite}x {self.nom_produit}"


class AppelServeur(models.Model):
    """Appel serveur depuis une table."""
    restaurant_slug = models.CharField(max_length=50, default="millionnaire")
    numero_table = models.CharField(max_length=20)
    traite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Table {self.numero_table} — {'traité' if self.traite else 'en attente'}"
