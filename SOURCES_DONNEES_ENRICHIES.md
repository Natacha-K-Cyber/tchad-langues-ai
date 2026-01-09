# 📚 Sources de données enrichies pour les langues du Tchad

## 🎯 Objectif : Enrichir le corpus d'entraînement

Actuellement : **1923 entrées** - Objectif : **10,000+ entrées**

## 📖 Sources textuelles supplémentaires

### 1. SIL International - Ethnologue
- **URL** : https://www.ethnologue.com/language/sre
- **Contenu** : Dictionnaires, grammaires, corpus
- **Action** : Contacter SIL pour accès aux ressources

### 2. Glottolog
- **URL** : https://glottolog.org/
- **Recherche** : "Sara", "Central Sara", "Sara-Bagirmi"
- **Contenu** : Références bibliographiques, corpus linguistiques

### 3. OLAC (Open Language Archives Community)
- **URL** : http://www.language-archives.org/
- **Recherche** : "Sara", "Chad"
- **Contenu** : Archives linguistiques ouvertes

### 4. HAL Archives (France)
- **URL** : https://hal.archives-ouvertes.fr/
- **Recherches** :
  - "Sara language Chad"
  - "langue sara tchad"
  - "Sara-Bagirmi languages"
  - "linguistique tchad"
- **Contenu** : Thèses, articles, corpus

### 5. Google Scholar
- **Recherches** :
  - "Sara language Chad dictionary"
  - "Sara-Bagirmi languages corpus"
  - "Chad linguistics Sara"
- **Contenu** : Articles académiques, PDFs

### 6. ResearchGate
- **URL** : https://www.researchgate.net/
- **Recherche** : "Sara language", "Chad languages"
- **Contenu** : Publications, datasets

### 7. YouTube (transcription audio → texte)
- **Recherches** :
  - "langue sara tchad"
  - "apprendre sara"
  - "conte sara tchad"
  - "cours sara"
  - "dialogue sara"
- **Action** : Extraire audio → Transcrire avec Whisper → Ajouter au corpus

### 8. Radio/Télévision tchadienne
- Émissions en langue Sara
- Archives disponibles
- Transcription nécessaire

## 🎤 Sources audio pour prononciation

### 1. Mozilla Common Voice
- **URL** : https://commonvoice.mozilla.org/
- **Codes langue** : "sre" (Sara), "chad"
- **Format** : Audio + transcriptions
- **Action** : Vérifier disponibilité, télécharger dataset

### 2. YouTube (extraction audio)
- **Outils** : yt-dlp
- **Format** : WAV ou MP3
- **Transcription** : Whisper
- **Action** : Télécharger → Transcrire → Aligner

### 3. Shtooka Project
- **URL** : https://shtooka.net/
- **Contenu** : Enregistrements de mots prononcés
- **Format** : Audio + transcriptions

### 4. Enregistrements personnels
- **Ta voix** : Utiliser le script `prepare_audio_recording.py`
- **Locuteurs natifs** : Collaborations
- **Format** : WAV 16kHz minimum

## 🔧 Outils pour la collecte audio

### Installation
```bash
# Pour YouTube
pip install yt-dlp

# Pour transcription
pip install openai-whisper

# Pour traitement audio
pip install librosa soundfile
```

### Utilisation

**1. Télécharger audio depuis YouTube** :
```bash
yt-dlp -x --audio-format wav --audio-quality 0 URL_VIDEO
```

**2. Transcrire avec Whisper** :
```bash
whisper audio.wav --language fr --model base
```

**3. Aligner audio-transcription** :
- Utiliser `aeneas` ou `gentle` pour l'alignement
- Créer des segments audio-text

## 📊 Plan d'enrichissement

### Phase 1 : Collecte textuelle (Objectif : 5000+ phrases)
1. ✅ Morkeg Books (fait - 1923 entrées)
2. 🔄 Persée.fr (en cours)
3. ⏳ HAL Archives
4. ⏳ Google Scholar
5. ⏳ YouTube (transcription)

### Phase 2 : Collecte audio (Objectif : 5000+ enregistrements)
1. ⏳ Common Voice
2. ⏳ YouTube (extraction)
3. ⏳ Enregistrements personnels
4. ⏳ Shtooka

### Phase 3 : Intégration audio-text
1. ⏳ Transcription automatique (Whisper)
2. ⏳ Alignement audio-transcription
3. ⏳ Création dataset multimédia

## 🎯 Stratégie d'enrichissement rapide

### Option A : YouTube (le plus rapide)
- Beaucoup de contenu disponible
- Extraction audio facile
- Transcription automatique avec Whisper
- **Avantage** : Rapide, beaucoup de données

### Option B : Enregistrements personnels
- Qualité contrôlée
- Disponible immédiatement
- **Avantage** : Qualité garantie

### Option C : Combinaison
- YouTube pour volume
- Enregistrements personnels pour qualité
- **Avantage** : Meilleur des deux

## 📝 Scripts créés

1. `collect_audio_sources.py` - Plan de collecte audio
2. `transcribe_audio.py` - Transcription avec Whisper
3. `prepare_audio_recording.py` - Guide d'enregistrement

## 🚀 Actions immédiates

1. **Installer les outils** :
```bash
pip install yt-dlp openai-whisper librosa
```

2. **Télécharger quelques vidéos YouTube** pour tester

3. **Transcrire avec Whisper** pour obtenir du texte

4. **Ajouter au corpus** d'entraînement

## 💡 Astuce

Pendant que l'entraînement tourne, tu peux :
- Télécharger des vidéos YouTube
- Les transcrire avec Whisper
- Enrichir le corpus pour le prochain entraînement

