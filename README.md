# Dokumentasi Tugas — Algoritma Backtracking
### N-Queens Problem

**Nama**  : Fardanu Fibri Alfarizi  
**NIM**   : 21120124110105  
**Kelas** : Algoritma Pemrograman D  
**Bahasa**: Python | **Visualisasi**: CLI

---

## 1. Deskripsi Masalah

N-Queens Problem adalah masalah klasik dalam ilmu komputer:
Tempatkan N bidak ratu pada papan catur N×N sedemikian rupa sehingga tidak ada dua ratu yang saling menyerang.

**Goal / Solusi Akhir:**
- Papan N×N terisi tepat N bidak ratu
- Semua N ratu berhasil diletakkan

**Batasan (Constraint):**
- Satu kolom tidak boleh berisi lebih dari satu ratu
- Satu baris tidak boleh berisi lebih dari satu ratu
- Diagonal tidak boleh berisi lebih dari satu ratu

---

## 2. Pseudocode

```
FUNCTION solve_n_queens(row, board, n):
  IF row == n THEN
    PRINT "Solusi ditemukan!"
    RETURN True
  END IF

  FOR col FROM 0 TO n-1 DO
    IF is_safe(board, row, col) THEN
      board[row] = col            // Tempatkan ratu
      VISUALIZE(place, row, col)

      IF solve_n_queens(row+1, board, n) THEN
        RETURN True               // Lanjut ke baris berikutnya
      END IF

      board[row] = -1             // Cabut ratu (backtrack)
      VISUALIZE(backtrack, row, col)
    ELSE
      VISUALIZE(conflict, row, col)
    END IF
  END FOR

  RETURN False   // Tidak ada kolom valid di baris ini
END FUNCTION

FUNCTION is_safe(board, row, col):
  FOR r FROM 0 TO row-1 DO
    IF board[r] == col THEN
      RETURN False                // Konflik kolom
    IF |board[r] - col| == |r - row| THEN
      RETURN False                // Konflik diagonal
  END FOR
  RETURN True
END FUNCTION
```

---

## 3. Flowchart

```
        [MULAI]
           |
           v
    [row == N ?]
    /          \
  YA           TIDAK
   |              |
[Solusi!]    [Loop col = 0..N-1]
[RETURN True]     |
                  v
          [is_safe(row, col)?]
          /                  \
        YA                   TIDAK
         |                     |
   [Tempatkan ratu]       [Skip, lanjut
   [rekursi row+1]         col berikut]
         |
   [Rekursi berhasil?]
   /              \
 YA               TIDAK
  |                  |
[RETURN True]   [Cabut ratu / Backtrack]
                [coba col berikutnya]
                     |
              [Semua col habis?]
                     |
               [RETURN False]
                     |
                  [SELESAI]
```

---

## 4. Struktur File

```
tugas alpro n_queens.py
├── main()              Entry point: input user, mulai program
├── solve_n_queens()    Wrapper: inisialisasi board, panggil backtrack
│   └── backtrack()     Fungsi rekursi inti (closure)
├── is_safe()           Validasi constraint (kolom & diagonal)
├── print_board()       Render papan ke terminal dengan warna ANSI
└── print_summary()     Tampilkan ringkasan hasil akhir
```

---

## 5. Penjelasan Kode

### `is_safe(board, row, col)`
Memeriksa apakah posisi `(row, col)` aman. Mengecek semua ratu di baris `0..(row-1)`:
- **Konflik kolom** : `board[r] == col`
- **Konflik diagonal** : `|board[r] - col| == |r - row|`

Pengecekan baris tidak perlu karena tiap rekursi hanya mengisi satu baris unik.

### `backtrack(row)`
Fungsi rekursif inti.
- **Base case** : `row == N` → solusi ditemukan
- Loop tiap kolom, cek `is_safe`, tempatkan ratu, rekursi ke `row+1`, jika gagal cabut dan coba kolom lain.

### `print_board()`
Menggunakan ANSI escape codes untuk warna terminal:

| Warna       | Arti                                  |
|-------------|---------------------------------------|
| Hijau tua   | Ratu baru berhasil ditempatkan        |
| Merah tua   | Konflik terdeteksi, posisi dilewati   |
| Oranye      | Backtrack, ratu dicabut               |
| Hijau cerah | Solusi lengkap ditemukan              |

---

## 6. Cara Menjalankan

```bash
tugas alpro n_queens.py
```

**Input yang diminta:**
1. **Nilai N** : ukuran papan (4–10, rekomendasi: 6)
2. **Kecepatan** : `1` = Lambat (0.7s) · `2` = Normal (0.35s) · `3` = Cepat (0.1s)

> **Rekomendasi:** Mulai dengan N=6, kecepatan Normal agar proses backtracking terlihat jelas tanpa terlalu lambat.

---

## 7. Contoh Output

```
  ╔══════════════════════════════════╗
  ║          RINGKASAN HASIL         ║
  ╚══════════════════════════════════╝

  ✔ Solusi ditemukan untuk 6-Queens!

  Penempatan ratu (baris → kolom):
    Baris 1  →  Kolom 2
    Baris 2  →  Kolom 4
    Baris 3  →  Kolom 6
    Baris 4  →  Kolom 1
    Baris 5  →  Kolom 3
    Baris 6  →  Kolom 5

  Total langkah (percobaan)  : 196
  Waktu eksekusi             : 44.872 detik

  Visualisasi Solusi:
    1 2 3 4 5 6
  ▪ ♛ ▪ ▫ ▪ ▫
  ▫ ▪ ▫ ♛ ▫ ▪
  ▪ ▫ ▪ ▫ ▪ ♛
  ♛ ▪ ▫ ▪ ▫ ▪
  ▪ ▫ ♛ ▫ ▪ ▫
  ▫ ▪ ▫ ▪ ♛ ▪
```

---

## 8. Analisis Kompleksitas

| Aspek                      | Keterangan                                              |
|----------------------------|---------------------------------------------------------|
| Worst case (tanpa pruning) | O(N!)                                                   |
| Dengan backtracking        | Jauh lebih kecil dari O(N!) karena cabang dipangkas     |
| Space complexity           | O(N) — array board 1 dimensi                            |
| Kedalaman rekursi maks     | O(N) — satu level per baris                             |

---

## 9. Referensi

- Slide kuliah: *Algoritma Backtracking* — Arseto Satriyo Nugroho
- GeeksforGeeks: N Queen Problem using Backtracking
- Cormen et al., *Introduction to Algorithms*, 3rd Edition
- Python ANSI Escape Codes: https://en.wikipedia.org/wiki/ANSI_escape_code
