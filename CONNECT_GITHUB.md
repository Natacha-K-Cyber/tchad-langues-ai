# 🔗 Connecter ton projet à GitHub (Dépôt Privé)

## Étape 1 : Créer le dépôt privé sur GitHub

1. **Va sur** https://github.com et connecte-toi
2. **Clique sur le bouton "+"** en haut à droite → **"New repository"**
3. **Remplis le formulaire** :
   - **Repository name** : `tchad-langues-ai`
   - **Description** : `Application éducative pour apprendre les langues du Tchad avec IA`
   - **Visibilité** : ✅ **Private** (IMPORTANT - coche cette case !)
   - ❌ **NE PAS** cocher "Add a README file"
   - ❌ **NE PAS** cocher "Add .gitignore"
   - ❌ **NE PAS** choisir de licence
4. **Clique sur "Create repository"**

## Étape 2 : Connecter ton dépôt local

Après avoir créé le dépôt, GitHub affichera une page avec des instructions.

**Remplace `TON_USERNAME` par ton nom d'utilisateur GitHub** dans cette commande :

```bash
cd C:\Users\ubunt\tchad-langues-ai
git remote add origin https://github.com/TON_USERNAME/tchad-langues-ai.git
```

**Exemple** : Si ton username est `john-doe`, la commande sera :
```bash
git remote add origin https://github.com/john-doe/tchad-langues-ai.git
```

## Étape 3 : Pousser ton code

```bash
# Pousser vers GitHub
git push -u origin main
```

## Étape 4 : Authentification

Si GitHub te demande de t'authentifier :

### Option A : Personal Access Token (Recommandé)
1. Va sur : https://github.com/settings/tokens
2. Clique sur **"Generate new token"** → **"Generate new token (classic)"**
3. Donne un nom : `tchad-langues-ai`
4. Sélectionne la permission : ✅ **repo** (accès complet aux dépôts)
5. Clique sur **"Generate token"**
6. **Copie le token** (tu ne le verras qu'une fois !)
7. Quand Git te demande le mot de passe, **colle le token** au lieu du mot de passe

### Option B : GitHub CLI (Alternative)
```bash
# Installer GitHub CLI si tu veux
# Puis utiliser: gh auth login
```

## Vérification

Une fois fait :
- Va sur : `https://github.com/TON_USERNAME/tchad-langues-ai`
- Tu devrais voir tous tes fichiers
- Le dépôt doit être marqué comme **Private** 🔒

## Commandes Git pour la suite

```bash
# Voir l'état
git status

# Ajouter des fichiers
git add .

# Faire un commit
git commit -m "Description de tes changements"

# Pousser vers GitHub
git push
```

## ⚠️ Important

- Les fichiers dans `data/raw/`, `data/processed/`, `models/` ne seront **PAS** sauvegardés (trop volumineux, dans .gitignore)
- Seul le code source est sauvegardé
- Les données sensibles restent locales

