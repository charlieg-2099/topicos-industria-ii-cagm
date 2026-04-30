# Análisis de Capacidades Computacionales para Simulaciones WCSim

> **Evaluación de recursos de procesamiento y almacenamiento para el pipeline de análisis de eventos de física de partículas utilizando WCSim en arquitectura Apple Silicon**

**Autor:** Carlos Guzmán  
**Institución:** Maestría en Ciencias Aplicadas - Tópicos de Industria  
**Fecha:** Abril 2026  
**Sistema:** Mac M1 (32GB RAM) con Rancher Desktop

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Especificaciones del Sistema](#especificaciones-del-sistema)
3. [Metodología](#metodología)
4. [Resultados Experimentales](#resultados-experimentales)
5. [Análisis de Proyecciones](#análisis-de-proyecciones)
6. [Conclusiones](#conclusiones)
7. [Anexos](#anexos)

---

## 🎯 Resumen Ejecutivo

Este documento presenta un análisis exhaustivo de los recursos computacionales necesarios para ejecutar el pipeline completo de procesamiento de datos de simulaciones WCSim. Se evaluaron **cinco cajas de procesamiento** (4, 5, 6, 8 y 9) utilizando **tres tipos de partículas** (e⁻, μ⁻, γ) con **1,000 eventos por partícula** como base de medición.

### Hallazgos Principales

- **Tiempo total de procesamiento (1M eventos/partícula):** ~1,600 horas (66.7 días) en ejecución secuencial
- **Almacenamiento total requerido (1M eventos/partícula):** ~1.2 TB
- **Caja más costosa en tiempo:** Generación de archivos ROOT (Caja 4) - 60% del tiempo total
- **Caja más costosa en almacenamiento:** Archivos ROOT y NPZ - 75% del espacio total

---

## 💻 Especificaciones del Sistema

### Hardware

| Componente | Especificación |
|------------|----------------|
| **Modelo** | MacBook Pro (2021) |
| **Procesador** | Apple M1 (8 cores: 4 Performance + 4 Efficiency) |
| **Memoria RAM** | 32 GB LPDDR4X |
| **Almacenamiento** | 512 GB SSD NVMe |
| **Arquitectura** | ARM64 (Apple Silicon) |

### Software y Entorno

| Componente | Versión/Configuración |
|------------|----------------------|
| **Sistema Operativo** | macOS Sonoma 14.4.1 |
| **Runtime de Contenedores** | Rancher Desktop 1.13.1 |
| **Docker Engine** | 26.0.0 |
| **Imagen WCSim** | `manu33/wcsim:1.2` (linux/amd64) |
| **Emulación** | Rosetta 2 (amd64 → arm64) |

### Configuración de Recursos

Durante las mediciones se utilizaron dos configuraciones:

**Configuración Inicial:**
- CPUs asignadas: 2
- Memoria RAM: 6 GB
- Uso: Mediciones preliminares

**Configuración Optimizada:**
- CPUs asignadas: 6
- Memoria RAM: 18 GB
- Uso: Mediciones finales reportadas

> **Nota sobre rendimiento:** La emulación de arquitectura linux/amd64 en Apple Silicon (arm64) introduce un overhead de aproximadamente 20-30% en comparación con ejecución nativa.

---

## 🔬 Metodología

### Diseño Experimental

Se implementó un pipeline de medición automatizado que registra:
1. **Tiempo de ejecución** (segundos) con precisión de milisegundos
2. **Tamaño de archivo de salida** (bytes) para cada caja de procesamiento
3. **Uso de recursos** (CPU, memoria) durante la ejecución

### Cajas de Procesamiento Evaluadas

| Caja | Descripción | Input | Output | Herramienta |
|------|-------------|-------|--------|-------------|
| **4** | Generación de archivos ROOT | Archivos MAC | Archivos ROOT | WCSim |
| **5** | Conversión ROOT → NPZ | Archivos ROOT | Archivos NPZ | event_dump.py |
| **6** | Conversión NPZ → Imágenes | Archivos NPZ | Arrays de imágenes | npz_to_image.py |
| **8** | Generación ML_NPZ | Archivos ROOT | NPZ optimizado para ML | event_dump_barrel.py |
| **9** | Conversión NPZ → HDF5 | Archivos NPZ | Archivos H5 | np_to_digihit_array_hdf5.py |

### Partículas Simuladas

- **e⁻ (Electrón):** Energía 500 MeV, 1000 eventos
- **μ⁻ (Muon):** Energía 500 MeV, 1000 eventos
- **γ (Gamma):** Energía 500 MeV, 1000 eventos

### Archivos MAC de Configuración

Los archivos de configuración Geant4 (`.mac`) se generaron con los siguientes parámetros:

```bash
/gun/particle [e-|mu-|gamma]
/gun/energy 500 MeV
/gun/direction 1 0 0
/gun/position 0 0 0
/run/beamOn 1000
```

Archivos disponibles en: [`tarea5_cagm/mac/`](mac/)

### Script de Medición

Se desarrolló un script bash (`bench_cagm.sh`) para automatizar las mediciones:

```bash
./bench_cagm.sh <particle> <box> <output_file> -- <command>
```

El script registra automáticamente tiempo y tamaño en `results_cagm.csv`.

---

## 📊 Resultados Experimentales

### Datos Completos (1,000 eventos)

| Partícula | Caja | Tiempo (seg) | Tiempo (min) | Tamaño (bytes) | Tamaño (MB) |
|-----------|------|-------------:|-------------:|---------------:|------------:|
| e⁻ | 4_ROOT | 3,417 | 56.95 | 166,723,584 | 159.0 |
| e⁻ | 5_NPZ | 630 | 10.50 | 143,945,380 | 137.3 |
| e⁻ | 6_IMG | 1,473 | 24.55 | 112,640,128 | 107.4 |
| e⁻ | 8_MLNPZ | 101 | 1.68 | 20,359,864 | 19.4 |
| e⁻ | 9_H5 | 5 | 0.08 | 25,381,204 | 24.2 |
| **μ⁻** | 4_ROOT | 3,493 | 58.22 | 148,897,792 | 142.0 |
| μ⁻ | 5_NPZ | 509 | 8.48 | 129,400,435 | 123.4 |
| μ⁻ | 6_IMG | 1,082 | 18.03 | 112,640,128 | 107.4 |
| μ⁻ | 8_MLNPZ | 72 | 1.20 | 13,998,397 | 13.3 |
| μ⁻ | 9_H5 | 4 | 0.07 | 16,432,360 | 15.7 |
| **γ** | 4_ROOT | 3,200 | 53.33 | 166,873,526 | 159.1 |
| γ | 5_NPZ | 627 | 10.45 | 143,824,572 | 137.2 |
| γ | 6_IMG | 1,458 | 24.30 | 112,640,128 | 107.4 |
| γ | 8_MLNPZ | 96 | 1.60 | 20,205,852 | 19.3 |
| γ | 9_H5 | 5 | 0.08 | 25,234,448 | 24.1 |

### Resumen por Partícula (1,000 eventos)

| Partícula | Tiempo Total (min) | Almacenamiento Total (MB) |
|-----------|-------------------:|--------------------------:|
| **e⁻** | 93.76 | 447.3 |
| **μ⁻** | 86.00 | 401.8 |
| **γ** | 89.76 | 447.1 |
| **TOTAL** | **269.52** | **1,296.2** |

### Visualizaciones

#### Tiempos de Procesamiento por Caja

![Tiempos 1k](figures/tiempos_1k_cagm.png)

*Figura 1: Tiempo de ejecución por caja de procesamiento (escala logarítmica). Se observa que la Caja 4 (ROOT) domina el tiempo total de procesamiento.*

#### Tamaños de Archivo por Caja

![Tamaños 1k](figures/tamanos_1k_cagm.png)

*Figura 2: Tamaño de archivos de salida por caja. Los archivos ROOT y NPZ representan la mayor parte del almacenamiento requerido.*

---

## 📈 Análisis de Proyecciones

### Escalamiento a 1,000,000 de Eventos

Aplicando un factor de escala lineal de **×1,000** a las mediciones base:

#### Proyección por Partícula

| Partícula | Tiempo (horas) | Tiempo (días) | Almacenamiento (GB) |
|-----------|---------------:|--------------:|--------------------:|
| **e⁻** | 1,562.7 | 65.1 | 437.0 |
| **μ⁻** | 1,433.3 | 59.7 | 392.4 |
| **γ** | 1,496.0 | 62.3 | 436.8 |

#### Proyección Total (3 partículas × 1M eventos)

| Métrica | Valor |
|---------|-------|
| **Tiempo total de procesamiento** | **4,492 horas** (187.2 días) |
| **Almacenamiento total** | **1.23 TB** (1,266 GB) |

#### Estimación de Horas para 1M Eventos

![Horas 1M](figures/estimado_horas_1M_cagm.png)

*Figura 3: Tiempo estimado de procesamiento para 1 millón de eventos por partícula en ejecución secuencial.*

#### Estimación de Almacenamiento para 1M Eventos

![GB 1M](figures/estimado_gb_1M_cagm.png)

*Figura 4: Almacenamiento estimado requerido para 1 millón de eventos por partícula.*

### Desglose Detallado por Caja (1M eventos)

| Partícula | Caja | Tiempo (h) | % Tiempo | Tamaño (GB) | % Almacenamiento |
|-----------|------|----------:|---------:|------------:|-----------------:|
| e⁻ | 4_ROOT | 949.2 | 60.7% | 155.6 | 35.6% |
| e⁻ | 5_NPZ | 175.0 | 11.2% | 134.1 | 30.7% |
| e⁻ | 6_IMG | 409.2 | 26.2% | 104.9 | 24.0% |
| e⁻ | 8_MLNPZ | 28.1 | 1.8% | 19.0 | 4.3% |
| e⁻ | 9_H5 | 1.4 | 0.1% | 23.6 | 5.4% |
| μ⁻ | 4_ROOT | 970.3 | 67.7% | 136.8 | 34.9% |
| μ⁻ | 5_NPZ | 141.4 | 9.9% | 120.5 | 30.7% |
| μ⁻ | 6_IMG | 300.6 | 21.0% | 104.9 | 26.7% |
| μ⁻ | 8_MLNPZ | 20.0 | 1.4% | 13.0 | 3.3% |
| μ⁻ | 9_H5 | 1.1 | 0.1% | 15.3 | 3.9% |
| γ | 4_ROOT | 888.9 | 59.4% | 155.4 | 35.6% |
| γ | 5_NPZ | 174.2 | 11.6% | 134.0 | 30.7% |
| γ | 6_IMG | 405.0 | 27.1% | 104.9 | 24.0% |
| γ | 8_MLNPZ | 26.7 | 1.8% | 18.8 | 4.3% |
| γ | 9_H5 | 1.4 | 0.1% | 23.5 | 5.4% |

---

## 🔍 Conclusiones

### Hallazgos Clave

1. **Cuello de Botella Principal: Caja 4 (ROOT)**
   - Representa el **60-68%** del tiempo total de procesamiento
   - Cualquier optimización debe enfocarse prioritariamente en esta etapa
   - Candidato ideal para paralelización masiva

2. **Almacenamiento Dominado por ROOT y NPZ**
   - Cajas 4 y 5 representan **~66%** del almacenamiento total
   - Estrategias de compresión podrían reducir significativamente los requerimientos

3. **Variabilidad entre Partículas**
   - Muones (μ⁻) requieren **menos tiempo y espacio** que electrones y gammas
   - Diferencia atribuible a la física de interacción: muones a 500 MeV no producen cascadas electromagnéticas

4. **Cajas Ligeras (8 y 9)**
   - Representan menos del **2%** del tiempo total combinado
   - No son críticas para optimización de recursos

### Implicaciones Prácticas

#### Para Procesamiento Secuencial (1 core)

- **Tiempo requerido:** ~187 días continuos
- **Inviable** para producción a gran escala
- **Recomendación:** Implementar paralelización

#### Con Paralelización (ejemplo: 100 cores)

- **Tiempo reducido:** ~1.9 días
- **Factible** para producción
- **Costo:** Requiere infraestructura de cómputo distribuido

#### Requerimientos de Almacenamiento

- **1.23 TB** para dataset completo (3 partículas × 1M eventos)
- **Recomendación:** Planificar al menos **2 TB** considerando:
  - Archivos temporales
  - Respaldos
  - Margen de seguridad (20%)

### Consideraciones de Arquitectura

El uso de **Apple Silicon (M1)** con emulación presenta:

**Ventajas:**
- Excelente eficiencia energética
- Memoria unificada de alto rendimiento
- Ideal para desarrollo y pruebas

**Limitaciones:**
- Overhead de emulación (~20-30%)
- No escalable para producción masiva
- Recomendación: Migrar a clusters x86_64 nativos para producción

---

## 📚 Anexos

### A. Comandos de Ejecución

#### Generación de Archivos ROOT (Caja 4)

```bash
docker exec WCSim bash -c "cd /home/neutrino/software; source run.sh; \
  cd \$SOFTWARE/WCSim_build; \
  ./WCSim /home/neutrino/data/1_MAC/VaryE/e-/wcs_MCA_e-__0_500_MeV.mac; \
  mv wcs_MCA_e-__0_500_MeV.root /home/neutrino/data/2_ROOT/VaryE/e-/"
```

#### Conversión ROOT → NPZ (Caja 5)

```bash
docker exec WCSim bash -c "cd /home/neutrino/software; source run.sh; \
  cd /home/WatChMal/DataTools/DataTools-master/root_utils; \
  export PYTHONPATH=/home/WatChMal/DataTools/DataTools-master:\$PYTHONPATH; \
  python3 event_dump.py \
    /home/neutrino/data/2_ROOT/VaryE/e-/wcs_MCA_e-__0_500_MeV.root \
    -d /home/neutrino/data/3_Analisis_NPZ/VaryE/e-"
```

### B. Generación de Gráficas

```bash
cd tarea5_cagm/scripts
python3 make_charts_cagm.py
```

Las gráficas se generan automáticamente en `tarea5_cagm/figures/`.

### C. Estructura del Proyecto

```
tarea5_cagm/
├── README_Tarea5_CAGM.md          # Este documento
├── mac/                            # Archivos de configuración MAC
│   ├── wcs_MCA_e-__0_500_MeV.mac
│   ├── wcs_MCA_mu-__0_500_MeV.mac
│   └── wcs_MCA_gamma__0_500_MeV.mac
├── output/
│   └── results_cagm.csv           # Datos de mediciones
├── figures/                        # Visualizaciones generadas
│   ├── tiempos_1k_cagm.png
│   ├── tamanos_1k_cagm.png
│   ├── estimado_horas_1M_cagm.png
│   └── estimado_gb_1M_cagm.png
└── scripts/
    ├── bench_cagm.sh              # Script de medición
    └── make_charts_cagm.py        # Generador de gráficas
```

### D. Referencias

- **WCSim:** Water Cherenkov Simulator - https://github.com/WCSim/WCSim
- **DataTools:** WatChMaL Data Processing Tools - https://github.com/WatChMaL/DataTools
- **Imagen Docker:** manu33/wcsim:1.2 - https://hub.docker.com/r/manu33/wcsim

---

## 📞 Contacto carlos.guzman@academicos.udg.mx

**Carlos Guzmán**  
Maestría en Ciencias Aplicadas  
Tópicos de Industria  II
Abril 2026

---

*Documento generado como parte del análisis de capacidades computacionales para simulaciones de física de partículas utilizando WCSim en arquitectura Apple Silicon.*
