#!/bin/bash
# Script d'installation pour Kali Linux
# Configuration: 20GB RAM, 8 CPU cores, 40GB stockage

echo "=========================================="
echo "Installation Tchad Langues AI sur Kali"
echo "Configuration: 20GB RAM, 8 CPU, 40GB disk"
echo "=========================================="
echo ""

# Vérifier l'espace disque
echo "[0/9] Verification de l'espace disque..."
df -h /
AVAILABLE=$(df -h / | tail -1 | awk '{print $4}' | sed 's/G//')
echo "Espace disponible: ${AVAILABLE}GB"
if (( $(echo "$AVAILABLE < 10" | bc -l) )); then
    echo "ATTENTION: Moins de 10GB disponibles!"
    read -p "Continuer quand meme? (o/n): " continue
    if [ "$continue" != "o" ]; then
        exit 1
    fi
fi
echo ""

# Mise à jour du système
echo "[1/9] Mise a jour du systeme..."
sudo apt update && sudo apt upgrade -y

# Nettoyage pour économiser l'espace
echo "[2/9] Nettoyage du systeme..."
sudo apt clean
sudo apt autoremove -y

# Installation des dépendances système (minimales)
echo "[3/9] Installation des dependances systeme..."
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    git \
    build-essential \
    curl \
    wget \
    bc

# Cloner le projet depuis GitHub
echo ""
echo "[4/9] Clonage du projet depuis GitHub..."
if [ -d "tchad-langues-ai" ]; then
    echo "Le dossier existe deja. Mise a jour..."
    cd tchad-langues-ai
    git pull
else
    git clone https://github.com/Natacha-K-Cyber/tchad-langues-ai.git
    cd tchad-langues-ai
fi

# Créer l'environnement virtuel
echo ""
echo "[5/9] Creation de l'environnement virtuel Python..."
python3.10 -m venv venv
source venv/bin/activate

# Mettre à jour pip
echo ""
echo "[6/9] Mise a jour de pip..."
pip install --upgrade pip setuptools wheel

# Installer PyTorch (CPU version - optimisé pour 20GB RAM)
echo ""
echo "[7/9] Installation de PyTorch (CPU)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Installer les dépendances ML (essentielles seulement)
echo ""
echo "[8/9] Installation des dependances ML..."
pip install \
    transformers>=4.35.0 \
    datasets>=2.14.0 \
    accelerate>=0.24.0 \
    peft>=0.6.0 \
    bitsandbytes>=0.41.0 \
    sentencepiece>=0.1.99 \
    tokenizers>=0.15.0 \
    streamlit>=1.28.0 \
    pandas>=2.0.0 \
    pyyaml>=6.0 \
    requests>=2.31.0 \
    beautifulsoup4>=4.12.0 \
    PyPDF2>=3.0.0 \
    pdfplumber>=0.10.0 \
    tqdm>=4.66.0

# Nettoyer le cache pip pour économiser l'espace
echo ""
echo "[9/9] Nettoyage du cache pip..."
pip cache purge

echo ""
echo "=========================================="
echo "Installation terminee !"
echo "=========================================="
echo ""
echo "Espace disque utilise:"
df -h /
echo ""
echo "Pour activer l'environnement:"
echo "  cd tchad-langues-ai"
echo "  source venv/bin/activate"
echo ""
echo "Pour verifier l'installation:"
echo "  python -c 'import torch; print(\"PyTorch:\", torch.__version__)'"
echo "  python -c 'import transformers; print(\"Transformers:\", transformers.__version__)'"
echo ""
echo "IMPORTANT: Surveille l'espace disque regulierement!"
echo "  df -h /"
echo ""

