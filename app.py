import requests

def convertir_devises(montant, devise_source, devise_cible):
    url = f"https://api.exchangerate-api.com/v4/latest/{devise_source}"
    response = requests.get(url)
    data = response.json()
    taux_conversion = data['rates'][devise_cible]
    return montant * taux_conversion

if __name__ == "__main__":
    montant = float(input("Entrez le montant à convertir: "))
    devise_source = input("Entrez la devise source (par exemple, USD): ")
    devise_cible = input("Entrez la devise cible (par exemple, EUR): ")
    montant_converti = convertir_devises(montant, devise_source, devise_cible)
    print(f"{montant} {devise_source} équivaut à {montant_converti} {devise_cible}")
