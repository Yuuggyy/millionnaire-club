import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Commande, CommandeItem, AppelServeur, Categorie, Produit, Parametre


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


@csrf_exempt
def api_stats(request):
    jour = Commande.objects.filter(statut="recue").count()
    return JsonResponse({"success": True, "data": {
        "commandes_total": Commande.objects.count(),
        "commandes_en_attente": jour,
        "appels_en_attente": AppelServeur.objects.filter(traite=False).count(),
    }})


# ---------------------------------------------------------------------------
# API ADMINISTRATION (panel maison — même contrat que les autres restaurants)
# ---------------------------------------------------------------------------

import hashlib
import os as _os


def _admin_creds():
    return (
        _os.environ.get("ADMIN_EMAIL", "admin@millionnaireclub.cd"),
        _os.environ.get("ADMIN_PASSWORD", "MClub!2026Kinshasa"),
    )


def _admin_token():
    email, pwd = _admin_creds()
    return hashlib.sha256(f"{email}:{pwd}".encode()).hexdigest()


def _admin_ok(request):
    return request.headers.get("X-Admin-Token", "") == _admin_token()


@csrf_exempt
def api_admin_login(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    email, pwd = _admin_creds()
    if d.get("email") == email and d.get("password") == pwd:
        return JsonResponse({"success": True, "token": _admin_token()})
    return JsonResponse({"success": False, "error": "Identifiants incorrects"}, status=401)


def _commande_json(c):
    return {
        "id": c.id,
        "table": c.numero_table,
        "total": c.montant_total,
        "statut": c.statut,
        "notes": c.demandes_speciales,
        "created_at": c.created_at.strftime("%d/%m/%Y %H:%M"),
        "items": [{"nom": i.nom_produit, "prix": i.prix_unit, "qte": i.quantite} for i in c.items.all()],
    }


@csrf_exempt
def api_admin_commandes(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    rows = Commande.objects.prefetch_related("items").all()[:200]
    return JsonResponse({"success": True, "commandes": [_commande_json(c) for c in rows]})


@csrf_exempt
def api_admin_commande_statut(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    statut = d.get("statut", "")
    if statut not in ("recue", "en_cours", "terminee", "annulee"):
        return JsonResponse({"success": False, "error": "Statut invalide"}, status=400)
    try:
        c = Commande.objects.get(id=d.get("id"))
    except Commande.DoesNotExist:
        return JsonResponse({"success": False, "error": "Commande introuvable"}, status=404)
    c.statut = statut
    c.save()
    return JsonResponse({"success": True})


@csrf_exempt
def api_admin_commande_delete(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    Commande.objects.filter(id=d.get("id")).delete()
    return JsonResponse({"success": True})


@csrf_exempt
def api_admin_appels(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    rows = AppelServeur.objects.all()[:200]
    return JsonResponse({"success": True, "appels": [
        {"id": a.id, "table": a.numero_table, "traite": a.traite, "created_at": a.created_at.strftime("%d/%m/%Y %H:%M")}
        for a in rows
    ]})


@csrf_exempt
def api_admin_appel_traiter(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    try:
        a = AppelServeur.objects.get(id=d.get("id"))
    except AppelServeur.DoesNotExist:
        return JsonResponse({"success": False, "error": "Appel introuvable"}, status=404)
    a.traite = bool(d.get("traite", True))
    a.save()
    return JsonResponse({"success": True})


@csrf_exempt
def api_admin_stats(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    return JsonResponse({
        "success": True,
        "commandes_actives": Commande.objects.filter(statut__in=["recue", "en_cours"]).count(),
        "appels_en_attente": AppelServeur.objects.filter(traite=False).count(),
    })


# ---------------------------------------------------------------------------
# MENU PUBLIC (le flipbook se remplit depuis la base)
# ---------------------------------------------------------------------------

@csrf_exempt
def api_menu(request):
    cats = Categorie.objects.filter(actif=True).prefetch_related("plats")
    return JsonResponse({"success": True, "categories": [
        {"id": c.id, "nom": c.nom, "ordre": c.ordre,
         "plats": [{"id": p.id, "nom": p.nom, "description": p.description, "prix": p.prix,
                    "disponible": p.disponible, "ordre": p.ordre} for p in c.plats.all() if p.disponible]}
        for c in cats
    ]})


# ---------------------------------------------------------------------------
# CRUD CATEGORIES / PRODUITS / PARAMETRES (panel maison)
# ---------------------------------------------------------------------------

@csrf_exempt
def api_admin_categories(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    cats = Categorie.objects.all()
    return JsonResponse({"success": True, "categories": [
        {"id": c.id, "nom": c.nom, "ordre": c.ordre, "actif": c.actif} for c in cats
    ]})


@csrf_exempt
def api_admin_categorie_save(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    nom = str(d.get("nom", "")).strip()
    if not nom:
        return JsonResponse({"success": False, "error": "Le nom est obligatoire"}, status=400)
    fields = {"nom": nom, "ordre": int(d.get("ordre", 10) or 10), "actif": bool(d.get("actif", True))}
    if d.get("id"):
        Categorie.objects.filter(id=d["id"]).update(**fields)
    else:
        Categorie.objects.create(**fields)
    return JsonResponse({"success": True})


@csrf_exempt
def api_admin_categorie_delete(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    Categorie.objects.filter(id=d.get("id")).delete()
    return JsonResponse({"success": True})


@csrf_exempt
def api_admin_produits(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    plats = Produit.objects.select_related("categorie").all()
    return JsonResponse({"success": True, "produits": [
        {"id": p.id, "categorie_id": p.categorie_id, "categorie": p.categorie.nom,
         "nom": p.nom, "description": p.description, "prix": p.prix,
         "disponible": p.disponible, "ordre": p.ordre} for p in plats
    ]})


@csrf_exempt
def api_admin_produit_save(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    nom = str(d.get("nom", "")).strip()
    if not nom:
        return JsonResponse({"success": False, "error": "Le nom est obligatoire"}, status=400)
    try:
        cat = Categorie.objects.get(id=d.get("categorie_id"))
    except Categorie.DoesNotExist:
        return JsonResponse({"success": False, "error": "Catégorie introuvable"}, status=400)
    fields = {
        "categorie": cat, "nom": nom,
        "description": str(d.get("description", "") or ""),
        "prix": float(d.get("prix", 0) or 0),
        "ordre": int(d.get("ordre", 10) or 10),
        "disponible": bool(d.get("disponible", True)),
    }
    if d.get("id"):
        Produit.objects.filter(id=d["id"]).update(**{k: v for k, v in fields.items()})
    else:
        Produit.objects.create(**fields)
    return JsonResponse({"success": True})


@csrf_exempt
def api_admin_produit_delete(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    Produit.objects.filter(id=d.get("id")).delete()
    return JsonResponse({"success": True})


@csrf_exempt
def api_admin_parametres(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    return JsonResponse({"success": True, "parametres": [
        {"id": p.id, "cle": p.cle, "valeur": p.valeur} for p in Parametre.objects.all()
    ]})


@csrf_exempt
def api_admin_parametre_save(request):
    if not _admin_ok(request):
        return JsonResponse({"success": False, "error": "Non autorisé"}, status=401)
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)
    d = json.loads(request.body or "{}")
    cle = str(d.get("cle", "")).strip()
    if not cle:
        return JsonResponse({"success": False, "error": "La clé est obligatoire"}, status=400)
    obj, _ = Parametre.objects.update_or_create(cle=cle, defaults={"valeur": str(d.get("valeur", "") or "")})
    return JsonResponse({"success": True, "id": obj.id})
