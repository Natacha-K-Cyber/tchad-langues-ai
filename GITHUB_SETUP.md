# 📦 Configuration GitHub - Dépôt Privé

## Étape 1 : Créer un dépôt privé sur GitHub

1. Va sur https://github.com
2. Clique sur le bouton **"+"** en haut à droite
3. Sélectionne **"New repository"**
4. Remplis les informations :
   - **Repository name** : `tchad-langues-ai`
   - **Description** : "Application éducative pour apprendre les langues du Tchad avec IA"
   - **Visibilité** : ✅ **Private** (IMPORTANT - coche cette case !)
   - **NE PAS** cocher "Add a README file" (on en a déjà un)
   - **NE PAS** ajouter .gitignore (on en a déjà un)
   - **NE PAS** choisir une licence pour l'instant
5. Clique sur **"Create repository"**

## Étape 2 : Connecter ton dépôt local à GitHub

Après avoir créé le dépôt, GitHub te donnera des instructions. Utilise ces commandes :

```bash
cd C:\Users\ubunt\tchad-langues-ai

# Ajouter le dépôt distant (remplace TON_USERNAME par ton nom d'utilisateur GitHub)
git remote add origin https://github.com/TON_USERNAME/tchad-langues-ai.git

# Renommer la branche principale en 'main' (si nécessaire)
git branch -M main

# Pousser le code vers GitHub
git push -u origin main
```

## Étape 3 : Authentification

Si GitHub te demande de t'authentifier :
- Utilise un **Personal Access Token** (PAT) au lieu d'un mot de passe
- Pour créer un PAT : GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Donne-lui les permissions `repo` (accès complet aux dépôts)

## Vérification

Une fois fait, tu peux vérifier que tout est bien sauvegardé :
- Va sur https://github.com/TON_USERNAME/tchad-langues-ai
- Tu devrais voir tous tes fichiers
- Le dépôt doit être marqué comme **Private** 🔒

## Commandes Git utiles pour la suite

```bash
# Voir l'état des fichiers modifiés
git status

# Ajouter des fichiers modifiés
git add .

# Faire un commit
git commit -m "Description de tes changements"

# Pousser vers GitHub
git push

# Récupérer les dernières modifications (si tu travailles sur plusieurs machines)
git pull
```

## ⚠️ Important

- Les fichiers dans `data/raw/`, `data/processed/`, `models/` ne seront **PAS** sauvegardés (trop volumineux)
- Seul le code source est sauvegardé
- Les données sensibles restent locales

