import sys
import os
import shutil
import configparser
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence, ImageEnhance, ImageFilter

class GifMakerApp:
    WINDOW_TITLE = "Gif Maker / @Nu4g3"
    DISCORD_LINK = "https://discord.gg/RGv9YvH3Fq"
    
    TRANSLATIONS = {
        'EN': {
            'title': 'GIF MAKER',
            'browse': 'CLICK TO BROWSE',
            'import': 'IMPORT ANOTHER',
            'ready': 'READY',
            'options': 'OPTIONS',
            'speed': 'PLAYBACK SPEED',
            'scale': 'PREVIEW SCALE',
            'opacity': 'OPACITY',
            'brightness': 'BRIGHTNESS',
            'contrast': 'CONTRAST',
            'blur': 'BLUR',
            'loop': 'LOOP ENABLED',
            'gray': 'GRAYSCALE MODE',
            'sepia': 'SEPIA EFFECT',
            'invert': 'INVERT COLORS',
            'res': 'EXPORT RESOLUTION',
            'export': 'EXPORT GIF',
            'exporting': 'EXPORTING...',
            'exported': 'EXPORTED TO',
            'failed': 'EXPORT FAILED',
            'lang': 'LANGUAGE',
            'general': 'GENERAL',
            'discord': 'JOIN DISCORD',
            'pref_msg': "Store GIFs locally in 'Input Gif' folder?",
            'pref_title': "Preference",
            'success_title': "Success",
            'success_msg': "GIF saved:",
        },
        'FR': {
            'title': 'GIF MAKER',
            'browse': 'CLIQUER POUR PARCOURIR',
            'import': 'IMPORTER UN AUTRE',
            'ready': 'PRÊT',
            'options': 'OPTIONS',
            'speed': 'VITESSE DE LECTURE',
            'scale': 'ÉCHELLE APERÇU',
            'opacity': 'OPACITÉ',
            'brightness': 'LUMINOSITÉ',
            'contrast': 'CONTRASTE',
            'blur': 'FLOU',
            'loop': 'BOUCLE ACTIVÉE',
            'gray': 'MODE GRIS',
            'sepia': 'EFFET SÉPIA',
            'invert': 'INVERSER COULEURS',
            'res': 'RÉSOLUTION EXPORT',
            'export': 'EXPORTER LE GIF',
            'exporting': 'EXPORTATION...',
            'exported': 'EXPORTÉ EN',
            'failed': 'ÉCHEC EXPORT',
            'lang': 'LANGUE',
            'general': 'GÉNÉRAL',
            'discord': 'REJOINDRE LE DISCORD',
            'pref_msg': "Stocker les GIFs localement dans le dossier 'Input Gif' ?",
            'pref_title': "Préférence",
            'success_title': "Succès",
            'success_msg': "GIF sauvegardé :",
        }
    }
    
    INITIAL_SIZE = "500x500"
    EXPANDED_SIZE = "800x500"
    
    BG_COLOR = "#000000"
    BG_ACCENT = "#050505"
    BG_CANVAS = "#030303"
    TEXT_COLOR = "#ffffff"
    TEXT_DIM = "#555555"
    TEXT_STATUS = "#333333"
    BORDER_COLOR = "#1a1a1a"

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_state()
        self.setup_styles()
        self.build_ui()
        self.root.after(100, self.load_configuration)

    def setup_window(self):
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(self.INITIAL_SIZE)
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        try:
            icon_path = Path(__file__).parent / "Assets" / "nuage.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass

    def initialize_state(self):
        self.app_dir = Path(__file__).parent
        self.config_path = self.app_dir / "Save" / "gif_maker_save.cfg"
        self.local_storage = False
        self.active_gif_path = None
        self.frames = []
        self.current_frame_idx = 0
        self.animation_process = None
        self.current_lang = 'EN'
        
        self.params = {
            'speed': 100,
            'scale': 1.0,
            'opacity': 1.0,
            'brightness': 1.0,
            'contrast': 1.0,
            'blur': 0,
            'loop': True,
            'grayscale': False,
            'sepia': False,
            'inverted': False
        }

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TScale", background=self.BG_ACCENT, troughcolor=self.BORDER_COLOR, bordercolor=self.BG_ACCENT)

    def build_ui(self):
        self.main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        self.main_container.pack(fill="both", expand=True)

        self.left_panel = tk.Frame(self.main_container, bg=self.BG_COLOR, width=500, height=500)
        self.left_panel.pack(side="left", fill="both", expand=True)
        self.left_panel.pack_propagate(False)

        self.main_title = tk.Label(
            self.left_panel, text=self.get_text('title'), bg=self.BG_COLOR, fg=self.TEXT_COLOR, 
            font=("Inter", 18, "bold"), pady=30
        )
        self.main_title.pack()

        self.content_stack = tk.Frame(self.left_panel, bg=self.BG_COLOR)
        self.content_stack.pack(expand=True)

        self.drop_zone = tk.Canvas(
            self.content_stack, width=380, height=280, bg=self.BG_CANVAS, 
            highlightthickness=1, highlightbackground=self.BORDER_COLOR, cursor="hand2"
        )
        self.drop_zone.pack()
        self.drop_zone.bind("<Button-1>", lambda _: self.on_browse_clicked())
        self.draw_drop_icon()
        
        self.drop_help_text = self.drop_zone.create_text(
            190, 200, text=self.get_text('browse'), fill="#444444", 
            font=("Inter", 9, "bold")
        )

        self.preview_view = tk.Frame(self.content_stack, bg=self.BG_COLOR)
        self.display_label = tk.Label(self.preview_view, bg=self.BG_CANVAS, bd=0)
        self.display_label.pack(padx=20, pady=10)
        
        self.import_btn = tk.Button(
            self.preview_view, text=self.get_text('import'), bg=self.BG_COLOR, fg=self.TEXT_DIM,
            activebackground=self.BG_COLOR, activeforeground=self.TEXT_COLOR, bd=1, relief="flat",
            font=("Inter", 8, "bold"), command=self.reset_application, cursor="hand2"
        )
        self.import_btn.pack(pady=5)

        self.status_bar = tk.Label(
            self.left_panel, text=self.get_text('ready'), bg=self.BG_COLOR, fg=self.TEXT_STATUS, 
            font=("Inter", 8, "bold")
        )
        self.status_bar.pack(side="bottom", pady=(5, 20))

        self.progress_indicator = ttk.Progressbar(
            self.left_panel, orient="horizontal", length=300, mode="determinate"
        )
        self.progress_indicator.pack(side="bottom", pady=5)
        self.progress_indicator.pack_forget()

        self.sidebar = tk.Frame(self.main_container, bg=self.BG_ACCENT, width=300)
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_forget()

        self.build_settings_sidebar()

    def get_text(self, key):
        return self.TRANSLATIONS[self.current_lang].get(key, key)

    def build_settings_sidebar(self):
        canvas = tk.Canvas(self.sidebar, bg=self.BG_ACCENT, highlightthickness=0, width=285)
        scrollbar = tk.Scrollbar(self.sidebar, orient="vertical", command=canvas.yview, bg=self.BG_ACCENT)
        
        self.settings_root = tk.Frame(canvas, bg=self.BG_ACCENT)
        self.settings_root.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.settings_root, anchor="nw", width=285)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # General Section
        self.create_section_label('general', is_key=True)
        
        lang_frame = tk.Frame(self.settings_root, bg=self.BG_ACCENT)
        lang_frame.pack(fill="x", padx=30, pady=5)
        
        tk.Label(lang_frame, text=self.get_text('lang'), bg=self.BG_ACCENT, fg="#888888", font=("Inter", 8, "bold")).pack(side="left")
        self.lang_var = tk.StringVar(value=self.current_lang)
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=['EN', 'FR'], state="readonly", width=5)
        self.lang_combo.pack(side="right")
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        tk.Button(
            self.settings_root, text=self.get_text('discord'), bg="#5865F2", fg=self.TEXT_COLOR,
            font=("Inter", 8, "bold"), bd=0, relief="flat", padx=10, pady=5,
            command=lambda: webbrowser.open(self.DISCORD_LINK)
        ).pack(fill="x", padx=30, pady=5)

        # Effects Section
        self.options_title = tk.Label(
            self.settings_root, text=self.get_text('options'), bg=self.BG_ACCENT, fg=self.TEXT_COLOR,
            font=("Inter", 11, "bold")
        )
        self.options_title.pack(anchor="w", padx=30, pady=(20, 10))

        self.scales = {}
        self.scales['speed'] = self.create_slider('speed', 10, 500, 'speed', 100)
        self.scales['scale'] = self.create_slider('scale', 50, 200, 'scale', 100, is_perc=True)
        self.scales['opacity'] = self.create_slider('opacity', 0, 100, 'opacity', 100, is_perc=True)
        self.scales['brightness'] = self.create_slider('brightness', 0, 200, 'brightness', 100, is_perc=True)
        self.scales['contrast'] = self.create_slider('contrast', 0, 200, 'contrast', 100, is_perc=True)
        self.scales['blur'] = self.create_slider('blur', 0, 10, 'blur', 0)

        self.toggles = {}
        self.toggles['loop'] = self.create_toggle('loop', 'loop', True)
        self.toggles['gray'] = self.create_toggle('gray', 'grayscale', False)
        self.toggles['sepia'] = self.create_toggle('sepia', 'sepia', False)
        self.toggles['invert'] = self.create_toggle('invert', 'inverted', False)

        self.res_label = self.create_section_label('res', is_key=True)
        self.resolution_choice = tk.StringVar(value="1080p (1920x1080)")
        self.res_box = ttk.Combobox(
            self.settings_root, textvariable=self.resolution_choice, state="readonly",
            values=["144p (256x144)", "360p (640x360)", "480p (854x480)", 
                    "720p (1280x720)", "1080p (1920x1080)", "1440p (2560x1440)", "4K (3840x2160)"]
        )
        self.res_box.pack(fill="x", padx=30, pady=5)

        tk.Frame(self.settings_root, bg=self.BG_ACCENT).pack(expand=True)

        self.export_btn = tk.Button(
            self.settings_root, text=self.get_text('export'), bg=self.TEXT_COLOR, fg=self.BG_COLOR,
            font=("Inter", 10, "bold"), bd=0, relief="flat", padx=20, pady=10,
            command=self.initiate_export
        )
        self.export_btn.pack(fill="x", padx=30, pady=(10, 40))

    def change_language(self, _=None):
        self.current_lang = self.lang_var.get()
        self.update_ui_text()

    def update_ui_text(self):
        self.main_title.configure(text=self.get_text('title'))
        self.drop_zone.itemconfig(self.drop_help_text, text=self.get_text('browse'))
        self.import_btn.configure(text=self.get_text('import'))
        self.status_bar.configure(text=self.get_text('ready'))
        self.options_title.configure(text=self.get_text('options'))
        self.export_btn.configure(text=self.get_text('export'))
        
        for key, (label_widget, scale_widget, label_key) in self.scales.items():
            label_widget.configure(text=self.get_text(label_key))
            
        for key, (cb_widget, label_key) in self.toggles.items():
            cb_widget.configure(text=self.get_text(label_key))

    def create_slider(self, label_key, min_val, max_val, param_key, default, is_perc=False):
        lbl = tk.Label(self.settings_root, text=self.get_text(label_key), bg=self.BG_ACCENT, fg=self.TEXT_DIM, font=("Inter", 8, "bold"))
        lbl.pack(anchor="w", padx=30, pady=(10, 0))
        
        def update_val(v):
            val = float(v)
            self.params[param_key] = val / 100.0 if is_perc else val
            self.update_status_msg(f"{self.get_text(label_key)}: {v}%" if is_perc else f"{self.get_text(label_key)}: {v}")

        s = tk.Scale(
            self.settings_root, from_=min_val, to=max_val, orient="horizontal",
            bg=self.BG_ACCENT, fg=self.TEXT_COLOR, highlightthickness=0, troughcolor=self.BORDER_COLOR,
            command=update_val, font=("Inter", 8)
        )
        s.set(default)
        s.pack(fill="x", padx=30, pady=5)
        return (lbl, s, label_key)

    def create_toggle(self, label_key, param_key, default):
        var = tk.BooleanVar(value=default)
        def on_toggle():
            self.params[param_key] = var.get()
            if param_key == 'loop' and self.params['loop']: self.animate_loop()
            self.update_status_msg(f"{self.get_text(label_key)}: {'ON' if self.params[param_key] else 'OFF'}")

        cb = tk.Checkbutton(
            self.settings_root, text=self.get_text(label_key), variable=var,
            bg=self.BG_ACCENT, fg="#888888", selectcolor=self.BG_COLOR, activebackground=self.BG_ACCENT,
            font=("Inter", 9, "bold"), command=on_toggle
        )
        cb.pack(anchor="w", padx=30, pady=5)
        return (cb, label_key)

    def create_section_label(self, text, is_key=False):
        t = self.get_text(text) if is_key else text
        lbl = tk.Label(self.settings_root, text=t, bg=self.BG_ACCENT, fg=self.TEXT_DIM, font=("Inter", 8, "bold"))
        lbl.pack(anchor="w", padx=30, pady=(10, 0))
        return lbl

    def draw_drop_icon(self):
        self.drop_zone.create_rectangle(160, 100, 220, 160, outline=self.TEXT_COLOR, width=2)
        self.drop_zone.create_line(190, 115, 190, 145, fill=self.TEXT_COLOR, width=2)
        self.drop_zone.create_line(180, 125, 190, 115, fill=self.TEXT_COLOR, width=2)
        self.drop_zone.create_line(200, 125, 190, 115, fill=self.TEXT_COLOR, width=2)

    def load_configuration(self):
        config = configparser.ConfigParser()
        if self.config_path.exists():
            config.read(self.config_path)
            if 'Settings' in config:
                self.local_storage = config.getboolean('Settings', 'local_storage', fallback=False)
                self.current_lang = config.get('Settings', 'language', fallback='EN')
                self.lang_var.set(self.current_lang)
                self.update_ui_text()
                return

        choice = messagebox.askyesno(self.get_text('pref_title'), self.get_text('pref_msg'))
        self.local_storage = choice
        self.save_config()

    def save_config(self):
        config = configparser.ConfigParser()
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        config['Settings'] = {
            'local_storage': str(self.local_storage),
            'language': self.current_lang
        }
        with open(self.config_path, 'w') as f:
            config.write(f)

    def on_browse_clicked(self):
        path = filedialog.askopenfilename(filetypes=[("GIF Files", "*.gif")])
        if path:
            self.process_selected_file(Path(path))

    def process_selected_file(self, file_path):
        self.active_gif_path = file_path
        display_path = file_path
        if self.local_storage:
            storage_dir = self.app_dir / "Input Gif"
            storage_dir.mkdir(exist_ok=True)
            target = storage_dir / file_path.name
            if file_path != target:
                try: shutil.copy2(file_path, target)
                except Exception: pass
            display_path = target

        self.load_gif_frames(display_path)
        self.drop_zone.pack_forget()
        self.preview_view.pack()
        self.sidebar.pack(side="right", fill="y")
        self.root.geometry(self.EXPANDED_SIZE)
        self.update_status_msg(f"LOADED: {file_path.name.upper()}", self.TEXT_COLOR)

    def load_gif_frames(self, path):
        if self.animation_process:
            self.root.after_cancel(self.animation_process)
        with Image.open(path) as img:
            self.frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(img)]
        self.current_frame_idx = 0
        self.animate_loop()

    def apply_visual_effects(self, img, export_res=None):
        work_img = img.copy()
        if export_res:
            work_img = work_img.resize(export_res, Image.Resampling.LANCZOS)
        else:
            w, h = work_img.size
            nw, nh = int(w * self.params['scale']), int(h * self.params['scale'])
            if nw > 400 or nh > 300:
                ratio = min(400/nw, 300/nh)
                nw, nh = int(nw * ratio), int(nh * ratio)
            work_img = work_img.resize((nw, nh), Image.Resampling.LANCZOS)

        if self.params['blur'] > 0:
            work_img = work_img.filter(ImageFilter.GaussianBlur(self.params['blur']))
        if self.params['brightness'] != 1.0:
            work_img = ImageEnhance.Brightness(work_img).enhance(self.params['brightness'])
        if self.params['contrast'] != 1.0:
            work_img = ImageEnhance.Contrast(work_img).enhance(self.params['contrast'])
        if self.params['grayscale']:
            work_img = work_img.convert("L").convert("RGBA")
        if self.params['sepia']:
            work_img = work_img.convert("L").convert("RGB").point(lambda x: x * 1.1 if x < 200 else 255).convert("RGBA")
        if self.params['inverted']:
            r, g, b, a = work_img.split()
            work_img = Image.merge("RGBA", (Image.eval(r, lambda x: 255-x), Image.eval(g, lambda x: 255-x), Image.eval(b, lambda x: 255-x), a))
        if self.params['opacity'] < 1.0:
            alpha = work_img.split()[3].point(lambda p: p * self.params['opacity'])
            work_img.putalpha(alpha)
        return work_img

    def animate_loop(self):
        if not self.frames: return
        processed = self.apply_visual_effects(self.frames[self.current_frame_idx])
        self.tk_photo = ImageTk.PhotoImage(processed)
        self.display_label.configure(image=self.tk_photo)
        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
        if self.current_frame_idx == 0 and not self.params['loop']: return
        delay = int(1000 / (10 * (self.params['speed'] / 100)))
        self.animation_process = self.root.after(max(10, delay), self.animate_loop)

    def initiate_export(self):
        if not self.active_gif_path: return
        save_dir = self.app_dir / "Output Gif"
        save_dir.mkdir(exist_ok=True)
        suggested_name = f"Nu4g3_{self.active_gif_path.stem}"
        target = filedialog.asksaveasfilename(
            initialdir=str(save_dir), initialfile=suggested_name, defaultextension=".gif",
            filetypes=[("GIF Files", "*.gif")], title="Export Result"
        )
        if target:
            threading.Thread(target=self.perform_export, args=(Path(target),), daemon=True).start()

    def perform_export(self, target_path):
        res_text = self.resolution_choice.get()
        res_map = {
            "144p": (256, 144), "360p": (640, 360), "480p": (854, 480),
            "720p": (1280, 720), "1080p": (1920, 1080), "1440p": (2560, 1440), "4K": (3840, 2160)
        }
        res_key = res_text.split(" ")[0]
        dimension = res_map.get(res_key, (1920, 1080))
        self.root.after(0, lambda: self.toggle_progress(True))
        self.safe_status_update(self.get_text('exporting'), "#ffff00")
        try:
            with Image.open(self.active_gif_path) as src:
                out_frames = []
                total = src.n_frames if hasattr(src, 'n_frames') else 1
                orig_duration = src.info.get('duration', 100)
                for i, frame in enumerate(ImageSequence.Iterator(src)):
                    processed = self.apply_visual_effects(frame.convert("RGBA"), export_res=dimension)
                    out_frames.append(processed)
                    progress = int(((i + 1) / total) * 100)
                    self.root.after(0, lambda p=progress: self.progress_indicator.configure(value=p))
                new_duration = int(orig_duration / (self.params['speed'] / 100.0))
                out_frames[0].save(
                    str(target_path), save_all=True, append_images=out_frames[1:], 
                    loop=0 if self.params['loop'] else 1, duration=max(10, new_duration)
                )
            self.safe_status_update(f"{self.get_text('exported')} {res_key}", "#00ff00")
            self.root.after(0, lambda: messagebox.showinfo(self.get_text('success_title'), f"{self.get_text('success_msg')} {target_path.name}"))
        except Exception as e:
            self.safe_status_update(self.get_text('failed'), "#ff0000")
            print(f"Error: {e}")
        finally:
            self.root.after(1000, lambda: self.toggle_progress(False))

    def toggle_progress(self, show):
        if show:
            self.progress_indicator.pack(side="bottom", pady=5)
            self.progress_indicator.configure(value=0)
        else:
            self.progress_indicator.pack_forget()

    def safe_status_update(self, text, color):
        self.root.after(0, lambda: self.update_status_msg(text, color))

    def reset_application(self):
        if self.animation_process: self.root.after_cancel(self.animation_process)
        self.preview_view.pack_forget()
        self.sidebar.pack_forget()
        self.drop_zone.pack()
        self.root.geometry(self.INITIAL_SIZE)
        self.update_status_msg(self.get_text('ready'), self.TEXT_STATUS)

    def update_status_msg(self, text, color=None):
        self.status_bar.configure(text=text)
        if color: self.status_bar.configure(fg=color)

if __name__ == "__main__":
    app_root = tk.Tk()
    GifMakerApp(app_root)
    app_root.mainloop()

# Version 1.0 ended = 22/04/2026 at 10:54 AM