# Run GateShop on GitHub (no local VM)

GateShop is PHP + MySQL, so it **cannot** run on GitHub Pages (static only).
It runs in **GitHub Codespaces** — GitHub's cloud — straight from this repo.

## Start it
1. On the repo page: **Code ▸ Codespaces ▸ Create codespace on main**.
2. Wait ~2–3 min. The container builds and runs `docker compose up` automatically.
3. A **Ports** tab appears with port **8080** → click the globe/Open-in-browser icon.
   That URL is your live GateShop.

## Share the link with the class
- In the **Ports** tab, right-click port 8080 ▸ **Port Visibility ▸ Public**.
- Copy the forwarded URL and share it. (Leave it **Private** if only you test.)

## Notes
- The URL lives only while the codespace is running. Stop the codespace to take it offline.
- Free Codespaces hours apply per GitHub account.
- This app is **intentionally vulnerable** — keep the port Private, or Public only to your class, never left open long-term.
- Admin password: set `ADMIN_PASSWORD` in `labs/gateshop/.env` inside the codespace, then `docker compose up -d --build` again.
