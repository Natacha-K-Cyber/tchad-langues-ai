# ⚙️ Configuration optimisée pour 20GB RAM + 40GB Stockage

## ✅ Ta configuration actuelle

- **RAM** : 20 650 MB (~20 GB) ✅ Excellent
- **CPU** : 8 cores ✅ Excellent  
- **Stockage** : 40.08 GB ⚠️ Limité mais faisable

## 📊 Analyse de l'espace disque

### Utilisation estimée :

| Élément | Espace nécessaire |
|---------|-------------------|
| Système Kali Linux | ~15-20 GB |
| Environnement Python + packages | ~5-8 GB |
| Modèle Mistral 7B (4-bit) | ~4-5 GB |
| Données d'entraînement | ~2-5 GB |
| Checkpoints (limités à 3-5) | ~10-15 GB |
| Logs et métriques | ~2-3 GB |
| **TOTAL** | **~38-56 GB** |

### ⚠️ Attention : Stockage limité !

**40 GB est juste mais faisable si on optimise :**
- ✅ Utiliser 4-bit quantization (réduit le modèle)
- ✅ Limiter les checkpoints (garder seulement les meilleurs)
- ✅ Nettoyer régulièrement les logs
- ✅ Compresser les données

## 🎯 Configuration d'entraînement optimisée

### Paramètres adaptés pour 20GB RAM + 40GB stockage :

```yaml
model:
  base_model: "mistralai/Mistral-7B-Instruct-v0.2"
  use_quantization: true  # 4-bit OBLIGATOIRE
  use_lora: true
  lora_r: 16
  lora_alpha: 32
  lora_dropout: 0.05
  
training:
  output_dir: "./models/tchad_langues"
  num_train_epochs: 3
  per_device_train_batch_size: 2  # Adapté pour 20GB RAM
  gradient_accumulation_steps: 4  # Simule batch_size=8
  learning_rate: 2e-4
  warmup_steps: 100
  save_steps: 1000  # Moins de checkpoints pour économiser l'espace
  save_total_limit: 3  # Garder seulement 3 meilleurs checkpoints
  eval_steps: 500
  logging_steps: 100
  max_length: 512
  dataloader_num_workers: 4  # Utiliser les 8 CPU cores
```

## 💾 Gestion de l'espace disque

### Script de nettoyage (à exécuter régulièrement) :

```bash
#!/bin/bash
# Nettoyage de l'espace disque

echo "Nettoyage de l'espace disque..."

# Nettoyer les caches pip
pip cache purge

# Nettoyer les logs anciens (garder seulement les 10 derniers)
find ./logs -name "*.log" -mtime +7 -delete

# Nettoyer les checkpoints intermédiaires (garder seulement les meilleurs)
# (à faire manuellement selon tes besoins)

# Vérifier l'espace disponible
df -h /
```

### Commandes utiles :

```bash
# Vérifier l'espace disque
df -h /

# Voir les plus gros fichiers
du -sh * | sort -rh | head -10

# Nettoyer les caches
pip cache purge
apt clean
```

## 🚀 Plan d'action

### Étape 1 : Vérifier l'espace disponible
```bash
df -h /
# Assure-toi d'avoir au moins 10-15 GB libres
```

### Étape 2 : Installation optimisée
- Installer seulement les packages nécessaires
- Utiliser 4-bit quantization
- Limiter les checkpoints

### Étape 3 : Monitoring pendant l'entraînement
- Surveiller l'espace disque régulièrement
- Nettoyer les logs anciens
- Supprimer les checkpoints intermédiaires

## 📋 Recommandations

### ✅ À faire :
1. **Nettoyer le système** avant l'installation
2. **Utiliser 4-bit quantization** (obligatoire)
3. **Limiter les checkpoints** (save_total_limit: 3)
4. **Nettoyer régulièrement** les logs et caches
5. **Surveiller l'espace** pendant l'entraînement

### ❌ À éviter :
1. Ne pas sauvegarder tous les checkpoints
2. Ne pas garder tous les logs
3. Ne pas installer de packages inutiles
4. Ne pas télécharger plusieurs modèles

## 🔧 Alternative : Augmenter le stockage

Si possible, augmente le stockage à **80-100 GB** pour plus de confort :
- Dans VirtualBox : Settings → Storage → Augmenter le disque
- Ou créer un disque additionnel

## ✅ Conclusion

**Ta configuration (20GB RAM + 8 CPU) est EXCELLENTE !** ✅

Le stockage de 40GB est **limité mais faisable** avec optimisation :
- ✅ Entraînement possible
- ⚠️ Gestion de l'espace nécessaire
- 💡 Augmenter à 80GB si possible (recommandé)

**Tu peux commencer l'entraînement avec cette config !** 🚀

