"""Exporta datos de un CSV a un archivo JSON.

Uso:
    python exportar.py --input datos.csv --output resultado.json
    python exportar.py --input datos.csv --output resultado.json --indent 4
"""
import argparse
import csv
import json


def exportar_a_json(ruta_entrada, ruta_salida, indent=2):
    """Lee un CSV y escribe su contenido como lista de objetos JSON."""
    with open(ruta_entrada, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(filas, f, indent=indent, ensure_ascii=False)

    return len(filas)


def main():
    parser = argparse.ArgumentParser(description="Exportar un CSV a JSON")
    parser.add_argument("--input", required=True, help="Ruta del CSV de entrada")
    parser.add_argument("--output", required=True, help="Ruta del JSON de salida")
    parser.add_argument("--indent", type=int, default=2, help="Indentación (default: 2)")
    args = parser.parse_args()

    total = exportar_a_json(args.input, args.output, args.indent)
    print(f"Exportadas {total} filas a {args.output}")


if __name__ == "__main__":
    main()
