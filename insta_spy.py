import instaloader
from getpass import getpass

# 1. Instagram Motorunu Hazırla
L = instaloader.Instaloader()

def start_tracking():
    # Giriş məlumatlarını alırıq
    user = input("[>] Instagram İstifadəçi Adınız: ")
    # getpass şifrəni yazanda ekranda görünməməsi üçündür (təhlükəsizlik)
    password = getpass("[>] Şifrəniz: ")

    try:
        # Birbaşa giriş cəhdi
        print(f"\n[*] @{user} hesabına bağlantı qurulur...")
        L.login(user, password) 
        print("[+] Giriş uğurludur!\n")

        target = input("[?] İzlənəcək hədəf profil: ")
        profile = instaloader.Profile.from_username(L.context, target)

        print(f"[*] @{target} analiz edilir... Səhifələrdəki rəylər axtarılır.")
        
        # 2. Hədəfin izlədiyi adamları yoxlayırıq
        for followee in profile.get_followees():
            print(f"[SCANNING]: {followee.username} səhifəsi yoxlanılır...")
            
            # Həmin səhifənin son postlarını skan edirik
            for post in followee.get_posts():
                # Hər səhifədə yalnız son 3 postu yoxla (Banlanmamaq üçün sürəti nizamlayırıq)
                for comment in post.get_comments():
                    if comment.owner.username == target:
                        print(f"\n🎯 TAPILDI!")
                        print(f"🔗 Post URL: https://www.instagram.com/p/{post.shortcode}/")
                        print(f"💬 Rəy: {comment.text}")
                        print("-" * 30)

    except instaloader.exceptions.BadCredentialsException:
        print("[!] XƏTA: İstifadəçi adı və ya şifrə yanlışdır.")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        print("[!] DİQQƏT: Hesabda 2FA (İki mərhələli doğrulama) aktivdir. Kodu daxil etməlisiniz.")
        # Bura 2FA üçün kod əlavə edilə bilər
    except Exception as e:
        print(f"[!] Gözlənilməz xəta: {e}")

if __name__ == "__main__":
    start_tracking()