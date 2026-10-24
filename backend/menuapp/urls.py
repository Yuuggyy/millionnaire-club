from django.urls import path

from . import views

urlpatterns = [
    path("submitOrder/", views.api_submit_order, name="api-submit-order"),
    path("callWaiter/", views.api_call_waiter, name="api-call-waiter"),
    path("stats/", views.api_stats, name="api-stats"),
    path("menu/", views.api_menu, name="api-menu"),

    # Panel maison
    path("admin/login/", views.api_admin_login, name="api-admin-login"),
    path("admin/commandes/", views.api_admin_commandes, name="api-admin-commandes"),
    path("admin/commande/statut/", views.api_admin_commande_statut, name="api-admin-commande-statut"),
    path("admin/commande/delete/", views.api_admin_commande_delete, name="api-admin-commande-delete"),
    path("admin/appels/", views.api_admin_appels, name="api-admin-appels"),
    path("admin/appel/traiter/", views.api_admin_appel_traiter, name="api-admin-appel-traiter"),
    path("admin/stats/", views.api_admin_stats, name="api-admin-stats"),
    path("admin/categories/", views.api_admin_categories, name="api-admin-categories"),
    path("admin/categorie/save/", views.api_admin_categorie_save, name="api-admin-categorie-save"),
    path("admin/categorie/delete/", views.api_admin_categorie_delete, name="api-admin-categorie-delete"),
    path("admin/produits/", views.api_admin_produits, name="api-admin-produits"),
    path("admin/produit/save/", views.api_admin_produit_save, name="api-admin-produit-save"),
    path("admin/produit/delete/", views.api_admin_produit_delete, name="api-admin-produit-delete"),
    path("admin/parametres/", views.api_admin_parametres, name="api-admin-parametres"),
    path("admin/parametre/save/", views.api_admin_parametre_save, name="api-admin-parametre-save"),
]
