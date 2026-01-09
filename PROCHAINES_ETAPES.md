# 🚀 Prochaines étapes après l'installation

## ✅ Ce qui est fait
- ✅ VM Kali configurée (20GB RAM, 8 CPU)
- ✅ Environnement Python installé
- ✅ Toutes les bibliothèques ML installées
- ✅ Environnement virtuel activé

## 📋 Étape 1 : Vérifier que tu es dans le bon répertoire

```bash
# Tu devrais être dans le dossier du projet
pwd
# Devrait afficher : /home/tyma/tchad-langues-ai

# Si tu n'es pas là, va dedans :
cd ~/tchad-langues-ai

# Vérifier que l'environnement virtuel est activé
# Tu devrais voir (venv) au début de ta ligne de commande
# Si ce n'est pas le cas :
source venv/bin/activate
```

## 📋 Étape 2 : Collecter les données

### 2.1 : Télécharger le lexique Morkeg Books

```bash
# Télécharger le PDF du lexique Sara
python scripts/data_collection/download_morkeg.py
```

Cela va :
- Télécharger le PDF depuis Morkeg Books
- Le sauvegarder dans `data/raw/morkeg/`

### 2.2 : Extraire le texte du PDF

```bash
# Extraire le texte du PDF téléchargé
python scripts/data_processing/extract_pdf_text.py
```

Cela va :
- Extraire le texte du PDF
- Sauvegarder les données dans `data/processed/`

### 2.3 : Explorer d'autres sources (optionnel mais recommandé)

```bash
# Voir les sources disponibles
python scripts/data_collection/explore_sources.py
```

## 📋 Étape 3 : Préparer les données pour l'entraînement

### 3.1 : Créer le corpus d'entraînement

Une fois les données collectées, il faut les formater pour l'entraînement :

```bash
# Créer le script de préparation (on va le créer)
python scripts/data_processing/prepare_training_data.py
```

### 3.2 : Vérifier les données préparées

```bash
# Vérifier que les données sont prêtes
ls -lh data/training/
```

## 📋 Étape 4 : Configurer l'entraînement

### 4.1 : Vérifier la configuration

```bash
# Voir la configuration actuelle
cat config.yaml
```

### 4.2 : Ajuster les paramètres si nécessaire

Pour 20GB RAM, la configuration devrait être :
- `per_device_train_batch_size: 2`
- `use_quantization: true` (4-bit)
- `use_lora: true`

## 📋 Étape 5 : Tester avec un petit modèle d'abord (Recommandé)

Avant d'entraîner Mistral 7B, teste avec un modèle plus petit :

```bash
# Tester avec TinyLlama 1.1B (plus rapide, moins de RAM)
# On va créer un script de test
python scripts/training/test_small_model.py
```

## 📋 Étape 6 : Entraîner le modèle

Une fois les données prêtes :

```bash
# Lancer l'entraînement
python scripts/training/fine_tune_llm.py
```

## 🎯 Plan d'action immédiat

**Commence par :**

1. **Télécharger les données** :
   ```bash
   python scripts/data_collection/download_morkeg.py
   ```

2. **Extraire le texte** :
   ```bash
   python scripts/data_processing/extract_pdf_text.py
   ```

3. **Vérifier ce qui a été collecté** :
   ```bash
   ls -lh data/raw/morkeg/
   ls -lh data/processed/
   ```

## ⚠️ Important

- Assure-toi d'avoir une **connexion internet** pour télécharger les données
- Le téléchargement du PDF peut prendre quelques minutes
- L'extraction du texte peut prendre 5-10 minutes selon la taille du PDF

## 📝 Checklist

- [ ] Environnement virtuel activé
- [ ] Dans le bon répertoire (`~/tchad-langues-ai`)
- [ ] Télécharger le lexique Morkeg Books
- [ ] Extraire le texte du PDF
- [ ] Vérifier les données collectées
- [ ] Préparer les données pour l'entraînement
- [ ] Configurer l'entraînement
- [ ] Tester avec un petit modèle
- [ ] Entraîner le modèle final

## 💡 Astuce

Si une commande échoue, lis le message d'erreur et dis-moi ce qui ne va pas. Je t'aiderai à corriger !

