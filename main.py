import sys
import time

try:
    import telnetlib
except ImportError:
    print("[!] Modul telnetlib3 diperlukan. Menginstall dependencies...")
    sys.exit(1)

def print_banner():
    print("=" * 50)
    print("      FIBERHOME_ADDWAN by.shiegiet      ")
    print("==================================================")

def main():
    print_banner()
    
    # Input MAC Address
    mac_input = input("\nMasukkan MAC Address Router: ").strip()
    if not mac_input:
        print("[!] MAC Address tidak boleh kosong.")
        return

    clean_mac = mac_input.replace(":", "").replace("-", "").strip()
    if len(clean_mac) < 6:
        print("[!] Error: MAC Address terlalu pendek (minimal 6 karakter).")
        return

    # Hitung password
    last_6_mac = clean_mac[-6:].upper()
    admin_password = f"Fh@{last_6_mac}"

    print("-" * 50)
    print(f"[*] MAC Dibersihkan : {clean_mac}")
    print(f"[*] 6 Karakter Akhir  : {last_6_mac}")
    print(f"[*] Password Admin    : {admin_password}")
    print("-" * 50)
    print("[*] Menghubungkan ke Telnet 192.168.1.1...")

    try:
        tn = telnetlib.Telnet("192.168.1.1", timeout=10)

        tn.read_until(b"login: ", timeout=5)
        tn.write(b"gpon\n")

        tn.read_until(b"Password: ", timeout=5)
        tn.write(admin_password.encode('ascii') + b"\n")

        time.sleep(1)
        tn.write(b"en\n")

        tn.read_until(b"Password: ", timeout=5)
        tn.write(admin_password.encode('ascii') + b"\n")

        time.sleep(1)
        tn.write(b"cd factorydir\n")
        time.sleep(1)
        tn.write(b"set factorymode enable\n")
        time.sleep(1)
        tn.write(b"load preconfig IDN_XL\n")
        time.sleep(2)
        tn.write(b"reset\n")

        print("\n[SUKSES] Seluruh perintah berhasil dikirim ke perangkat FiberHome!")
        tn.close()

    except Exception as e:
        print(f"\n[ERROR] Gagal terhubung atau eksekusi terputus: {str(e)}")

    input("\nTekan ENTER untuk keluar...")

if __name__ == "__main__":
    main()
