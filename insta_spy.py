import instaloader

# 1. Instagram Sessiyası yaradırıq
L = instaloader.Instaloader()

# DİQQƏT: GitHub-a qoyanda bura öz məlumatlarını yazma!
# Onları istifadəçidən giriş olaraq alacağıq.
USER = input("Username: ")
SESSION_ID = input("Session ID: ")

try:
    # Sessiya vasitəsilə giriş (Şifrə yazmadan, ban riskini azaldır)
    L.context._session.cookies.set("sessionid", SESSION_ID)
    print(f"[+] {USER} olaraq giriş edildi...")

    target_username = input("İzlənəcək dostun username-i: ")
    profile = instaloader.Profile.from_username(L.context, target_username)

    print(f"[*] @{target_username} analiz edilir. Bu bir az vaxt ala bilər...")

    # 2. Dostunun izlədiyi ortaq səhifələri skan edirik
    for followed in profile.get_followees():
        print(f"[SCANNING]: {followed.username} səhifəsi yoxlanılır...")
        
        # Həmin səhifənin son postlarını yoxlayırıq
        count = 0
        for post in followed.get_posts():
            if count > 5: break # Hər səhifədə son 5 postu yoxla (sürət üçün)
            
            # Postun altındakı rəylərdə dostunu axtarırıq
            for comment in post.get_comments():
                if comment.owner.username == target_username:
                    print(f"🔥 TAPILDI! @{target_username} bura rəy yazıb: {post.url}")
                    print(f"Mesaj: {comment.text}")
            count += 1

except Exception as e:
    print(f"[!] Xəta baş verdi: {e}")