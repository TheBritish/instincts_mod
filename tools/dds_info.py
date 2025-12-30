import struct, sys
p = r'C:\Users\Craig.CraigBates-PC\Documents\Paradox Interactive\Europa Universalis V\mod\instincts_mod\in_game\gfx\interface\icons\traits\conqueror.dds'
with open(p, 'rb') as f:
    h = f.read(128)
if h[:4] != b'DDS ':
    print('Not a DDS')
    sys.exit(1)
height = struct.unpack_from('<I', h, 12)[0]
width = struct.unpack_from('<I', h, 16)[0]
mipmaps = struct.unpack_from('<I', h, 28)[0]
dw_pf_size = struct.unpack_from('<I', h, 76)[0]
dw_pf_flags = struct.unpack_from('<I', h, 80)[0]
fourcc = h[84:88].decode('ascii', 'replace')
dw_rgb_bitcount = struct.unpack_from('<I', h, 88)[0]
dw_r_mask = struct.unpack_from('<I', h, 92)[0]
dw_g_mask = struct.unpack_from('<I', h, 96)[0]
dw_b_mask = struct.unpack_from('<I', h, 100)[0]
dw_a_mask = struct.unpack_from('<I', h, 104)[0]
print("%dx%d mipmaps=%d" % (width, height, mipmaps))
print("pixelfmt.size=%d flags=0x%08X fourcc='%s' rgb_bits=%d" % (dw_pf_size, dw_pf_flags, fourcc, dw_rgb_bitcount))
print("masks: R=0x%08X G=0x%08X B=0x%08X A=0x%08X" % (dw_r_mask, dw_g_mask, dw_b_mask, dw_a_mask))
