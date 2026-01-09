# 💻 Spécifications VM recommandées pour l'entraînement

## 🎯 Configuration recommandée pour un début sérieux

### Option 1 : Minimum viable (POC sérieux)
**RAM : 16 GB**
**Stockage : 100 GB**

**Pourquoi :**
- Permet d'entraîner **Mistral 7B** avec LoRA + 4-bit quantization
- Batch size de 2-4 (acceptable)
- Peut charger le modèle + données + système
- Checkpoints et logs possibles

**Limitations :**
- Batch size limité
- Pas de GPU (CPU seulement, plus lent)
- Entraînement plus long mais faisable

### Option 2 : Recommandé (Confortable)
**RAM : 32 GB**
**Stockage : 150-200 GB**

**Pourquoi :**
- Batch size de 4-8 (meilleure convergence)
- Plus de marge pour les données
- Plusieurs checkpoints simultanés
- Meilleure performance globale

**Avantages :**
- Entraînement plus rapide
- Plus de flexibilité
- Peut tester différents hyperparamètres

### Option 3 : Idéal (Production)
**RAM : 64 GB**
**Stockage : 250-500 GB**
**GPU : NVIDIA (optionnel mais recommandé)**

**Pourquoi :**
- Batch size élevé (8-16)
- Entraînement très rapide avec GPU
- Peut entraîner plusieurs modèles
- Prêt pour la production

## 📊 Détails techniques

### Utilisation de la RAM (Mistral 7B avec LoRA + 4-bit)

| Composant | RAM utilisée |
|-----------|--------------|
| Modèle 7B (4-bit) | ~4-5 GB |
| LoRA adapters | ~0.5-1 GB |
| Données d'entraînement | ~2-4 GB |
| Gradients + Optimizer | ~2-4 GB |
| Système + Python | ~2-3 GB |
| **TOTAL** | **~12-17 GB** |

**Conclusion : 16 GB minimum, 32 GB recommandé**

### Utilisation du stockage

| Élément | Espace nécessaire |
|---------|-------------------|
| Modèle de base (7B) | ~4-5 GB |
| Données d'entraînement | ~5-10 GB |
| Checkpoints (x10) | ~20-30 GB |
| Logs et métriques | ~5-10 GB |
| Environnement Python | ~5-10 GB |
| Système Kali | ~20-30 GB |
| **TOTAL** | **~60-95 GB** |

**Conclusion : 100 GB minimum, 150-200 GB recommandé**

## 🛠️ Configuration VM Kali Linux

### Configuration recommandée (Option 2)

```
RAM : 32 GB
Stockage : 200 GB
CPU : 4-8 cores (si possible)
GPU : Optionnel (NVIDIA si disponible)
```

### Pourquoi cette configuration ?

1. **32 GB RAM** :
   - Permet batch size confortable (4-8)
   - Marge pour les données volumineuses
   - Pas de problèmes de mémoire
   - Peut faire du fine-tuning efficace

2. **200 GB Stockage** :
   - Assez pour plusieurs modèles
   - Checkpoints multiples
   - Données d'entraînement
   - Logs et expérimentations

3. **CPU 4-8 cores** :
   - Parallélisation du traitement
   - Entraînement plus rapide
   - Meilleure gestion des données

## 📋 Outils open source utilisés

Tous les outils sont open source :

- **PyTorch** - Framework ML
- **Transformers (Hugging Face)** - Modèles LLM
- **PEFT / LoRA** - Fine-tuning efficace
- **BitsAndBytes** - Quantization 4-bit
- **Accelerate** - Optimisation d'entraînement
- **Datasets** - Gestion des données
- **Streamlit** - Interface web

## 🚀 Plan d'action

### Étape 1 : Configurer la VM
- Augmenter RAM à **32 GB**
- Augmenter stockage à **200 GB**
- Allouer **4-8 CPU cores** si possible

### Étape 2 : Installer l'environnement
```bash
# Sur Kali Linux
sudo apt update
sudo apt install python3.10 python3-pip git build-essential

# Cloner le projet
git clone https://github.com/Natacha-K-Cyber/tchad-langues-ai.git
cd tchad-langues-ai

# Créer environnement
python3 -m venv venv
source venv/bin/activate

# Installer PyTorch (CPU ou CUDA selon GPU)
pip install torch torchvision torchaudio

# Installer dépendances ML
pip install transformers datasets accelerate peft bitsandbytes
pip install streamlit pandas pyyaml tqdm
```

### Étape 3 : Tester avec un petit modèle d'abord
- Commencer avec **TinyLlama 1.1B** pour valider le pipeline
- Puis passer à **Mistral 7B** une fois que tout fonctionne

## 💡 Alternative : Cloud (si VM limitée)

Si tu ne peux pas augmenter la VM, utilise :

- **Google Colab Pro** (~10€/mois) : GPU T4, 25GB RAM
- **Kaggle Notebooks** (gratuit) : GPU P100, 30GB RAM
- **Hugging Face Spaces** (gratuit) : GPU limité

## 📝 Résumé des recommandations

| Configuration | RAM | Stockage | Usage |
|---------------|-----|----------|-------|
| **Minimum** | 16 GB | 100 GB | POC sérieux |
| **Recommandé** | 32 GB | 200 GB | Développement confortable |
| **Idéal** | 64 GB | 500 GB | Production |

**Pour un début sérieux : 32 GB RAM + 200 GB stockage** ✅

## ⚠️ Note importante

- **Sans GPU** : L'entraînement sera plus lent (CPU seulement)
- **Avec GPU** : Beaucoup plus rapide (10-50x)
- Pour un POC, CPU est acceptable
- Pour la production, GPU recommandé

