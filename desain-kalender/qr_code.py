"""
Encoder QR Code murni Python (tanpa dependensi eksternal).

Dipakai untuk blok "SCAN ME" pada kalender. Mendukung versi 1-5,
ECC level L/M/Q/H (cukup untuk URL pendek), mode byte (UTF-8).
Algoritma mengikuti ISO/IEC 18004.
"""

from __future__ import annotations

_ECC_CW = {
    "L": {1: 7, 2: 10, 3: 15, 4: 20, 5: 26},
    "M": {1: 10, 2: 16, 3: 26, 4: 18, 5: 24},
    "Q": {1: 13, 2: 22, 3: 18, 4: 26, 5: 18},
    "H": {1: 17, 2: 28, 3: 22, 4: 16, 5: 22},
}

_NUM_BLOCK = {
    "L": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
    "M": {1: 1, 2: 1, 3: 1, 4: 2, 5: 2},
    "Q": {1: 1, 2: 1, 3: 2, 4: 2, 5: 4},
    "H": {1: 1, 2: 1, 3: 2, 4: 4, 5: 4},
}

_TOTAL_CW = {1: 26, 2: 44, 3: 70, 4: 100, 5: 134}
_ALIGN = {1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30]}
_ECL_BITS = {"L": 1, "M": 0, "Q": 3, "H": 2}


class _GF:
    """Aritmetika GF(256), polinomial primitif 0x11D."""

    EXP = [0] * 512
    LOG = [0] * 256
    _ready = False

    @classmethod
    def init(cls):
        x = 1
        for i in range(255):
            cls.EXP[i] = x
            cls.LOG[x] = i
            x <<= 1
            if x & 0x100:
                x ^= 0x11D
        for i in range(255, 512):
            cls.EXP[i] = cls.EXP[i - 255]
        cls._ready = True

    @classmethod
    def mul(cls, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return cls.EXP[cls.LOG[a] + cls.LOG[b]]


_GF.init()


def _rs_generator(degree: int):
    poly = [1]
    for i in range(degree):
        new = [0] * (len(poly) + 1)
        for j, coef in enumerate(poly):
            new[j] ^= coef
            new[j + 1] ^= _GF.mul(coef, _GF.EXP[i])
        poly = new
    return poly


def _rs_remainder(data, degree: int):
    gen = _rs_generator(degree)
    res = list(data) + [0] * degree
    for i in range(len(data)):
        coef = res[i]
        if coef:
            for j in range(1, len(gen)):
                res[i + j] ^= _GF.mul(gen[j], coef)
    return res[-degree:]


def _data_capacity(version: int, ecl: str) -> int:
    return _TOTAL_CW[version] - _ECC_CW[ecl][version]


def _encode_data(payload: bytes, version: int, ecl: str):
    cap = _data_capacity(version, ecl)
    bits = [0, 1, 0, 0]
    for i in range(7, -1, -1):
        bits.append((len(payload) >> i) & 1)
    for byte in payload:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    max_bits = cap * 8
    if len(bits) > max_bits:
        raise ValueError("Data terlalu panjang untuk versi/ECC ini")
    bits += [0] * min(4, max_bits - len(bits))
    while len(bits) % 8:
        bits.append(0)
    codewords = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    pad = [0xEC, 0x11]
    k = 0
    while len(codewords) < cap:
        codewords.append(pad[k % 2])
        k += 1
    return codewords


def _interleave(codewords, version: int, ecl: str):
    num_blocks = _NUM_BLOCK[ecl][version]
    ec_len = _ECC_CW[ecl][version]
    total_data = len(codewords)
    short_len, num_long = divmod(total_data, num_blocks)
    blocks, ec_blocks = [], []
    idx = 0
    for b in range(num_blocks):
        size = short_len + (1 if b >= num_blocks - num_long else 0)
        blk = codewords[idx:idx + size]
        idx += size
        blocks.append(blk)
        ec_blocks.append(_rs_remainder(blk, ec_len))
    out = []
    for i in range(max(len(b) for b in blocks)):
        for b in blocks:
            if i < len(b):
                out.append(b[i])
    for i in range(ec_len):
        for b in ec_blocks:
            out.append(b[i])
    return out


def _function_mask(version: int):
    size = version * 4 + 17
    fn = [[False] * size for _ in range(size)]

    def finder(row, col):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr, cc = row + r, col + c
                if 0 <= rr < size and 0 <= cc < size:
                    fn[rr][cc] = True

    finder(0, 0)
    finder(0, size - 7)
    finder(size - 7, 0)
    for i in range(size):
        fn[6][i] = True
        fn[i][6] = True
    pos = _ALIGN[version]
    for r in pos:
        for c in pos:
            if (r, c) in ((6, 6), (6, size - 7), (size - 7, 6)):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    fn[r + dr][c + dc] = True
    for i in range(9):
        fn[8][i] = True
        fn[i][8] = True
    for i in range(8):
        fn[8][size - 1 - i] = True
        fn[size - 1 - i][8] = True
    return fn


def _format_bits(ecl: str, mask: int) -> int:
    data = (_ECL_BITS[ecl] << 3) | mask
    rem = data
    for _ in range(10):
        rem = (rem << 1) ^ ((rem >> 9) * 0x537)
    return ((data << 10) | (rem & 0x3FF)) ^ 0x5412


def _mask_fn(mask: int, x: int, y: int) -> bool:
    return [
        (x + y) % 2 == 0,
        y % 2 == 0,
        x % 3 == 0,
        (x + y) % 3 == 0,
        (x // 3 + y // 2) % 2 == 0,
        (x * y) % 2 + (x * y) % 3 == 0,
        ((x * y) % 2 + (x * y) % 3) % 2 == 0,
        ((x + y) % 2 + (x * y) % 3) % 2 == 0,
    ][mask]


def _penalty(m):
    size = len(m)
    score = 0
    lines = list(m) + [[m[r][c] for r in range(size)] for c in range(size)]
    for line in lines:
        run, prev = 0, None
        for v in line:
            if v == prev:
                run += 1
            else:
                if run >= 5:
                    score += run - 2
                run, prev = 1, v
        if run >= 5:
            score += run - 2
    for r in range(size - 1):
        for c in range(size - 1):
            if m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1]:
                score += 3
    pat = [True, False, True, True, True, False, True]
    for line in lines:
        for i in range(size - 6):
            if line[i:i + 7] == pat:
                score += 40
    dark = sum(1 for row in m for v in row if v)
    ratio = dark * 100 // (size * size)
    score += abs(ratio - 50) // 5 * 10
    return score


def _draw_format(m, size: int, bits: int):
    def bit(i):
        return ((bits >> i) & 1) == 1

    for i in range(6):
        m[i][8] = bit(i)
    m[7][8] = bit(6)
    m[8][8] = bit(7)
    m[8][7] = bit(8)
    for i in range(9, 15):
        m[8][14 - i] = bit(i)
    for i in range(8):
        m[size - 1 - i][8] = bit(i)
    for i in range(8, 15):
        m[8][size - 15 + i] = bit(i)
    m[size - 8][8] = True


def encode(text: str, ecl: str = "M"):
    payload = text.encode("utf-8")
    version = None
    for v in range(1, 6):
        if len(payload) + 2 <= _data_capacity(v, ecl):
            version = v
            break
    if version is None:
        raise ValueError("Teks terlalu panjang (maks. versi 5)")
    codewords = _interleave(_encode_data(payload, version, ecl), version, ecl)

    size = version * 4 + 17
    fn = _function_mask(version)
    m = [[False] * size for _ in range(size)]

    def draw_finder(row, col):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr, cc = row + r, col + c
                if not (0 <= rr < size and 0 <= cc < size):
                    continue
                inside = 0 <= r <= 6 and 0 <= c <= 6
                ring = r in (0, 6) or c in (0, 6)
                core = 2 <= r <= 4 and 2 <= c <= 4
                m[rr][cc] = inside and (ring or core)

    draw_finder(0, 0)
    draw_finder(0, size - 7)
    draw_finder(size - 7, 0)
    for i in range(8, size - 8):
        m[6][i] = i % 2 == 0
        m[i][6] = i % 2 == 0
    pos = _ALIGN[version]
    for r in pos:
        for c in pos:
            if (r, c) in ((6, 6), (6, size - 7), (size - 7, 6)):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    m[r + dr][c + dc] = max(abs(dr), abs(dc)) != 1

    bits = [(cw >> i) & 1 for cw in codewords for i in range(7, -1, -1)]
    idx = 0
    right = size - 1
    while right >= 1:
        if right == 6:
            right = 5
        for vert in range(size):
            for j in range(2):
                x = right - j
                upward = ((right + 1) & 2) == 0
                y = (size - 1 - vert) if upward else vert
                if not fn[y][x] and idx < len(bits):
                    m[y][x] = bits[idx] == 1
                    idx += 1
        right -= 2

    best = None
    for mask in range(8):
        trial = [row[:] for row in m]
        for y in range(size):
            for x in range(size):
                if not fn[y][x] and _mask_fn(mask, x, y):
                    trial[y][x] = not trial[y][x]
        _draw_format(trial, size, _format_bits(ecl, mask))
        sc = _penalty(trial)
        if best is None or sc < best[0]:
            best = (sc, mask, trial)
    return best[2]


def to_svg_path(matrix, size_mm: float, quiet: int = 2):
    """Path SVG modul gelap (koordinat mm) + ukuran satu modul."""
    n = len(matrix)
    unit = size_mm / (n + quiet * 2)
    parts = []
    for y, row in enumerate(matrix):
        for x, val in enumerate(row):
            if val:
                parts.append(
                    f"M{(x + quiet) * unit:.4f} {(y + quiet) * unit:.4f}"
                    f"h{unit:.4f}v{unit:.4f}h-{unit:.4f}z"
                )
    return "".join(parts), unit


def _decode(matrix, ecl: str = "M"):
    """Dekoder internal untuk self-test (bukan decoder QR umum)."""
    n = len(matrix)
    version = (n - 17) // 4
    mask = None
    for k in range(8):
        fb = _format_bits(ecl, k)
        if all(matrix[i][8] == bool((fb >> i) & 1) for i in range(6)) \
           and matrix[8][8] == bool((fb >> 7) & 1) \
           and matrix[8][7] == bool((fb >> 8) & 1):
            mask = k
            break
    assert mask is not None, "format info tidak valid"
    fn = _function_mask(version)
    bits, right = [], n - 1
    while right >= 1:
        if right == 6:
            right = 5
        for vert in range(n):
            for j in range(2):
                x = right - j
                upward = ((right + 1) & 2) == 0
                y = (n - 1 - vert) if upward else vert
                if not fn[y][x]:
                    v = matrix[y][x]
                    if _mask_fn(mask, x, y):
                        v = not v
                    bits.append(1 if v else 0)
        right -= 2
    cws = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits) - 7, 8)]
    cap = _data_capacity(version, ecl)
    data, ecc = cws[:cap], cws[cap:cap + _ECC_CW[ecl][version]]
    assert _rs_remainder(data, len(ecc)) == list(ecc), "Reed-Solomon tidak konsisten"
    mode = data[0] >> 4
    count = ((data[0] & 0x0F) << 4) | (data[1] >> 4)
    assert mode == 4
    bytes_out = []
    bitbuf = "".join(f"{cw:08b}" for cw in data[1:])[4:]
    for i in range(count):
        bytes_out.append(int(bitbuf[i * 8:i * 8 + 8], 2))
    return version, mask, bytes(bytes_out).decode("utf-8"), len(cws)


def ascii_art(matrix) -> str:
    return "\n".join("".join("██" if v else "  " for v in row) for row in matrix)


if __name__ == "__main__":
    TEKS = "https://www.mitrasyariahbank.com"
    m = encode(TEKS, "M")
    ver, mask, hasil, jml = _decode(m, "M")
    print(f"versi={ver} ({(ver * 4 + 17)}x{(ver * 4 + 17)}) mask={mask} codeword={jml}")
    print("hasil decode:", hasil)
    assert hasil == TEKS, "round-trip gagal!"
    print("SELF-TEST LULUS: matriks -> decode -> teks sama, ECC Reed-Solomon valid")
