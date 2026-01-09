# 💾 Comment augmenter le stockage de la VM Kali dans VirtualBox

## ⚠️ IMPORTANT : Sauvegarde d'abord !

Avant de modifier le disque, **sauvegarde ta VM** ou au moins tes données importantes.

## 📋 Méthode 1 : Augmenter le disque existant (Recommandé)

### Étape 1 : Arrêter la VM
1. **Éteins complètement** la VM Kali (pas en veille, complètement éteinte)
2. Ferme VirtualBox si nécessaire

### Étape 2 : Ouvrir le gestionnaire de médias virtuels
1. Ouvre **VirtualBox**
2. Va dans le menu : **Fichier** → **Gestionnaire de médias virtuels** (ou `Ctrl+D`)
3. Tu verras la liste de tes disques virtuels

### Étape 3 : Augmenter la taille du disque
1. **Sélectionne** le disque `Kali.vdi` dans la liste
2. Clique sur **"Propriétés"** (icône d'engrenage) ou **clic droit** → **Propriétés**
3. Va dans l'onglet **"Détails"**
4. Clique sur **"Taille"** ou cherche l'option pour modifier la taille
5. **Augmente la taille** à **80 GB** ou **100 GB** (selon ton espace disque disponible)
6. Clique sur **"Appliquer"** ou **"OK"**

### Étape 4 : Redémarrer la VM et étendre la partition
Une fois le disque agrandi, tu dois **étendre la partition** dans Kali :

1. **Démarre la VM Kali**
2. Ouvre un terminal
3. Vérifie l'espace actuel :
```bash
df -h /
lsblk
```

4. Installe `gparted` (si pas déjà installé) :
```bash
sudo apt update
sudo apt install gparted -y
```

5. Lance GParted :
```bash
sudo gparted
```

6. Dans GParted :
   - Sélectionne la partition principale (généralement `/dev/sda1` ou `/dev/sda2`)
   - Clique sur **"Redimensionner/Déplacer"**
   - Étends la partition pour utiliser tout l'espace disponible
   - Clique sur **"Appliquer"** (icône ✓ verte)
   - Attends que l'opération se termine

7. Vérifie que ça a fonctionné :
```bash
df -h /
```

## 📋 Méthode 2 : Créer un disque additionnel (Alternative)

Si tu ne peux pas modifier le disque existant :

### Étape 1 : Créer un nouveau disque
1. Dans VirtualBox, sélectionne ta VM Kali
2. Va dans **Paramètres** → **Stockage**
3. Clique sur **"Contrôleur SATA"** → **"Ajouter un disque dur"**
4. Clique sur **"Créer un nouveau disque"**
5. Choisis **VDI** (VirtualBox Disk Image)
6. Choisis **"Allocation dynamique"**
7. Donne une taille de **40-60 GB**
8. Donne un nom : `Kali-Data.vdi`

### Étape 2 : Monter le disque dans Kali
1. Démarre la VM Kali
2. Ouvre un terminal
3. Vérifie le nouveau disque :
```bash
lsblk
```

4. Formate le disque :
```bash
sudo fdisk /dev/sdb  # (remplace sdb par le nom de ton nouveau disque)
# Dans fdisk : n (nouveau), p (primaire), Entrée, Entrée, w (écrire)
sudo mkfs.ext4 /dev/sdb1
```

5. Crée un point de montage et monte :
```bash
sudo mkdir /mnt/data
sudo mount /dev/sdb1 /mnt/data
```

6. Pour monter automatiquement au démarrage, ajoute dans `/etc/fstab` :
```bash
echo '/dev/sdb1 /mnt/data ext4 defaults 0 2' | sudo tee -a /etc/fstab
```

## 🎯 Recommandation

**Utilise la Méthode 1** (augmenter le disque existant) - c'est plus simple et tout est au même endroit.

## 📊 Taille recommandée

- **Minimum** : 80 GB (confortable pour l'entraînement)
- **Idéal** : 100 GB (marge pour plusieurs modèles et expérimentations)

## ⚠️ Précautions

1. **Sauvegarde** avant de modifier
2. **Éteins complètement** la VM (pas en veille)
3. **Vérifie l'espace disque** de ton PC hôte avant d'augmenter
4. **Ne supprime pas** le disque pendant l'opération

## 🔧 Commandes utiles pour vérifier

```bash
# Voir l'espace disque dans Kali
df -h /

# Voir les partitions
lsblk

# Voir la taille du disque
sudo fdisk -l
```

## 💡 Astuce

Si tu as des problèmes avec GParted, tu peux aussi utiliser la ligne de commande :

```bash
# Voir les partitions
sudo fdisk -l

# Étendre la partition (remplace sda2 par ta partition)
sudo resize2fs /dev/sda2
```

## ✅ Vérification finale

Après avoir augmenté le stockage, vérifie :

```bash
df -h /
```

Tu devrais voir plus d'espace disponible !

