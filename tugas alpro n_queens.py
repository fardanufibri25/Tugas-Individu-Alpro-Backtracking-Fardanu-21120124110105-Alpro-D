import time
import os

# ANSI color codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GRAY   = "\033[90m"
WHITE  = "\033[97m"
BG_DARK = "\033[48;5;235m"
BG_LIGHT = "\033[48;5;238m"
BG_QUEEN = "\033[48;5;22m"
BG_ATTACK = "\033[48;5;52m"
BG_TRY   = "\033[48;5;17m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_board(board, n, current_row=None, current_col=None,
                mode="place", step_info="", step_num=0):
    """
    Render the board with colors to the terminal.
    mode: 'place'   = placing a queen (green highlight)
          'attack'  = conflict detected (red highlight)
          'backtrack' = removing a queen (yellow highlight)
          'done'   = final solution (all green)
    """
    clear()
    # Header
    print(f"\n{BOLD}{CYAN}  ╔══════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}  ║   N-QUEENS BACKTRACKING SOLVER   ║{RESET}")
    print(f"{BOLD}{CYAN}  ╚══════════════════════════════════╝{RESET}")
    print(f"  {GRAY}Papan: {WHITE}{n}x{n}{RESET}   "
          f"{GRAY}Langkah: {WHITE}{step_num}{RESET}\n")

    # Column labels
    print("     " + "  ".join(f"{GRAY}{c+1}{RESET}" for c in range(n)))
    print(f"   {GRAY}┌" + "───" * n + "┐" + RESET)

    for r in range(n):
        print(f"  {GRAY}{r+1} │{RESET}", end="")
        for c in range(n):
            # Determine cell background (checkerboard)
            dark = (r + c) % 2 == 0
            bg   = BG_DARK if dark else BG_LIGHT

            # Override background based on state
            if r == current_row and c == current_col:
                if mode == "place":
                    bg = BG_QUEEN
                elif mode == "attack":
                    bg = BG_ATTACK
                elif mode == "backtrack":
                    bg = "\033[48;5;130m"
                elif mode == "done":
                    bg = BG_QUEEN

            if board[r] == c and r != current_row:
                if mode == "done":
                    bg = BG_QUEEN
                else:
                    bg = "\033[48;5;28m"

            # Cell content
            if board[r] == c:
                icon = f"{WHITE} ♛ {RESET}"
            else:
                icon = f"   {RESET}"

            print(f"{bg}{icon}", end="")

        print(f"{GRAY}│{RESET}")

    print(f"   {GRAY}└" + "───" * n + "┘" + RESET)

    # Legend
    print(f"\n  {BG_QUEEN}   {RESET} Ratu ditempatkan   "
          f"{BG_ATTACK}   {RESET} Konflik   "
          f"\033[48;5;28m   {RESET} Ratu sebelumnya\n")

    # Status message
    if mode == "place":
        print(f"  {GREEN}▶ {step_info}{RESET}")
    elif mode == "attack":
        print(f"  {RED}✗ {step_info}{RESET}")
    elif mode == "backtrack":
        print(f"  {YELLOW}↩ {step_info}{RESET}")
    elif mode == "done":
        print(f"  {BOLD}{GREEN}✔ {step_info}{RESET}")
    else:
        print(f"  {GRAY}{step_info}{RESET}")


def is_safe(board, row, col):
    """
    Cek apakah posisi (row, col) aman untuk menempatkan ratu.
    Periksa kolom, diagonal kiri-atas, dan diagonal kanan-atas.
    """
    for r in range(row):
        placed_col = board[r]
        if placed_col == col:                        # Konflik kolom
            return False
        if abs(placed_col - col) == abs(r - row):   # Konflik diagonal
            return False
    return True


def solve_n_queens(n, delay=0.4):
    """
    Selesaikan N-Queens dengan backtracking.
    Tampilkan setiap langkah secara visual di terminal.
    """
    board = [-1] * n   # board[row] = kolom tempat ratu di baris tersebut
    solutions = []
    steps = [0]

    def backtrack(row):
        if row == n:
            # Solusi ditemukan
            solutions.append(board[:])
            print_board(board, n, mode="done",
                        step_info=f"SOLUSI #{len(solutions)} DITEMUKAN! "
                                  f"Semua {n} ratu berhasil ditempatkan.",
                        step_num=steps[0])
            time.sleep(delay * 2)
            return True   # Hentikan setelah solusi pertama

        for col in range(n):
            steps[0] += 1

            if is_safe(board, row, col):
                # Tempatkan ratu
                board[row] = col
                print_board(board, n, current_row=row, current_col=col,
                            mode="place",
                            step_info=f"Baris {row+1}: Coba kolom {col+1} → AMAN, "
                                      f"ratu ditempatkan",
                            step_num=steps[0])
                time.sleep(delay)

                # Rekursi ke baris berikutnya
                if backtrack(row + 1):
                    return True

                # Backtrack: cabut ratu
                steps[0] += 1
                print_board(board, n, current_row=row, current_col=col,
                            mode="backtrack",
                            step_info=f"Baris {row+1}: Tidak ada solusi dari kolom "
                                      f"{col+1} → Backtrack, coba kolom lain",
                            step_num=steps[0])
                time.sleep(delay * 0.7)
                board[row] = -1

            else:
                # Konflik terdeteksi
                board[row] = col
                print_board(board, n, current_row=row, current_col=col,
                            mode="attack",
                            step_info=f"Baris {row+1}: Kolom {col+1} → KONFLIK "
                                      f"(diserang ratu lain), lewati",
                            step_num=steps[0])
                time.sleep(delay * 0.5)
                board[row] = -1

        return False

    backtrack(0)
    return solutions, steps[0]


def print_summary(solutions, n, total_steps, elapsed):
    """Tampilkan ringkasan hasil setelah animasi selesai."""
    clear()
    print(f"\n{BOLD}{CYAN}  ╔══════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}  ║          RINGKASAN HASIL         ║{RESET}")
    print(f"{BOLD}{CYAN}  ╚══════════════════════════════════╝{RESET}\n")

    if solutions:
        sol = solutions[0]
        print(f"  {GREEN}✔ Solusi ditemukan untuk {n}-Queens!{RESET}\n")
        print(f"  {GRAY}Penempatan ratu (baris → kolom):{RESET}")
        for r, c in enumerate(sol):
            print(f"    Baris {r+1}  →  Kolom {c+1}")

        print(f"\n  {GRAY}Total langkah (percobaan)  : {WHITE}{total_steps}{RESET}")
        print(f"  {GRAY}Waktu eksekusi             : {WHITE}{elapsed:.3f} detik{RESET}\n")

        # Mini board representation
        print(f"  {BOLD}Visualisasi Solusi:{RESET}")
        header = "  " + " ".join(str(c+1) for c in range(n))
        print(f"  {GRAY}{header}{RESET}")
        for r in range(n):
            row_str = ""
            for c in range(n):
                if sol[r] == c:
                    row_str += f"{GREEN}♛{RESET} "
                else:
                    dark = (r + c) % 2 == 0
                    row_str += (f"{GRAY}▪{RESET} " if dark else f"{WHITE}▫{RESET} ")
            print(f"  {row_str}")
    else:
        print(f"  {RED}✗ Tidak ada solusi untuk {n}-Queens.{RESET}")

    print()


def main():
    clear()
    print(f"\n{BOLD}{CYAN}  ╔══════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}  ║   N-QUEENS BACKTRACKING SOLVER   ║{RESET}")
    print(f"{BOLD}{CYAN}  ╚══════════════════════════════════╝{RESET}\n")

    print(f"  {GRAY}Masalah N-Queens:{RESET}")
    print(f"  Tempatkan N ratu pada papan NxN agar tidak ada")
    print(f"  dua ratu yang saling menyerang.\n")

    # Input N
    while True:
        try:
            n = int(input(f"  {YELLOW}Masukkan nilai N (4-10, rekomendasi 6): {RESET}"))
            if 4 <= n <= 10:
                break
            print(f"  {RED}Nilai N harus antara 4 dan 10.{RESET}")
        except ValueError:
            print(f"  {RED}Input tidak valid.{RESET}")

    # Input kecepatan
    print(f"\n  {YELLOW}Pilih kecepatan animasi:{RESET}")
    print("  1. Lambat  (0.7 detik/langkah) – mudah diikuti")
    print("  2. Normal  (0.35 detik/langkah)")
    print("  3. Cepat   (0.1 detik/langkah)")
    speed_map = {"1": 0.7, "2": 0.35, "3": 0.1}
    speed_input = input(f"\n  {YELLOW}Pilih (1/2/3) [default=2]: {RESET}").strip()
    delay = speed_map.get(speed_input, 0.35)

    input(f"\n  {GREEN}Tekan ENTER untuk mulai animasi...{RESET}")

    start = time.time()
    solutions, total_steps = solve_n_queens(n, delay=delay)
    elapsed = time.time() - start

    time.sleep(1)
    print_summary(solutions, n, total_steps, elapsed)
    input(f"  {GRAY}Tekan ENTER untuk keluar...{RESET}")


if __name__ == "__main__":
    main()
