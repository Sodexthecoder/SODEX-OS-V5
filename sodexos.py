import customtkinter as ctk
from rembg import remove
from PIL import Image, ImageOps, ImageFilter
import psutil
import speedtest
import threading
import os
import shutil
import base64
from tkinter import filedialog, messagebox

# --- SODEX GLOBAL V5: THE ARCHITECT ---
VERSION = "5.0.1-Stable"
DEVELOPER = "Sodex"
def show_about(self):
    about_window = ctk.CTkToplevel(self)
    about_window.title("ABOUT SODEX OS")
    about_window.geometry("400x300")
    about_window.attributes("-topmost", True)  # Hep üstte kalsın

    ctk.CTkLabel(about_window, text="SODEX OS GLOBAL", font=("Impact", 30), text_color="#00D4FF").pack(pady=20)
    ctk.CTkLabel(about_window, text="Version 5.0 - Professional Suite", font=("Arial", 14)).pack()

    # SENİN İMZAN BURASI
    ctk.CTkLabel(about_window, text="Developed by: SODEX", font=("Arial", 16, "bold"), text_color="#00FF41").pack(
        pady=20)

    ctk.CTkLabel(about_window, text="© 2026 All Rights Reserved", font=("Arial", 10), text_color="gray").pack(
        side="bottom", pady=10)

LANGUAGES = {
    "English": {"dash": "Dashboard", "ai": "AI Tools", "org": "Organizer", "vault": "Vault", "speed": "Speed Test",
                "set": "Settings", "theme": "Appearance", "lang": "Language", "run": "Start Process",
                "sel": "Select File", "cpu": "CPU Usage", "ram": "RAM Usage", "dl": "Download", "ul": "Upload"},
    "Turkish": {"dash": "Panel", "ai": "AI Araçları", "org": "Düzenleyici", "vault": "Kasa", "speed": "Hız Testi",
                "set": "Ayarlar", "theme": "Görünüm", "lang": "Dil", "run": "İşlemi Başlat", "sel": "Dosya Seç",
                "cpu": "İşlemci", "ram": "Bellek", "dl": "İndirme", "ul": "Yükleme"},
    "Spanish": {"dash": "Tablero", "ai": "Herramientas AI", "org": "Organizador", "vault": "Bóveda",
                "speed": "Velocidad", "set": "Ajustes", "theme": "Apariencia", "lang": "Idioma", "run": "Iniciar",
                "sel": "Seleccionar", "cpu": "CPU", "ram": "RAM", "dl": "Descarga", "ul": "Subida"},
    "German": {"dash": "Übersicht", "ai": "KI-Tools", "org": "Organizer", "vault": "Tresor", "speed": "Speedtest",
               "set": "Einst.", "theme": "Design", "lang": "Sprache", "run": "Starten", "sel": "Wählen", "cpu": "CPU",
               "ram": "RAM", "dl": "Download", "ul": "Upload"},
    "French": {"dash": "Tableau", "ai": "Outils IA", "org": "Organisateur", "vault": "Coffre", "speed": "Vitesse",
               "set": "Réglages", "theme": "Apparence", "lang": "Langue", "run": "Démarrer", "sel": "Choisir",
               "cpu": "CPU", "ram": "RAM", "dl": "Téléchargement", "ul": "Téléchargement"},
    "Italian": {"dash": "Pannello", "ai": "Strumenti AI", "org": "Organizer", "vault": "Cassaforte",
                "speed": "Velocità", "set": "Impostazioni", "theme": "Aspetto", "lang": "Lingua", "run": "Avvia",
                "sel": "Seleziona", "cpu": "CPU", "ram": "RAM", "dl": "Download", "ul": "Upload"},
    "Russian": {"dash": "Панель", "ai": "AI Инструменты", "org": "Организатор", "vault": "Сейф", "speed": "Скорость",
                "set": "Настройки", "theme": "Вид", "lang": "Язык", "run": "Запуск", "sel": "Выбрать", "cpu": "ЦП",
                "ram": "ОЗУ", "dl": "Загрузка", "ul": "Отдача"},
    "Portuguese": {"dash": "Painel", "ai": "IA Ferramentas", "org": "Organizador", "vault": "Cofre",
                   "speed": "Velocidade", "set": "Config.", "theme": "Aparência", "lang": "Idioma", "run": "Iniciar",
                   "sel": "Selecionar", "cpu": "CPU", "ram": "RAM", "dl": "Download", "ul": "Upload"},
    "Japanese": {"dash": "ダッシュボード", "ai": "AIツール", "org": "整理機", "vault": "金庫", "speed": "速度テスト",
                 "set": "設定", "theme": "外観", "lang": "言語", "run": "開始", "sel": "選択", "cpu": "CPU使用率",
                 "ram": "メモリ使用率", "dl": "ダウンロード", "ul": "アップロード"},
    "Chinese": {"dash": "仪表板", "ai": "人工智能", "org": "整理器", "vault": "保险库", "speed": "速度测试",
                "set": "设置", "theme": "外观", "lang": "语言", "run": "开始", "sel": "选择文件", "cpu": "CPU占用",
                "ram": "内存占用", "dl": "下载", "ul": "上传"}
}


class SodexGlobalV5(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"SODEX OS V5 - {VERSION}")
        self.geometry("1100x750")

        # State
        self.cur_lang = "English"
        self.cur_file = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()

    def t(self, key):
        return LANGUAGES[self.cur_lang].get(key, key)

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="SODEX", font=("Impact", 35)).pack(pady=30)

        self.menu_btns = {}
        for m in ["dash", "ai", "org", "vault", "speed", "set"]:
            btn = ctk.CTkButton(self.sidebar, text=self.t(m).upper(), fg_color="transparent",
                                anchor="w", height=45, command=lambda x=m: self.switch(x))
            btn.pack(fill="x", padx=10, pady=2)
            self.menu_btns[m] = btn

        # Main Content
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.switch("dash")

    def switch(self, mode):
        for w in self.container.winfo_children(): w.destroy()
        getattr(self, f"view_{mode}")()

    # --- VIEWS ---
    def view_dash(self):
        ctk.CTkLabel(self.container, text=self.t("dash"), font=("Arial", 30, "bold")).pack(pady=20)
        self.cpu_bar = self.create_stat(self.t("cpu"))
        self.ram_bar = self.create_stat(self.t("ram"))
        self.update_mon()

    def create_stat(self, txt):
        f = ctk.CTkFrame(self.container)
        f.pack(fill="x", pady=10, padx=20)
        l = ctk.CTkLabel(f, text=f"{txt}: 0%", font=("Consolas", 18))
        l.pack(side="left", padx=20, pady=10)
        b = ctk.CTkProgressBar(f, width=300)
        b.set(0)
        b.pack(side="right", padx=20)
        return (l, b)

    def update_mon(self):
        try:
            c, r = psutil.cpu_percent(), psutil.virtual_memory().percent
            self.cpu_bar[0].configure(text=f"CPU: {c}%")
            self.cpu_bar[1].set(c / 100)
            self.ram_bar[0].configure(text=f"RAM: {r}%")
            self.ram_bar[1].set(r / 100)
            self.after(1000, self.update_mon)
        except:
            pass

    def view_ai(self):
        ctk.CTkLabel(self.container, text=self.t("ai"), font=("Arial", 25)).pack(pady=10)
        ctk.CTkButton(self.container, text=self.t("sel"), command=self.pick).pack(pady=10)
        self.ai_status = ctk.CTkLabel(self.container, text="...")
        self.ai_status.pack()
        ctk.CTkButton(self.container, text="BG REMOVE", command=lambda: self.ai_do("bg")).pack(pady=5)
        ctk.CTkButton(self.container, text="HD ENHANCE", command=lambda: self.ai_do("hd")).pack(pady=5)

    def pick(self):
        self.cur_file = filedialog.askopenfilename()
        if self.cur_file: self.ai_status.configure(text=os.path.basename(self.cur_file))

    def ai_do(self, m):
        if not self.cur_file: return
        threading.Thread(target=self.ai_engine, args=(m,), daemon=True).start()

    def ai_engine(self, m):
        try:
            self.after(0, lambda: self.ai_status.configure(text="PROCESSING..."))
            img = Image.open(self.cur_file)
            out = os.path.splitext(self.cur_file)[0] + f"_SODEX_{m}.png"
            if m == "bg":
                with open(self.cur_file, 'rb') as i:
                    res = remove(i.read())
                with open(out, 'wb') as o:
                    o.write(res)
            elif m == "hd":
                img.resize((img.size[0] * 2, img.size[1] * 2), Image.LANCZOS).save(out)
            messagebox.showinfo("SODEX", f"Saved: {out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_speed(self):
        ctk.CTkLabel(self.container, text=self.t("speed"), font=("Arial", 25)).pack(pady=20)
        self.sp_lbl = ctk.CTkLabel(self.container, text="0.00 Mbps", font=("Consolas", 40))
        self.sp_lbl.pack(pady=20)
        self.sp_btn = ctk.CTkButton(self.container, text=self.t("run"), command=self.run_sp)
        self.sp_btn.pack(pady=10)

    def run_sp(self):
        self.sp_btn.configure(state="disabled")
        threading.Thread(target=self.sp_engine, daemon=True).start()

    def sp_engine(self):
        try:
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            d = st.download() / 1e6
            self.after(0, lambda: self.sp_lbl.configure(text=f"{d:.2f} Mbps"))
        except:
            self.after(0, lambda: self.sp_lbl.configure(text="Error (403)"))
        finally:
            self.after(0, lambda: self.sp_btn.configure(state="normal"))

    def view_set(self):
        ctk.CTkLabel(self.container, text=self.t("set"), font=("Arial", 25)).pack(pady=20)

        # Theme
        ctk.CTkLabel(self.container, text=self.t("theme")).pack()
        ctk.CTkOptionMenu(self.container, values=["Dark", "Light"], command=ctk.set_appearance_mode).pack(pady=10)

        # Language
        ctk.CTkLabel(self.container, text=self.t("lang")).pack()
        self.lang_menu = ctk.CTkOptionMenu(self.container, values=list(LANGUAGES.keys()), command=self.change_lang)
        self.lang_menu.set(self.cur_lang)
        self.lang_menu.pack(pady=10)

    def change_lang(self, l):
        self.cur_lang = l
        self.setup_ui()  # UI'yı yeniden yükle

    def view_org(self):
        ctk.CTkButton(self.container, text=self.t("org"), height=100, command=self.run_org).pack(expand=True)

    def run_org(self):
        p = filedialog.askdirectory()
        if p:
            for f in os.listdir(p):
                ext = os.path.splitext(f)[1].lower()
                dest = "Images" if ext in ['.jpg', '.png'] else "Docs" if ext in ['.pdf', '.txt'] else "Others"
                os.makedirs(os.path.join(p, dest), exist_ok=True)
                shutil.move(os.path.join(p, f), os.path.join(p, dest, f))
            messagebox.showinfo("Done", "Organized!")

    def view_vault(self):
        ctk.CTkButton(self.container, text="ENCRYPT", fg_color="red", command=self.v_enc).pack(pady=20)
        ctk.CTkButton(self.container, text="DECRYPT", fg_color="green", command=self.v_dec).pack(pady=20)

    def v_enc(self):
        f = filedialog.askopenfilename()
        if f:
            with open(f, "rb") as r: d = base64.b64encode(r.read())
            with open(f + ".sodex", "wb") as w: w.write(d)
            os.remove(f)

    def v_dec(self):
        f = filedialog.askopenfilename(filetypes=[("Sodex", "*.sodex")])
        if f:
            with open(f, "rb") as r: d = base64.b64decode(r.read())
            with open(f.replace(".sodex", ""), "wb") as w: w.write(d)
            os.remove(f)


if __name__ == "__main__":
    app = SodexGlobalV5()
    app.mainloop()
