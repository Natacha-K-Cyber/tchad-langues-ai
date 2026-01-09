# 🚀 Installation complète sur Kali Linux - Guide pas à pas

## ✅ Prérequis vérifiés
- ✅ VM Kali lancée
- ✅ Stockage augmenté (80-100 GB)
- ✅ Connexion internet active

## 📋 Étape 1 : Vérifier l'espace disque

```bash
# Vérifier l'espace disponible
df -h /

# Tu devrais voir au moins 60-70 GB libres
```

## 📋 Étape 2 : Mettre à jour le système

```bash
# Mettre à jour la liste des paquets
sudo apt update

# Mettre à jour le système (optionnel mais recommandé)
sudo apt upgrade -y
```

## 📋 Étape 3 : Installer les dépendances de base

```bash
# Installer les outils essentiels
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    git \
    build-essential \
    curl \
    wget \
    bc
```

## 📋 Étape 4 : Cloner le projet depuis GitHub

```bash
# Aller dans le dossier home
cd ~

# Cloner le projet
git clone https://github.com/Natacha-K-Cyber/tchad-langues-ai.git

# Aller dans le dossier du projet
cd tchad-langues-ai

# Vérifier que tout est là
ls -la
```

## 📋 Étape 5 : Rendre le script d'installation exécutable

```bash
# Rendre le script exécutable
chmod +x KALI_SETUP.sh

# Vérifier les permissions
ls -l KALI_SETUP.sh
```

## 📋 Étape 6 : Exécuter le script d'installation

```bash
# Exécuter le script (cela peut prendre 15-30 minutes)
./KALI_SETUP.sh
```

Le script va :
- ✅ Vérifier l'espace disque
- ✅ Nettoyer le système
- ✅ Installer les dépendances
- ✅ Créer l'environnement Python
- ✅ Installer PyTorch et toutes les bibliothèques ML

## 📋 Étape 7 : Activer l'environnement virtuel

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Tu devrais voir (venv) au début de ta ligne de commande
```

## 📋 Étape 8 : Vérifier l'installation

```bash
# Vérifier Python
python --version
# Devrait afficher Python 3.10.x

# Vérifier PyTorch
python -c "import torch; print('PyTorch:', torch.__version__)"

# Vérifier Transformers
python -c "import transformers; print('Transformers:', transformers.__version__)"

# Vérifier PEFT (pour LoRA)
python -c "import peft; print('PEFT:', peft.__version__)"
```

## 📋 Étape 9 : Vérifier l'espace disque après installation

```bash
# Vérifier l'espace restant
df -h /

# Vérifier la taille de l'environnement
du -sh venv/
```

## 🎯 Prochaines étapes

Une fois l'installation terminée :

1. **Collecter les données** :
   ```bash
   python scripts/data_collection/download_morkeg.py
   python scripts/data_collection/explore_sources.py
   ```

2. **Préparer les données** :
   ```bash
   python scripts/data_processing/extract_pdf_text.py
   ```

3. **Configurer l'entraînement** :
   - Modifier `config.yaml` si nécessaire
   - Vérifier les paramètres d'entraînement

4. **Commencer l'entraînement** (une fois les données prêtes)

## ⚠️ En cas de problème

### Problème : "Permission denied"
```bash
chmod +x KALI_SETUP.sh
```

### Problème : "Command not found: python3.10"
```bash
sudo apt install python3.10 python3.10-venv
```

### Problème : Espace disque insuffisant
```bash
# Nettoyer les caches
sudo apt clean
pip cache purge
```

### Problème : Installation PyTorch échoue
```bash
# Réessayer avec l'index CPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## 📝 Notes importantes

- L'installation peut prendre **15-30 minutes**
- Assure-toi d'avoir une **connexion internet stable**
- Si une étape échoue, relis le message d'erreur et corrige
- Tu peux exécuter les commandes une par une si le script ne fonctionne pas

## ✅ Checklist d'installation

- [ ] Espace disque vérifié (>60 GB libres)
- [ ] Système mis à jour
- [ ] Dépendances de base installées
- [ ] Projet cloné depuis GitHub
- [ ] Script d'installation exécuté
- [ ] Environnement virtuel activé
- [ ] PyTorch installé et vérifié
- [ ] Transformers installé et vérifié
- [ ] PEFT installé et vérifié

Une fois tout coché, tu es prêt(e) ! 🎉

