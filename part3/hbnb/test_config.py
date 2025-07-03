from app import create_app

print("==== TEST CONFIGURATION FACTORY ====\n")

# Application en mode développement (défaut)
app_dev = create_app()
print("[DEV] DEBUG =", app_dev.config["DEBUG"])
print("[DEV] SECRET_KEY =", app_dev.config["SECRET_KEY"])

# Application en mode production (si tu as ajouté la classe ProductionConfig dans config.py)
try:
    app_prod = create_app("config.ProductionConfig")
    print("[PROD] DEBUG =", app_prod.config["DEBUG"])
    print("[PROD] SECRET_KEY =", app_prod.config["SECRET_KEY"])
except Exception as e:
    print("[PROD] Impossible de charger config.ProductionConfig :", e)

print("\n====================================")
