# ☁️ GIF MAKER - BY @Nu4g3

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**Gif Maker** est un éditeur de GIF ultra-léger, moderne et performant. Conçu pour la rapidité et la simplicité, il permet de transformer, filtrer et exporter vos GIFs préférés en quelques clics sans avoir besoin de logiciels complexes ou d'outils en ligne lents.

---

### 🌟 Fonctionnalités Principales

L'application offre une suite complète d'outils pour personnaliser vos animations :

- **⚡ Aperçu en Temps Réel** : Visualisez instantanément chaque réglage directement dans l'interface avant de lancer l'exportation.
- **🎨 Contrôle de l'Image** :
  - **Luminosité & Contraste** : Ajustez la clarté de vos GIFs.
  - **Opacité** : Rendez vos GIFs transparents.
  - **Flou (Blur)** : Appliquez un effet de flou artistique ou correctif.
- **🎬 Gestion de l'Animation** :
  - **Vitesse de Lecture** : Accélérez ou ralentissez vos GIFs (de 10% à 500%).
  - **Mise à l'Échelle** : Changez la taille de l'aperçu pour mieux voir les détails.
- **🎭 Effets Spéciaux** :
  - **Mode Niveaux de Gris** : Un look noir et blanc classique.
  - **Effet Sépia** : Pour un style vintage et chaud.
  - **Inversion des Couleurs** : Pour des effets psychédéliques ou techniques.
- **📤 Exportation Haute Qualité** :
  - Choisissez votre résolution de sortie, du **144p** jusqu'à l'ultra-haute définition **4K**.
  - Barre de progression interactive pour suivre l'exportation en temps réel.
- **🌐 Expérience Utilisateur** :
  - **Système Multi-langue** : Entièrement traduit en **Français** et **Anglais**.
  - **Sauvegarde Locale intelligente** : Option pour archiver automatiquement vos GIFs importés dans un dossier dédié.
  - **Interface Sombre (Dark Mode)** : Un design élégant et reposant pour les yeux.

---

### 🚀 Guide d'Installation

Le projet est conçu pour être prêt à l'emploi en quelques secondes.

#### Option 1 : Installation Automatique (Recommandé)
Double-cliquez simplement sur le fichier `Install.cmd`. Ce script va :
1. Vérifier votre installation Python.
2. Installer toutes les dépendances nécessaires (`Pillow`).
3. Préparer l'environnement pour le premier lancement.

#### Option 2 : Installation Manuelle
Si vous préférez la ligne de commande :
1. Ouvrez un terminal dans le dossier du projet.
2. Installez la bibliothèque PIL (Pillow) :
   ```bash
   pip install Pillow
   ```
3. Lancez l'application :
   ```bash
   python menu.py
   ```

---

### 📖 Comment utiliser ?

1. **Importation** : Cliquez sur la zone centrale pour sélectionner votre fichier `.gif`.
2. **Configuration** : Au premier lancement, choisissez si vous souhaitez activer la sauvegarde locale des originaux.
3. **Édition** : Utilisez le menu latéral à droite pour ajuster vos réglages.
4. **Langue** : Changez de langue à tout moment dans la section "GÉNÉRAL".
5. **Exportation** : Choisissez votre résolution cible et cliquez sur "EXPORTER LE GIF". Votre création sera sauvegardée dans le dossier `Output Gif/`.

---

### 📂 Structure du Projet

```text
Gif Maker/
├── menu.py             # Le code source principal de l'application
├── requirements.txt    # Liste des dépendances (Pillow)
├── Install.cmd         # Script d'installation rapide
├── Assets/             # Ressources visuelles (icônes)
├── Output Gif/         # Dossier de destination des exports
├── Input Gif/          # Dossier d'archivage des originaux (optionnel)
└── Save/               # Sauvegarde de vos préférences (langue, local storage)
```

---

### 🛠️ Fiche Technique

- **Langage** : Python 3
- **Interface Graphique** : Tkinter avec un design "Custom UI"
- **Traitement d'Image** : PIL (Python Imaging Library / Pillow)
- **Multi-threading** : Utilisé pour l'exportation afin de ne pas bloquer l'interface.

---

### 💬 Support & Communauté

Un bug ? Une suggestion de fonctionnalité ? Ou juste besoin d'aide ?
Rejoignez-nous sur Discord pour échanger avec la communauté !

👉 **Lien du Serveur :** [https://discord.gg/RGv9YvH3Fq](https://discord.gg/RGv9YvH3Fq)

*Fait avec ❤️ par Nu4g3. Version 1.0 (22/04/2026)*


---

# ☁️ GIF MAKER - BY @Nu4g3 (English Version)

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**Gif Maker** is an ultra-lightweight, modern, and high-performance GIF editor. Designed for speed and simplicity, it allows you to transform, filter, and export your favorite GIFs in just a few clicks without the need for complex software or slow online tools.

---

### 🌟 Main Features

The application provides a full suite of tools to customize your animations:

- **⚡ Real-Time Preview**: Instantly see every adjustment directly in the interface before starting the export.
- **🎨 Image Control**:
  - **Brightness & Contrast**: Adjust the clarity of your GIFs.
  - **Opacity**: Make your GIFs transparent.
  - **Blur**: Apply artistic or corrective blur effects.
- **🎬 Animation Management**:
  - **Playback Speed**: Speed up or slow down your GIFs (from 10% to 500%).
  - **Preview Scale**: Change the preview size to better see the details.
- **🎭 Special Effects**:
  - **Grayscale Mode**: A classic black and white look.
  - **Sepia Effect**: For a warm, vintage style.
  - **Invert Colors**: For psychedelic or technical effects.
- **📤 High-Quality Export**:
  - Choose your output resolution, from **144p** up to ultra-high-definition **4K**.
  - Interactive progress bar to track the export in real-time.
- **🌐 User Experience**:
  - **Multi-language System**: Fully translated into **French** and **English**.
  - **Smart Local Storage**: Option to automatically archive your imported GIFs in a dedicated folder.
  - **Dark Mode**: A sleek and eye-friendly design.

---

### 🚀 Installation Guide

The project is designed to be ready to use in seconds.

#### Option 1: Automatic Installation (Recommended)
Simply double-click the `Install.cmd` file. This script will:
1. Check your Python installation.
2. Install all necessary dependencies (`Pillow`).
3. Prepare the environment for the first run.

#### Option 2: Manual Installation
If you prefer the command line:
1. Open a terminal in the project folder.
2. Install the PIL library (Pillow):
   ```bash
   pip install Pillow
   ```
3. Run the application:
   ```bash
   python menu.py
   ```

---

### 📖 How to use?

1. **Importing**: Click the center zone to select your `.gif` file.
2. **Configuration**: On the first launch, choose whether you want to enable local backup of the originals.
3. **Editing**: Use the side menu on the right to adjust your settings.
4. **Language**: Change the language at any time in the "GENERAL" section.
5. **Exporting**: Choose your target resolution and click "EXPORT GIF". Your creation will be saved in the `Output Gif/` folder.

---

### 📂 Project Structure

```text
Gif Maker/
├── menu.py             # Main application source code
├── requirements.txt    # Dependency list (Pillow)
├── Install.cmd         # Quick installation script
├── Assets/             # Visual resources (icons)
├── Output Gif/         # Destination folder for exports
├── Input Gif/          # Original archiving folder (optional)
└── Save/               # Preference storage (language, local storage)
```

---

### 🛠️ Technical Specifications

- **Language**: Python 3
- **GUI**: Tkinter with a "Custom UI" design
- **Image Processing**: PIL (Python Imaging Library / Pillow)
- **Multi-threading**: Used for export to ensure the UI remains responsive.

---

### 💬 Support & Community

Found a bug? Have a feature suggestion? Or just need help?
Join us on Discord to chat with the community!

👉 **Discord Link:** [https://discord.gg/RGv9YvH3Fq](https://discord.gg/RGv9YvH3Fq)

*Made with ❤️ by Nu4g3. Version 1.0 (2026-04-22)*
