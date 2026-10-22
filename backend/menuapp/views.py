import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Commande, CommandeItem, AppelServeur


@csrf_exempt
def api_submit_order(request):
    """Contrat flipbook : POST {restaurant_slug, table_number, items:[{name,price,quantity}], special_notes}
    -> {success: true, total: <float>} ou {success: false, error: "..."}
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"})
    try:
        b = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON invalide"})

    table = str(b.get("table_number") or "").strip()
    items = b.get("items") or []
    if not table:
        return JsonResponse({"success": False, "error": "Numéro de table requis"})
    if not items:
        return JsonResponse({"success": False, "error": "Panier vide"})

    cmd = Commande.objects.create(
        restaurant_slug=str(b.get("restaurant_slug") or "millionnaire"),
        numero_table=table,
        demandes_speciales=str(b.get("special_notes") or ""),
    )
    total = 0.0
    for it in items:
        qte = max(1, int(it.get("quantity") or 1))
        prix = float(it.get("price") or 0)
        CommandeItem.objects.create(
            commande=cmd,
            nom_produit=str(it.get("name") or "Article")[:200],
            prix_unit=prix,
            quantite=qte,
        )
        total += prix * qte
    cmd.montant_total = total
    cmd.save()
    return JsonResponse({"success": True, "total": round(total, 2), "id": cmd.id})


@csrf_exempt
def api_call_waiter(request):
    """Contrat flipbook : POST {restaurant_slug, table_number} -> {success: true}"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"})
    try:
        b = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON invalide"})
    table = str(b.get("table_number") or "").strip()
    if not table:
        return JsonResponse({"success": False, "error": "Numéro de table requis"})
    AppelServeur.objects.create(
        restaurant_slug=str(b.get("restaurant_slug") or "millionnaire"),
        numero_table=table,
    )
    return JsonResponse({"success": True})


def api_stats(request):
    jour = Commande.objects.filter(statut="recue").count()
    return JsonResponse({"success": True, "data": {
        "commandes_total": Commande.objects.count(),
        "commandes_en_attente": jour,
        "appels_en_attente": AppelServeur.objects.filter(traite=False).count(),
    }})
