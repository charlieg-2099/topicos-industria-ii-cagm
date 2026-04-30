#!/bin/bash
# Script de medición de tiempos y tamaños para análisis WCSim
# Autor: Carlos Guzmán
# Uso: ./bench_cagm.sh <particle> <box_label> <output_file> -- <command...>

set -e

if [ $# -lt 4 ]; then
    echo "Uso: $0 <particle> <box_label> <output_file> -- <command...>"
    echo "Ejemplo: $0 e- 4_ROOT output.root -- docker exec WCSim ..."
    exit 1
fi

PARTICLE="$1"
BOX="$2"
OUTFILE="$3"
shift 3

# Esperar el separador --
if [ "$1" == "--" ]; then
    shift
fi

# Registrar tiempo de inicio
START=$(python3 -c 'import time; print(time.time())')

# Ejecutar comando
"$@"

# Registrar tiempo de fin
END=$(python3 -c 'import time; print(time.time())')

# Calcular duración
DURATION=$(python3 -c "print(f'{$END - $START:.3f}')")

# Obtener tamaño del archivo
if [ -f "$OUTFILE" ]; then
    BYTES=$(stat -f%z "$OUTFILE" 2>/dev/null || stat -c%s "$OUTFILE" 2>/dev/null || echo 0)
else
    BYTES=0
fi

# Guardar en CSV
RESULTS_FILE="$(dirname "$0")/../output/results_cagm.csv"

# Crear header si no existe
if [ ! -f "$RESULTS_FILE" ]; then
    echo "particle,box,seconds,bytes" > "$RESULTS_FILE"
fi

# Agregar medición
echo "$PARTICLE,$BOX,$DURATION,$BYTES" >> "$RESULTS_FILE"

# Mostrar resultado
echo ""
echo "=========================================="
echo "📊 Medición completada"
echo "=========================================="
echo "Partícula:  $PARTICLE"
echo "Caja:       $BOX"
echo "Duración:   ${DURATION}s ($(python3 -c "print(f'{$DURATION/60:.2f}')") min)"
echo "Tamaño:     $BYTES bytes ($(python3 -c "print(f'{$BYTES/1024/1024:.2f}')") MB)"
echo "Archivo:    $OUTFILE"
echo "=========================================="
echo ""

# Made with Bob
