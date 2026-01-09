# 🔧 Étendre la partition pour utiliser tout l'espace disque

## 🔍 Diagnostic

Tu as seulement **13 GB disponibles** alors que tu as augmenté le disque. Cela signifie que la partition n'a pas été étendue.

## 📋 Étape 1 : Vérifier la taille réelle du disque

```bash
# Voir la taille réelle du disque (pas juste la partition)
lsblk

# Ou
sudo fdisk -l
```

Cela va te montrer :
- La taille **réelle du disque** (devrait être 80-100 GB si tu l'as augmenté)
- La taille de la **partition actuelle** (probablement encore 40 GB)

## 📋 Étape 2 : Installer GParted

```bash
sudo apt update
sudo apt install gparted -y
```

## 📋 Étape 3 : Étendre la partition avec GParted

```bash
# Lancer GParted (nécessite sudo)
sudo gparted
```

Dans GParted :

1. **Sélectionne le disque** : `/dev/sda` (en haut à droite)
2. **Regarde la partition** : Tu devrais voir `/dev/sda1` ou `/dev/sda2` avec ~40 GB
3. **Sélectionne la partition** : Clic sur `/dev/sda1` (ou sda2)
4. **Redimensionner** : 
   - Clic droit → **"Redimensionner/Déplacer"**
   - OU bouton **"Redimensionner/Déplacer"** dans la barre d'outils
5. **Étendre** :
   - Dans la fenêtre, **étire la partition** vers la droite pour utiliser tout l'espace
   - OU entre la nouvelle taille (80 GB ou 100 GB)
   - Clique sur **"Redimensionner"**
6. **Appliquer** :
   - Clique sur le bouton **"Appliquer"** (icône ✓ verte en haut)
   - Confirme l'opération
   - **ATTENDS** que ça se termine (peut prendre quelques minutes)

## 📋 Étape 4 : Vérifier que ça a fonctionné

```bash
# Vérifier l'espace disponible maintenant
df -h /

# Tu devrais voir beaucoup plus d'espace disponible !
```

## 🔧 Alternative : Méthode en ligne de commande (si GParted ne fonctionne pas)

### Option A : Avec resize2fs (si la partition est déjà étendue)

```bash
# Voir les partitions
sudo fdisk -l

# Étendre le système de fichiers (remplace sda1 par ta partition)
sudo resize2fs /dev/sda1
```

### Option B : Étendre avec fdisk (si besoin de redimensionner la partition)

⚠️ **ATTENTION** : Cette méthode est plus risquée, fais une sauvegarde d'abord !

```bash
# Voir les partitions
sudo fdisk -l

# Lancer fdisk sur le disque
sudo fdisk /dev/sda

# Dans fdisk :
# 1. Tape 'd' (delete) pour supprimer la partition
# 2. Tape 'n' (new) pour créer une nouvelle partition
# 3. Tape 'p' (primary)
# 4. Appuie sur Entrée pour accepter les valeurs par défaut
# 5. Tape 'w' (write) pour sauvegarder

# Ensuite étendre le système de fichiers
sudo resize2fs /dev/sda1
```

## ✅ Vérification finale

Après avoir étendu la partition :

```bash
df -h /
```

Tu devrais voir :
- **Size** : 80G ou 100G (au lieu de 39G)
- **Avail** : 60-80 GB disponibles (au lieu de 13 GB)

## ⚠️ Important

- **Sauvegarde** tes données importantes avant
- **Ne ferme pas** GParted pendant l'opération
- **Attends** que l'opération se termine complètement

## 🎯 Une fois l'espace étendu

Tu pourras continuer l'installation normalement avec au moins 60-70 GB libres !

