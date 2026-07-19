#!/usr/bin/env python3
"""Minimal, correct BPS encoder + decoder (self-verifying). Emits a linear BPS using only
SourceRead / TargetRead ops (valid BPS; compact because base and target differ in only a few
small regions). Verifies by decoding its own output back against the base.

  usage: make_bps.py <source.nes> <target.nes> <out.bps>
"""
import sys, zlib

def enc_num(n):                      # beat/BPS variable-length number
    out = bytearray()
    while True:
        x = n & 0x7f
        n >>= 7
        if n == 0:
            out.append(0x80 | x); break
        out.append(x); n -= 1
    return bytes(out)

def dec_num(buf, p):
    data, shift = 0, 1
    while True:
        x = buf[p]; p += 1
        data += (x & 0x7f) * shift
        if x & 0x80: break
        shift <<= 7; data += shift
    return data, p

def make_bps(src, tgt, metadata=b""):
    body = bytearray()
    body += b"BPS1"
    body += enc_num(len(src))
    body += enc_num(len(tgt))
    body += enc_num(len(metadata)); body += metadata
    # walk target, grouping same-as-source vs different runs
    i, n = 0, len(tgt)
    def same_at(k):
        return k < len(src) and tgt[k] == src[k]
    while i < n:
        same = same_at(i)
        j = i
        while j < n and same_at(j) == same:
            j += 1
        length = j - i
        if same:                     # SourceRead (cmd 0): copy from source at outputOffset
            body += enc_num(((length - 1) << 2) | 0)
        else:                        # TargetRead (cmd 1): literal bytes follow
            body += enc_num(((length - 1) << 2) | 1)
            body += tgt[i:j]
        i = j
    body += zlib.crc32(src).to_bytes(4, "little")
    body += zlib.crc32(tgt).to_bytes(4, "little")
    patch_crc = zlib.crc32(bytes(body)).to_bytes(4, "little")
    body += patch_crc
    return bytes(body)

def apply_bps(patch, src):           # decoder (for self-verification)
    assert patch[:4] == b"BPS1"
    p = 4
    ssize, p = dec_num(patch, p)
    tsize, p = dec_num(patch, p)
    msize, p = dec_num(patch, p); p += msize
    assert ssize == len(src), "source size mismatch"
    assert zlib.crc32(src) == int.from_bytes(patch[-12:-8], "little"), "source CRC mismatch"
    out = bytearray(); end = len(patch) - 12
    so = ro = to = 0
    while p < end:
        cmd, p = dec_num(patch, p)
        length = (cmd >> 2) + 1
        action = cmd & 3
        if action == 0:              # SourceRead
            out += src[len(out):len(out) + length]
        elif action == 1:            # TargetRead
            out += patch[p:p + length]; p += length
        elif action == 2:            # SourceCopy
            rel, p = dec_num(patch, p)
            so += (-(rel >> 1) if (rel & 1) else (rel >> 1))
            out += src[so:so + length]; so += length
        else:                        # TargetCopy
            rel, p = dec_num(patch, p)
            to += (-(rel >> 1) if (rel & 1) else (rel >> 1))
            for _ in range(length):
                out.append(out[to]); to += 1
    assert len(out) == tsize, "target size mismatch"
    assert zlib.crc32(bytes(out)) == int.from_bytes(patch[-8:-4], "little"), "target CRC mismatch"
    return bytes(out)

if __name__ == "__main__":
    src = open(sys.argv[1], "rb").read()
    tgt = open(sys.argv[2], "rb").read()
    patch = make_bps(src, tgt)
    # self-verify: decode our own patch, must reproduce the target exactly
    back = apply_bps(patch, src)
    assert back == tgt, "SELF-VERIFY FAILED: decoded != target"
    open(sys.argv[3], "wb").write(patch)
    print(f"wrote {sys.argv[3]} ({len(patch)} bytes)  self-verify OK")
    print(f"  source {sys.argv[1]} crc32={zlib.crc32(src):08x} size={len(src)}")
    print(f"  target {sys.argv[2]} crc32={zlib.crc32(tgt):08x} size={len(tgt)}")
