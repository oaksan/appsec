#!/usr/bin/env bash
# Script para exportar o projeto Zeppelin-AppSec de forma limpa e compactada (.zip)
set -e

OUTPUT_ZIP="zeppelin_appsec_export.zip"

echo "=== Exportando Zeppelin-AppSec ==="

# 1. Consolidar alterações do SQLite WAL no arquivo zeppelin.db (se existir)
if [ -f "zeppelin.db" ]; then
    echo ">> Consolidando WAL do SQLite no banco zeppelin.db..."
    if [ -d ".venv" ]; then
        .venv/bin/python3 -c "import sqlite3; con = sqlite3.connect('zeppelin.db'); con.execute('PRAGMA wal_checkpoint(TRUNCATE);'); con.close()" 2>/dev/null || true
    elif command -v python3 &>/dev/null; then
        python3 -c "import sqlite3; con = sqlite3.connect('zeppelin.db'); con.execute('PRAGMA wal_checkpoint(TRUNCATE);'); con.close()" 2>/dev/null || true
    fi
fi

# 2. Remover zip anterior se existir
rm -f "$OUTPUT_ZIP"

# 3. Gerar arquivo ZIP excluindo pastas de ambiente virtual, caches e temporários
echo ">> Gerando arquivo compactado $OUTPUT_ZIP..."
zip -r "$OUTPUT_ZIP" . \
    -x ".venv/*" \
    -x "*/__pycache__/*" \
    -x "__pycache__/*" \
    -x ".pytest_cache/*" \
    -x "*/.pytest_cache/*" \
    -x ".gemini/*" \
    -x "*/.gemini/*" \
    -x ".specify/*" \
    -x "*/.specify/*" \
    -x ".git/*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "zeppelin.db-shm" \
    -x "zeppelin.db-wal" \
    -x "$OUTPUT_ZIP"

echo ""
echo "=== Sucesso! ==="
echo "Arquivo gerado: $(pwd)/$OUTPUT_ZIP ($(du -h "$OUTPUT_ZIP" | cut -f1))"
echo "Basta enviar esse arquivo .zip para o outro computador, descompactar e seguir o README.md."
