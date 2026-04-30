#!/usr/bin/env python3
"""
Script para generar visualizaciones de análisis de capacidades WCSim
Autor: Carlos Guzmán
Fecha: Abril 2026
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).parent.parent
CSV_FILE = BASE_DIR / "output" / "results_cagm.csv"
OUTPUT_DIR = BASE_DIR / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

EVENTS_1K = 1000
SCALE_1M = 1_000_000 / EVENTS_1K

# Cargar datos
data = []
with open(CSV_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['seconds'] = float(row['seconds'])
        row['bytes'] = int(row['bytes'])
        data.append(row)

PARTICLES = ['e-', 'mu-', 'gamma']
BOXES = ['4_ROOT', '5_NPZ', '6_IMG', '8_MLNPZ', '9_H5']
BOX_NAMES = {
    '4_ROOT': 'ROOT Files',
    '5_NPZ': 'NPZ Analysis',
    '6_IMG': 'Image Conv.',
    '8_MLNPZ': 'ML NPZ',
    '9_H5': 'HDF5'
}
COLORS = {'e-': '#2E86AB', 'mu-': '#A23B72', 'gamma': '#F18F01'}

def get_data(particle, box):
    for row in data:
        if row['particle'] == particle and row['box'] == box:
            return row
    return None

# Gráfica 1: Tiempos por caja (escala logarítmica)
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(BOXES))
width = 0.25

for i, p in enumerate(PARTICLES):
    times = [get_data(p, b)['seconds'] for b in BOXES]
    offset = (i - 1) * width
    bars = ax.bar(x + offset, times, width, label=p, color=COLORS[p], alpha=0.8)
    
ax.set_xlabel('Processing Box', fontsize=12, fontweight='bold')
ax.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
ax.set_title('Processing Time per Box - 1,000 Events\nMac M1 (32GB RAM, Rancher Desktop)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([BOX_NAMES[b] for b in BOXES], rotation=15, ha='right')
ax.set_yscale('log')
ax.legend(title='Particle', fontsize=10)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'tiempos_1k_cagm.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 2: Tamaños de archivo
fig, ax = plt.subplots(figsize=(10, 6))

for i, p in enumerate(PARTICLES):
    sizes_mb = [get_data(p, b)['bytes'] / (1024**2) for b in BOXES]
    offset = (i - 1) * width
    bars = ax.bar(x + offset, sizes_mb, width, label=p, color=COLORS[p], alpha=0.8)

ax.set_xlabel('Processing Box', fontsize=12, fontweight='bold')
ax.set_ylabel('File Size (MB)', fontsize=12, fontweight='bold')
ax.set_title('Output File Sizes per Box - 1,000 Events\nMac M1 (32GB RAM, Rancher Desktop)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([BOX_NAMES[b] for b in BOXES], rotation=15, ha='right')
ax.legend(title='Particle', fontsize=10)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'tamanos_1k_cagm.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 3: Estimación de horas para 1M eventos
fig, ax = plt.subplots(figsize=(9, 6))
total_hours = []

for p in PARTICLES:
    total_secs = sum(get_data(p, b)['seconds'] for b in BOXES)
    hours = (total_secs * SCALE_1M) / 3600
    total_hours.append(hours)

bars = ax.bar(PARTICLES, total_hours, color=[COLORS[p] for p in PARTICLES], 
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, total_hours):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.1f}h\n({val/24:.1f}d)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Processing Time (hours)', fontsize=12, fontweight='bold')
ax.set_xlabel('Particle Type', fontsize=12, fontweight='bold')
ax.set_title('Estimated Total Processing Time for 1M Events per Particle\n(Sequential execution on single core)',
             fontsize=13, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'estimado_horas_1M_cagm.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 4: Estimación de almacenamiento para 1M eventos
fig, ax = plt.subplots(figsize=(9, 6))
total_gb = []

for p in PARTICLES:
    total_bytes = sum(get_data(p, b)['bytes'] for b in BOXES)
    gb = (total_bytes * SCALE_1M) / (1024**3)
    total_gb.append(gb)

bars = ax.bar(PARTICLES, total_gb, color=[COLORS[p] for p in PARTICLES],
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, total_gb):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.1f} GB',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Storage Required (GB)', fontsize=12, fontweight='bold')
ax.set_xlabel('Particle Type', fontsize=12, fontweight='bold')
ax.set_title('Estimated Total Storage for 1M Events per Particle\n(All processing boxes combined)',
             fontsize=13, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'estimado_gb_1M_cagm.png', dpi=150, bbox_inches='tight')
plt.close()

# Resumen en consola
print("\n" + "="*70)
print("RESUMEN DE ANÁLISIS - CAPACIDADES WCSIM")
print("="*70)
print("\n📊 Mediciones base (1,000 eventos):")
print("-" * 70)
for p in PARTICLES:
    total_s = sum(get_data(p, b)['seconds'] for b in BOXES)
    total_mb = sum(get_data(p, b)['bytes'] for b in BOXES) / (1024**2)
    print(f"  {p:6} | Tiempo: {total_s:7.1f}s ({total_s/60:5.1f}min) | Tamaño: {total_mb:6.1f} MB")

print("\n🚀 Proyección para 1,000,000 eventos:")
print("-" * 70)
for p in PARTICLES:
    total_s = sum(get_data(p, b)['seconds'] for b in BOXES)
    total_bytes = sum(get_data(p, b)['bytes'] for b in BOXES)
    hours = (total_s * SCALE_1M) / 3600
    days = hours / 24
    gb = (total_bytes * SCALE_1M) / (1024**3)
    print(f"  {p:6} | {hours:6.1f}h ({days:4.1f}d) | {gb:6.1f} GB")

total_time = sum(sum(get_data(p, b)['seconds'] for b in BOXES) for p in PARTICLES)
total_storage = sum(sum(get_data(p, b)['bytes'] for b in BOXES) for p in PARTICLES)
total_hours_1m = (total_time * SCALE_1M) / 3600
total_gb_1m = (total_storage * SCALE_1M) / (1024**3)

print("\n📈 TOTAL (3 partículas, 1M eventos cada una):")
print("-" * 70)
print(f"  Tiempo total:        {total_hours_1m:7.1f} horas ({total_hours_1m/24:5.1f} días)")
print(f"  Almacenamiento:      {total_gb_1m:7.1f} GB ({total_gb_1m/1024:5.2f} TB)")
print("="*70)
print(f"\n✅ Gráficas generadas en: {OUTPUT_DIR}")
print("="*70 + "\n")

# Made with Bob
