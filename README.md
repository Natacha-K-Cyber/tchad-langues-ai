# 🌍 Tchad Langues AI - Application Éducative

Application d'apprentissage des langues du Tchad avec une approche gamifiée inspirée de Duolingo, adaptée à l'univers africain subsaharien avec des personnages authentiques.

## 🎯 Concept

Une application éducative et pédagogique pour apprendre les langues du Tchad, avec :
- **Interface gamifiée** type Duolingo
- **Personnages authentiques** avec des noms en langue Sara (Neloumta, Togue, Ronel, Senny, Manta, Ngar, Nouba, Neloumta, Nodji, Milamem)
- **Design africain** avec des couleurs et motifs inspirés de l'Afrique subsaharienne
- **IA fine-tunée** avec des LLMs open source (Mistral/Llama)

## 📚 Langues supportées (Phase 1)

- **Sara (Sarh)** 🇹🇩 - Langue principale du groupe Sara
- **Gambaye** 🇹🇩 - Dialecte Sara de la région de Gambaye  
- **Mbaye** 🇹🇩 - Dialecte Sara de la région de Mbaye
- **Arabe tchadien** 🇹🇩 - Arabe parlé au Tchad

## 👥 Personnages

Tous les personnages ont des noms authentiques en langue Sara :

- **Neloumta** 👨🏿 - Guide bienveillant et sage, expert des langues sara
- **Togue** 👩🏿 - Instructrice énergique et motivante
- **Ronel** 👦🏿 - Compagnon d'apprentissage amical et curieux
- **Senny** 👩🏿‍🏫 - Experte linguistique et enseignante
- **Manta** 💪🏿 - Coach motivant pour maintenir ta motivation
- **Ngar** 📖 - Narrateur des histoires et contes culturels
- **Nouba** 🤝 - Ami virtuel pour pratiquer les conversations
- **Nodji** 🎓 - Tuteur patient pour les exercices difficiles
- **Milamem** 🔥 - Gardien qui encourage à maintenir la série quotidienne

## 🗂️ Structure du projet

```
tchad-langues-ai/
├── data/
│   ├── raw/              # Documents bruts collectés
│   │   ├── persee/       # Articles Persée.fr
│   │   ├── morkeg/       # PDFs et extraits Morkeg Books
│   │   ├── common_voice/ # Données Mozilla Common Voice
│   │   └── audio_recordings/ # Enregistrements audio
│   ├── processed/        # Données nettoyées et tokenisées
│   └── training/         # Données formatées pour l'entraînement
├── scripts/
│   ├── data_collection/  # Scripts de scraping et téléchargement
│   ├── data_processing/  # Nettoyage et préparation
│   └── training/         # Scripts d'entraînement
├── models/               # Modèles entraînés
├── app/                  # Application web Streamlit
├── notebooks/            # Notebooks d'expérimentation Jupyter
├── config.yaml           # Configuration globale
└── requirements.txt      # Dépendances Python
```

## 🚀 Installation

```bash
# Cloner le projet
git clone https://github.com/TON_USERNAME/tchad-langues-ai.git
cd tchad-langues-ai

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 📋 État actuel du projet

### ✅ Fait
- Structure du projet
- Application Streamlit avec interface gamifiée
- Personnages avec noms authentiques Sara
- Système de progression (XP, niveaux, séries)
- Scripts de collecte de données
- Plan de collecte de données (texte + audio + phonétique)

### 🔄 En cours
- Collecte de données depuis diverses sources
- Préparation des données pour l'entraînement

### 📝 À faire
- Collecte audio (enregistrements)
- Ajout de transcriptions phonétiques
- Fine-tuning du modèle LLM
- Intégration du modèle dans l'application
- Tests et évaluation

## 📚 Sources de données

### Actuelles
- **Morkeg Books** - Lexique Sara Languages (PDF)
- **Persée.fr** - Articles académiques sur les langues du Tchad

### À explorer
- **Mozilla Common Voice** - Données audio open source
- **SIL International** - Base de données linguistiques
- **YouTube** - Vidéos éducatives en langue Sara
- **Collaborations** - Locuteurs natifs, écoles, universités

## 🛠️ Technologies utilisées

- **Python 3.10+**
- **Streamlit** - Interface web interactive
- **Transformers** (Hugging Face) - Modèles LLM
- **PEFT / LoRA** - Fine-tuning efficace
- **PyPDF2 / pdfplumber** - Extraction PDF
- **BeautifulSoup** - Web scraping
- **Plotly** - Graphiques interactifs

## 📖 Documentation

- `PLAN_COLLECTE_DONNEES.md` - Plan détaillé pour la collecte de données
- `QUICKSTART.md` - Guide de démarrage rapide (à venir)

## 🤝 Contribution

Ce projet est un POC en développement. Les contributions sont les bienvenues pour :
- Améliorer les données linguistiques
- Corriger les traductions
- Ajouter de nouvelles fonctionnalités
- Améliorer l'interface utilisateur

## 📄 Licence

À définir (suggestions : MIT, Apache 2.0, ou Creative Commons)

## 🔗 Références

- [Persée - Notes sur la langue des Sara (1935)](https://www.persee.fr/doc/jafr_0037-9166_1935_num_5_2_1587)
- [Morkeg Books - Sara Languages Lexicon](https://morkegbooks.com/Services/World/Languages/SaraBagirmi/pdfs/SaraLanguagesLexicon.pdf)
- [Sara-Bagirmi Language Project](http://morkegbooks.com/Services/World/Languages/SaraBagirmi)

---

**Développé avec ❤️ pour préserver et promouvoir les langues tchadiennes**

