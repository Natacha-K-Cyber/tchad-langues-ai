# 🚀 Instructions pour pousser vers GitHub

## ✅ Étape 1 : Créer le dépôt privé sur GitHub

**IMPORTANT** : Fais ça d'abord avant de pousser le code !

1. Va sur : https://github.com/new
2. Remplis :
   - **Repository name** : `tchad-langues-ai`
   - **Description** : `Application éducative pour apprendre les langues du Tchad avec IA`
   - ✅ **Coche "Private"** (dépôt privé)
   - ❌ Ne coche PAS "Add a README file"
   - ❌ Ne coche PAS "Add .gitignore"
   - ❌ Ne choisis PAS de licence
3. Clique sur **"Create repository"**

## ✅ Étape 2 : Pousser le code (après avoir créé le dépôt)

Le remote est déjà configuré avec ton username : **Natacha-K-Cyber**

Exécute simplement :

```bash
cd C:\Users\ubunt\tchad-langues-ai
git push -u origin main
```

## 🔐 Étape 3 : Authentification

Si GitHub te demande de t'authentifier :

### Option 1 : Personal Access Token (Recommandé)

1. Va sur : https://github.com/settings/tokens
2. Clique sur **"Generate new token"** → **"Generate new token (classic)"**
3. Donne un nom : `tchad-langues-ai`
4. Sélectionne : ✅ **repo** (accès complet aux dépôts)
5. Clique sur **"Generate token"**
6. **Copie le token** (tu ne le verras qu'une fois !)
7. Quand Git te demande le mot de passe, **colle le token** au lieu du mot de passe
8. Pour le username, entre : `Natacha-K-Cyber`

### Option 2 : GitHub Desktop (Plus simple)

Si tu préfères une interface graphique :
1. Installe GitHub Desktop : https://desktop.github.com/
2. Connecte-toi avec ton compte
3. Ajoute le dépôt local
4. Clique sur "Publish repository"

## ✅ Vérification

Une fois fait, vérifie que tout est bien sauvegardé :
- Va sur : https://github.com/Natacha-K-Cyber/tchad-langues-ai
- Tu devrais voir tous tes fichiers
- Le dépôt doit être marqué comme **Private** 🔒

## 📝 Commandes utiles pour la suite

```bash
# Voir l'état des fichiers
git status

# Ajouter des fichiers modifiés
git add .

# Faire un commit
git commit -m "Description de tes changements"

# Pousser vers GitHub
git push
```

## ⚠️ Important

- Les fichiers dans `data/raw/`, `data/processed/`, `models/` ne seront **PAS** sauvegardés (trop volumineux)
- Seul le code source est sauvegardé
- Les données sensibles restent locales

