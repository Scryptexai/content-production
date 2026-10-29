#!/usr/bin/env python3
"""Adegan 3D di Blender (Cycles CPU) → still + peta kedalaman.

Kenapa bukan animasi penuh: di mesin ini Cycles hanya ~8 dtk/frame (2 core),
jadi 6.000 frame = 14 jam. Yang dipakai karena itu:

  1. Blender merender SATU frame per adegan, kualitas tinggi (32 sample,
     denoise) — beberapa detik saja.
  2. Blender juga mengeluarkan peta kedalaman (Z) lewat compositor.
  3. Gerakan kamera dibakar belakangan di Python dari still + Z (parallax
     sungguhan, objek dekat bergerak lebih cepat daripada latar).

Hasil: gambar benar-benar 3D, kamera benar-benar bergerak, biayanya menit.

    python3 blender_scene.py --out remotion/public/footage --only office
"""
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

CREAM = (0.937, 0.906, 0.863, 1)
INK = (0.043, 0.055, 0.086, 1)
ROSE = (0.851, 0.557, 0.451, 1)
SAGE = (0.561, 0.663, 0.545, 1)


def reset(samples=24, res=(1600, 900)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = 4
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Filmic"
    sc.view_settings.look = "Medium High Contrast"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.image_settings.compression = 70
    # peta kedalaman (compositor dinyalakan hanya saat render Z)
    sc.view_layers[0].use_pass_z = True
    sc.use_nodes = True
    nt = sc.node_tree
    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers")
    # normalisasi Z: 0 = dekat, 1 = jauh
    mr = nt.nodes.new("CompositorNodeMapRange")
    mr.inputs["From Min"].default_value = 1.0
    mr.inputs["From Max"].default_value = 26.0
    mr.inputs["To Min"].default_value = 0.0
    mr.inputs["To Max"].default_value = 1.0

    comp = nt.nodes.new("CompositorNodeComposite")
    z_out = rl.outputs.get("Depth") or rl.outputs.get("Z")
    nt.links.new(z_out, mr.inputs["Value"])
    nt.links.new(mr.outputs["Value"], comp.inputs["Image"])
    sc.use_nodes = False   # dinyalakan lagi khusus saat render Z
    return sc


def mat(name, color, rough=0.6, emit=None, emit_strength=6.0, metal=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit is not None:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = emit_strength
    return m


def box(loc, size, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    o.data.materials.append(material)
    return o


def plane(loc, size, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc, rotation=rot)
    o = bpy.context.object
    o.data.materials.append(material)
    return o


def world(color=(0.012, 0.016, 0.028), strength=1.0):
    w = bpy.data.worlds.new("W")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*color, 1)
    bg.inputs[1].default_value = strength


def area(loc, energy, size=4.0, color=(1, 0.96, 0.90), rot=(0, 0, 0)):
    bpy.ops.object.light_add(type="AREA", location=loc, rotation=rot)
    l = bpy.context.object
    l.data.energy = energy
    l.data.size = size
    l.data.color = color
    return l


def camera(loc, look_at, fov=42):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    d = Vector(look_at) - Vector(loc)
    c.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    c.data.angle = math.radians(fov)
    c.data.clip_start = 0.3
    c.data.clip_end = 60
    bpy.context.scene.camera = c
    return c


# ------------------------------------------------------------------ adegan
def scene_grid():
    """Ruang grid perspektif: lantai menyala, garis merambat, kamera menyusur."""
    reset(samples=20, res=(1600, 900))
    world((0.005, 0.007, 0.013), 0.7)
    dark = mat("g_dark", (0.014, 0.018, 0.028, 1), rough=0.35, metal=0.35)
    glowc = mat("g_glow", (0.02, 0.03, 0.05, 1), rough=0.3,
                emit=(0.38, 0.56, 0.86, 1), emit_strength=7)
    plane((0, 10, 0), 90, dark)
    # garis membujur + melintang, menyala
    for i in range(-14, 15):
        size = 0.035 if i % 5 else 0.075
        m = glowc if i % 5 == 0 else mat("g_dim", (0.05, 0.07, 0.10, 1), rough=0.4,
                                         emit=(0.16, 0.22, 0.34, 1), emit_strength=2)
        box((i * 1.15, 10, 0.012), (size, 42, 0.01), m)
        box((0, 10 + i * 1.15, 0.012), (42, size, 0.01), m)
    # trefoil 3D penuh di kiri: tiga lingkaran bersilangan, jangkar visual
    tor = mat("tor", (0.05, 0.06, 0.09, 1), rough=0.3,
              emit=(0.92, 0.82, 0.74, 1), emit_strength=2.8)
    tor2 = mat("tor2", (0.05, 0.045, 0.04, 1), rough=0.3,
               emit=(0.85, 0.55, 0.45, 1), emit_strength=2.2)
    for k, rot_z in enumerate((0, 120, 240)):
        bpy.ops.mesh.primitive_torus_add(location=(-3.9, 8.4, 1.75), major_radius=0.78,
                                         minor_radius=0.075, major_segments=88, minor_segments=10)
        o = bpy.context.object
        o.rotation_euler = (math.radians(62), 0, math.radians(rot_z))
        o.data.materials.append(tor if k == 0 else tor2)
    area((0, 2, 7), 420, size=10, color=(0.7, 0.8, 1.0))
    area((-6, 9, 2.5), 220, size=6, color=(1.0, 0.7, 0.55))
    camera((-1.9, -6.4, 2.05), (0.9, 9.0, 1.05), fov=42)


def scene_columns():
    """Deretan kolom cahaya: satu kolom unggul, sisanya surut."""
    reset(samples=20, res=(1600, 900))
    world((0.006, 0.008, 0.015), 0.6)
    base = mat("c_base", (0.016, 0.020, 0.030, 1), rough=0.4, metal=0.3)
    plane((0, 8, 0), 80, base)
    cream = (0.94, 0.90, 0.86, 1)
    rose = (0.85, 0.55, 0.45, 1)
    sage = (0.56, 0.66, 0.54, 1)
    for gx in range(-6, 7):
        for gy in range(0, 7):
            h = 0.6 + 3.6 * (0.5 + 0.5 * math.sin(gx * 0.7 + gy * 0.45 + 0.6)) ** 2.2
            col = cream if (gx == 1 and gy == 3) else (rose if gy % 3 == 0 else sage)
            strength = 5.0 if (gx == 1 and gy == 3) else 0.55
            m = mat(f"col{gx}_{gy}", (0.03, 0.035, 0.045, 1), rough=0.5,
                    emit=col, emit_strength=strength)
            box((gx * 1.5, gy * 2.0 + 1.0, h / 2), (0.42, 0.42, h), m)
    area((0, 3, 8), 300, size=9, color=(0.8, 0.86, 1.0))
    camera((-1.6, -7.5, 2.3), (0.4, 6.0, 1.6), fov=42)


def scene_room():
    """Ruang kosong dengan cahaya dari satu celah: tempat kalimat berat."""
    reset(samples=20, res=(1600, 900))
    world((0.004, 0.006, 0.011), 0.35)
    wall = mat("r_wall", (0.030, 0.034, 0.044, 1), rough=0.9)
    floor = mat("r_floor", (0.020, 0.024, 0.032, 1), rough=0.42, metal=0.15)
    plane((0, 8, 0), 90, floor)
    box((0, 22, 6), (44, 0.5, 12), wall)
    box((12, 8, 6), (0.5, 40, 12), wall)
    box((-12, 8, 6), (0.5, 40, 12), wall)
    box((0, 8, 11.8), (44, 40, 0.4), wall)
    # celah cahaya tinggi di dinding kanan
    gap = mat("r_gap", (0.02, 0.03, 0.05, 1), rough=0.2,
              emit=(0.72, 0.82, 1.0, 1), emit_strength=14)
    box((11.6, 9, 4.6), (0.2, 9.0, 5.2), gap)
    area((10.4, 9, 4.6), 900, size=8, color=(0.62, 0.74, 1.0))
    # satu objek kesepian
    box((0.2, 9.6, 0.42), (1.9, 0.9, 0.8), mat("r_obj", (0.05, 0.055, 0.07, 1), rough=0.55))
    camera((-3.6, -4.5, 2.1), (0.6, 10.0, 1.2), fov=40)


def scene_tunnel():
    """Lorong bercahaya: kamera masuk, waktu terasa berjalan."""
    reset(samples=20, res=(1600, 900))
    world((0.004, 0.005, 0.010), 0.4)
    dark = mat("t_dark", (0.012, 0.015, 0.022, 1), rough=0.7)
    ring = mat("t_ring", (0.02, 0.03, 0.05, 1), rough=0.3,
               emit=(0.46, 0.62, 0.92, 1), emit_strength=6)
    for i in range(16):
        y = i * 2.6
        bpy.ops.mesh.primitive_torus_add(location=(0, y, 2.2), major_radius=5.2,
                                         minor_radius=0.09, major_segments=64, minor_segments=8)
        o = bpy.context.object
        o.rotation_euler = (math.radians(90), 0, 0)
        o.data.materials.append(ring if i % 3 == 0 else mat(f"t_r{i}", (0.04, 0.05, 0.07, 1),
                                                            rough=0.4, emit=(0.18, 0.24, 0.36, 1),
                                                            emit_strength=1.6))
    plane((0, 20, 0), 90, dark)
    area((0, 6, 8), 260, size=10, color=(0.75, 0.85, 1.0))
    camera((0.7, -9.0, 2.3), (-0.2, 8.0, 2.3), fov=48)


def scene_wire():
    """Grafik simpul: tiga lingkaran bersilangan sebagai benda 3D."""
    reset(samples=24, res=(1600, 900))
    world((0.005, 0.007, 0.013), 0.5)
    m_main = mat("w_main", (0.04, 0.05, 0.07, 1), rough=0.25,
                 emit=(0.90, 0.80, 0.72, 1), emit_strength=2.6)
    m_rose = mat("w_rose", (0.05, 0.04, 0.04, 1), rough=0.25,
                 emit=(0.85, 0.55, 0.45, 1), emit_strength=2.2)
    m_sage = mat("w_sage", (0.04, 0.05, 0.04, 1), rough=0.25,
                 emit=(0.56, 0.66, 0.54, 1), emit_strength=2.0)
    specs = [((0.0, 0.0, 0.0), (58, 0, 0), m_main, 1.55),
             ((0.0, 0.0, 0.0), (58, 0, 120), m_rose, 1.55),
             ((0.0, 0.0, 0.0), (58, 0, 240), m_sage, 1.55)]
    for loc, rot, m, mr in specs:
        bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=mr,
                                         minor_radius=0.055, major_segments=96,
                                         minor_segments=10)
        o = bpy.context.object
        o.rotation_euler = tuple(math.radians(a) for a in rot)
        o.data.materials.append(m)
    area((0, -6, 6), 260, size=8, color=(1.0, 0.96, 0.9))
    area((5, 4, 3), 160, size=6, color=(0.7, 0.8, 1.0))
    camera((0.0, -7.6, 1.1), (0.0, 0.0, 0.1), fov=38)


SCENES = {"grid": scene_grid, "columns": scene_columns, "room": scene_room,
          "tunnel": scene_tunnel, "wire": scene_wire}


def render(name, out_dir: Path):
    SCENES[name]()
    sc = bpy.context.scene
    out_dir.mkdir(parents=True, exist_ok=True)
    # 1) warna — compositor mati supaya tidak tertimpa pass Z
    sc.use_nodes = False
    sc.render.image_settings.color_mode = "RGB"
    sc.render.filepath = str(out_dir / f"3d-{name}.png")
    bpy.ops.render.render(write_still=True)
    # 2) kedalaman — compositor dinyalakan
    sc.use_nodes = True
    sc.render.image_settings.color_mode = "BW"
    sc.render.filepath = str(out_dir / f"3d-{name}-z.png")
    bpy.ops.render.render(write_still=True)
    print(f"  {name}: warna + kedalaman")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    names = [a.only] if a.only else list(SCENES)
    for n in names:
        render(n, Path(a.out))
