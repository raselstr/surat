#!/bin/bash

# ==================================================
# FORMAT HDD SEAGATE 2TB KE FAT32
# Target : /dev/sdb5
# Model  : ST2000DM001-1ER164
# Label  : DATA HDD
# ==================================================

set -Eeuo pipefail

DISK="/dev/sdb"
PART="/dev/sdb5"
MODEL_EXPECTED="ST2000DM001-1ER164"
LABEL_EXPECTED="DATA HDD"

info() { echo "[INFO] $*"; }
fail() { echo "[GAGAL] $*" >&2; exit 1; }

# Hak administrator otomatis
if [ "$(id -u)" -ne 0 ]; then
    SCRIPT_PATH="$(readlink -f "$0")"
    exec sudo bash "$SCRIPT_PATH"
fi

clear
echo "=========================================="
echo "       FORMAT HDD SEAGATE 2TB FAT32"
echo "=========================================="
echo

# Identifikasi HDD
[ -b "$DISK" ] || fail "Disk /dev/sdb tidak ditemukan."
[ -b "$PART" ] || fail "Partisi /dev/sdb5 tidak ditemukan."

MODEL=$(lsblk -dn -o MODEL "$DISK" | xargs)
SIZE=$(lsblk -bdn -o SIZE "$DISK" | xargs)
PARENT=$(lsblk -dn -o PKNAME "$PART" | xargs)
TYPE=$(blkid -s TYPE -o value "$PART" || true)
OLD_LABEL=$(blkid -s LABEL -o value "$PART" || true)

echo "Model       : $MODEL"
echo "Kapasitas   : $SIZE bytes"
echo "Partisi     : $PART"
echo "Filesystem  : $TYPE"
echo "Label       : $OLD_LABEL"
echo

# Validasi
[ "$MODEL" = "$MODEL_EXPECTED" ] || fail "Model HDD tidak sesuai."
[ "$PARENT" = "sdb" ] || fail "Partisi bukan bagian dari /dev/sdb."
[ "$SIZE" -ge 1900000000000 ] &&
[ "$SIZE" -le 2100000000000 ] || fail "Kapasitas tidak sesuai."
[ "$TYPE" = "ntfs" ] || fail "Filesystem bukan NTFS."
[ "$OLD_LABEL" = "$LABEL_EXPECTED" ] || fail "Label HDD tidak sesuai."

ROOT_SOURCE=$(findmnt -n -o SOURCE /)
ROOT_DISK=$(lsblk -sno PKNAME "$ROOT_SOURCE" 2>/dev/null | tail -n 1 || true)
[ "$ROOT_DISK" != "sdb" ] || fail "HDD terdeteksi sebagai disk sistem."

echo "Informasi partisi:"
lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINTS "$DISK"

echo
echo "PERHATIAN: SELURUH DATA /dev/sdb5 AKAN DIHAPUS."
echo "Tabel partisi dan partisi lain tidak diubah."
echo

read -r -p "Ketik FORMAT-SDB untuk melanjutkan: " JAWABAN
[ "$JAWABAN" = "FORMAT-SDB" ] || fail "Proses dibatalkan."

# Pastikan utilitas FAT32 tersedia
if ! command -v mkfs.fat >/dev/null 2>&1; then
    info "Menginstal dosfstools..."
    apt-get update
    apt-get install -y dosfstools
fi

# Lepaskan mount menggunakan perangkat langsung
info "Memeriksa status mount..."

if findmnt -rn -S "$PART" >/dev/null 2>&1; then
    info "Melepaskan partisi $PART..."
    umount "$PART" || fail "Gagal melepas partisi. Tutup aplikasi yang menggunakan HDD."
fi

# Pastikan sudah tidak ter-mount
if findmnt -rn -S "$PART" >/dev/null 2>&1; then
    fail "Partisi masih digunakan."
fi

sync

# Format
info "Memulai format FAT32..."
mkfs.fat -F 32 -n "$LABEL_EXPECTED" "$PART"

sync
udevadm settle

# Verifikasi
NEW_TYPE=$(blkid -s TYPE -o value "$PART")
NEW_LABEL=$(blkid -s LABEL -o value "$PART")

[ "$NEW_TYPE" = "vfat" ] || fail "Filesystem bukan FAT32."
[ "$NEW_LABEL" = "$LABEL_EXPECTED" ] || fail "Label tidak sesuai."

echo
echo "=========================================="
echo "          FORMAT BERHASIL"
echo "=========================================="
echo "Disk       : $DISK"
echo "Partisi    : $PART"
echo "Filesystem : FAT32"
echo "Label      : $NEW_LABEL"
echo "=========================================="

lsblk -f "$DISK"
