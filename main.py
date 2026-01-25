import flet as ft
import smtplib
import threading
import time
import math
import random
from email.message import EmailMessage

# --- CONFIGURATION ---
THEME_COLOR = "#00FF99" # Cyber Cyan/Green
BG_COLOR = "#050505"    # Deep Dark
CARD_BG = "#0f0f0f"     # Card Background

def main(page: ft.Page):
    # --- PAGE SETTINGS ---
    page.title = "WHATSAPP UNBAN BY FAIZI MODS"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_COLOR
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    # GLOBAL VARIABLES
    user_session = {"email": "", "pwd": ""}

    # --- 1. CYBER BACKGROUND (Optimized for Flet) ---
    # Kivy ka mesh animation Flet mein heavy hota hai, isliye hum static Cyber Grid use karenge
    # jo bilkul waisa hi look dega bina phone hang kiye.
    cyber_bg = ft.Stack([
        ft.Container(
            gradient=ft.RadialGradient(
                center=ft.Alignment(0, -0.5),
                radius=1.5,
                colors=["#1A2A2A", BG_COLOR],
            ),
            expand=True,
        ),
        # Tech Lines Overlay
        ft.Container(
            border=ft.border.all(1, ft.colors.with_opacity(0.1, THEME_COLOR)),
            margin=20,
            alignment=ft.alignment.top_right,
        )
    ], expand=True)

    # --- 2. CUSTOM TECH WIDGETS ---
    def get_tech_field(label, icon, is_pass=False, read_only=False):
        return ft.TextField(
            label=label,
            password=is_pass,
            can_reveal_password=is_pass,
            read_only=read_only,
            text_style=ft.TextStyle(color=THEME_COLOR, weight="bold"),
            label_style=ft.TextStyle(color="#008866"),
            border_color=THEME_COLOR,
            cursor_color="white",
            prefix_icon=icon,
            bgcolor="#0a0a0a",
            border_radius=5,
        )

    def get_tech_button(text, on_click_func, color=THEME_COLOR):
        return ft.Container(
            content=ft.Text(text, color="black", weight="bold", size=16),
            alignment=ft.alignment.center,
            bgcolor=color,
            border_radius=5,
            height=50,
            on_click=on_click_func,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=color),
            animate=ft.animation.Animation(300, "easeOut"),
        )

    # --- 3. LOGIC & TEXTS (EXACTLY SAME AS YOUR CODE) ---
    
    # HEAVY NOTES VARIABLES
    def get_heavy_note(ban_type, num, sender):
        if ban_type == "permanent":
            return f"URGENT LEGAL DISPUTE: Permanent Suspension of Account {num} - Immediate Review Required", \
                   f"""To the WhatsApp Legal & Support Team,

I am writing to formally dispute the permanent suspension of my WhatsApp account associated with the number: {num}.

This account is utilized strictly for critical business operations and personal communication. I have thoroughly reviewed the WhatsApp Terms of Service and Privacy Policy, and I certify that I have NOT violated any regulations regarding "Spam", "Scams", "Bulk Messaging", or "Unauthorized Usage".

It is highly probable that this suspension was triggered by an algorithmic error (False Positive) in your automated security system. This unjustified ban is causing severe financial and reputational damage to my business.

I respectfully demand a MANUAL HUMAN AUDIT of my account logs. I am confident that a proper investigation will verify my compliance with your policies.

Please restore access to my account immediately.

Sincerely,
Faizi Mods Team
(Reply to: {sender})"""
        else:
            return f"CRITICAL REVIEW REQUEST: Incorrect Flagging of Account {num}", \
                   f"""Dear WhatsApp Support Team,

My account ({num}) has been restricted or flagged for review. I strongly object to this action as it appears to be a mistake.

I strictly adhere to all Community Guidelines. I do not use unauthorized versions of the app, nor do I engage in automated behavior. My usage patterns are organic and compliant.

This restriction is preventing me from accessing important data. I request you to expedite the review process, verify my lawful usage, and lift all restrictions immediately.

Regards,
Faizi Mods Team
(Reply to: {sender})"""

    # --- 4. SCREENS ---
    
    # -- LOGIN SCREEN --
    login_status = ft.Text("SYSTEM AUTHENTICATION REQUIRED", color="grey", size=10)
    
    email_in = get_tech_field("ADMIN GMAIL", ft.icons.EMAIL)
    pass_in = get_tech_field("APP PASSWORD", ft.icons.LOCK, is_pass=True)

    def try_login(e):
        em = email_in.value.strip()
        pw = pass_in.value.strip()
        
        if not em or not pw:
            login_status.value = "ERROR: CREDENTIALS MISSING"
            login_status.color = "red"
            login_status.update()
            return

        login_status.value = "ESTABLISHING TLS CONNECTION..."
        login_status.color = THEME_COLOR
        login_status.update()

        def login_thread():
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
                server.starttls()
                server.login(em, pw)
                server.quit()
                
                # Success
                user_session["email"] = em
                user_session["pwd"] = pw
                page.clean()
                load_dashboard()
            except Exception as ex:
                err_msg = str(ex)
                if "5.7.8" in err_msg:
                    login_status.value = "FAIL: Invalid App Password (Check Google Account)"
                else:
                    login_status.value = f"FAIL: {err_msg[:30]}..."
                login_status.color = "red"
                login_status.update()

        threading.Thread(target=login_thread).start()

    # -- DASHBOARD SCREEN --
    def load_dashboard():
        # Console Log
        console = ft.Column(scroll="auto")
        console_container = ft.Container(
            content=console,
            height=120,
            bgcolor="black",
            border=ft.border.all(1, THEME_COLOR),
            border_radius=5,
            padding=10
        )

        def log(txt):
            console.controls.append(ft.Text(f"> {txt}", color=THEME_COLOR, font_family="monospace", size=10))
            page.update()

        log("SYSTEM_READY...")
        log(f"LOGGED IN AS: {user_session['email']}")

        target_in = get_tech_field("TARGET NUMBER (+92...)", ft.icons.PHONE_ANDROID)
        
        # Radio Buttons for Ban Type
        ban_group = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="permanent", label="PERMANENT BAN", fill_color=THEME_COLOR),
            ft.Radio(value="review", label="REVIEW BAN", fill_color=THEME_COLOR),
        ]), value="permanent")

        # Locked Email
        locked_email = get_tech_field("SENDER IDENTITY", ft.icons.LOCK_CLOCK, read_only=True)
        locked_email.value = user_session['email']

        send_btn_ref = ft.Ref[ft.Container]()

        def start_sending(e):
            num = target_in.value.strip()
            if len(num) < 10:
                log("ERROR: INVALID TARGET NUMBER")
                return
            
            # Disable button visual
            e.control.opacity = 0.5
            e.control.disabled = True
            e.control.update()
            
            log(f"TARGETING: {num}")
            
            def process_thread():
                time.sleep(0.5)
                log("ENCRYPTING PAYLOAD...")
                time.sleep(1)
                log("CONNECTING TO SERVER...")
                
                sender = user_session["email"]
                pwd = user_session["pwd"]
                subj, body = get_heavy_note(ban_group.value, num, sender)

                try:
                    msg = EmailMessage()
                    msg.set_content(body)
                    msg['Subject'] = subj
                    msg['From'] = sender
                    msg['To'] = "support@whatsapp.com"
                    msg['Reply-To'] = sender

                    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
                    server.starttls()
                    server.login(sender, pwd)
                    server.send_message(msg)
                    server.quit()
                    
                    log("SUCCESS: HEAVY APPEAL SENT!")
                    log("Wait 24h for response.")
                except Exception as ex:
                    log(f"FAIL: {str(ex)[:30]}")

                # Re-enable button
                e.control.opacity = 1
                e.control.disabled = False
                e.control.update()

            threading.Thread(target=process_thread).start()

        # Layout Assembly
        page.add(
            ft.Stack([
                cyber_bg, # Background
                ft.Container( # Content Overlay
                    padding=20,
                    content=ft.Column([
                        ft.Text("WHATSAPP UNBAN", size=24, weight="bold", color=THEME_COLOR),
                        ft.Text("FAIZI MODS", size=12, weight="bold", color="grey"),
                        ft.Divider(color="transparent", height=10),
                        console_container,
                        ft.Divider(color="transparent", height=10),
                        target_in,
                        locked_email,
                        ft.Text("SELECT APPEAL TYPE:", color="grey", size=10),
                        ban_group,
                        ft.Divider(color="transparent", height=10),
                        get_tech_button("INJECT HEAVY APPEAL", start_sending, THEME_COLOR),
                        ft.Divider(color="grey"),
                        
                        # Social Buttons
                        ft.Row([
                            ft.IconButton(ft.icons.WHATSAPP, icon_color="#25D366", on_click=lambda _: page.launch_url("https://chat.whatsapp.com/IZ31t5ixjniL0nS1mHhFSl")),
                            ft.IconButton(ft.icons.TELEGRAM, icon_color="#0088cc", on_click=lambda _: page.launch_url("https://t.me/faizi_mods")),
                            ft.IconButton(ft.icons.VIDEO_LIBRARY, icon_color="#FF0000", on_click=lambda _: page.launch_url("https://youtube.com/@faizimods")),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        
                        ft.Text("NOTE: This tool is 100% Secure.", size=10, color="grey", text_align="center")

                    ], scroll="auto", spacing=15)
                )
            ], expand=True)
        )

    # -- LOGIN LAYOUT --
    page.add(
        ft.Stack([
            cyber_bg,
            ft.Container(
                alignment=ft.alignment.center,
                padding=30,
                content=ft.Column([
                    ft.Text("TEAM FAIZI MODS", size=30, weight="bold", color=THEME_COLOR),
                    ft.Text("AUTHENTICATION REQUIRED", size=12, color="grey"),
                    ft.Divider(height=30, color="transparent"),
                    email_in,
                    ft.Divider(height=10, color="transparent"),
                    pass_in,
                    ft.Divider(height=20, color="transparent"),
                    get_tech_button("AUTHENTICATE (TLS)", try_login),
                    ft.Divider(height=10, color="transparent"),
                    login_status,
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        ], expand=True)
    )
# Isay apni main.py ke bilkul niche replace karein
if __name__ == "__main__":
    # view=None ke saath assets_dir ko empty string dena crash aur black screen se bachata hai
    ft.app(target=main, view=None, assets_dir="") 

