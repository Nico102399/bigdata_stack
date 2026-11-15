# Flujo de Git para un equipo de analítica

Guía de referencia rápida: cómo trabajar con Git en un repo de analítica (queries, informes, notebooks) sin romper lo que ya funciona.

## Idea central

- `main` es la versión que funciona. **Nadie commitea directo en ella.**
- Cada tarea vive en su propia **branch** con nombre descriptivo.
- Al terminar se abre un **Pull Request (PR)** para que otra persona lo revise.
- Si está bien, se fusiona a `main` y se **borra la branch**.

**Por qué `main` es sagrado:** los informes automatizados leen de `main`. Lo que fusionas el viernes es lo que verá la dirección el lunes a las 7:05. El PR es la red de seguridad contra decisiones de negocio basadas en un error tuyo.

## Flujo de un día típico

```bash
# 1. Empezar el día: actualizar main
git switch main
git pull

# 2. Crear branch para la tarea
git switch -c feature/query-retencion-cohortes

# 3. Trabajar y commitear (varios commits pequeños)
git add queries/retencion_cohortes.sql
git commit -m "feat: query base de retencion mensual"

# 4. Subir el progreso (backup + visibilidad)
git push -u origin feature/query-retencion-cohortes

# 5. Antes del PR: traer los últimos cambios de main
git switch main
git pull
git switch feature/query-retencion-cohortes
git merge main            # resolver conflictos si los hay

# 6. Crear el PR
gh pr create --title "feat: retencion por cohorte para producto" \
  --body "Query que calcula retencion M1-M6 por cohorte mensual."

# 7. Si el revisor pide cambios: commit + push (el PR se actualiza solo)
git add queries/retencion_cohortes.sql
git commit -m "docs: anadir comentario explicativo al CTE"
git push

# 8. Tras la aprobación: merge desde GitHub y borrar la branch
git switch main
git pull
git branch -d feature/query-retencion-cohortes
git fetch --prune
```

## Nombres de branches

Formato: `tipo/descripcion-en-minusculas-con-guiones`

| Prefijo | Para qué | Ejemplo |
|---|---|---|
| `feature/` | Funcionalidad nueva: query, análisis, notebook | `feature/segmentacion-clientes-rfm` |
| `fix/` | Corregir un cálculo, duplicado o filtro | `fix/informe-semanal-duplicados` |
| `docs/` | Documentación, README, comentarios | `docs/diccionario-metricas` |
| `refactor/` | Reorganizar sin cambiar resultados | `refactor/separar-queries-por-area` |

## Mensajes de commit (Conventional Commits)

Formato: `tipo: descripción breve`

```bash
git commit -m "feat: query de retencion por cohorte mensual"
git commit -m "fix: filtro de fecha excluia el ultimo dia del mes"
git commit -m "refactor: simplificar CTE de ingresos recurrentes"
git commit -m "docs: documentar metrica de churn en diccionario"
```

| Tipo | Significado |
|---|---|
| `feat` | Análisis, query o gráfico nuevo |
| `fix` | Corrección de cálculo, filtro o duplicado |
| `refactor` | Reorganizar sin cambiar resultados |
| `docs` | Documentación, comentarios, diccionario |

Evita mensajes como `cambios`, `fix`, `wip`, `asdf`: dentro de 3 meses no te servirán para saber cuándo cambió un cálculo.

## Estructura de un repo de analítica

```
analitica-ecommerce/
├── queries/                  # Queries SQL por área
│   ├── retencion/
│   │   ├── cohortes_mensual.sql
│   │   └── churn_por_segmento.sql
│   ├── ingresos/
│   │   ├── ingresos_recurrentes.sql
│   │   └── arpu_por_plan.sql
│   └── marketing/
│       ├── atribucion_canal.sql
│       └── cac_por_campana.sql
├── informes/                 # Scripts que generan informes periódicos
│   ├── kpis_semanales.py
│   └── informe_mensual.py
├── notebooks/                # Análisis exploratorios
│   ├── exploracion_churn_q3.ipynb
│   └── segmentacion_rfm.ipynb
├── docs/                     # Documentación del equipo
│   ├── diccionario_metricas.md
│   └── guia_nuevos_analistas.md
├── .gitignore
└── README.md
```

### Qué va en el repo y qué no

| En el repo (código y lógica) | Fuera del repo (datos, secretos, caché) |
|---|---|
| `queries/*.sql` | `*.csv`, `*.xlsx`, `*.parquet` |
| `informes/*.py` | `.env` (credenciales) |
| `notebooks/*.ipynb` | `__pycache__/`, `.ipynb_checkpoints/` |
| `docs/*.md`, `README.md`, `.gitignore` | `.DS_Store`, `Thumbs.db` |

**Regla simple:** el código y la lógica van en Git. Los datos y los secretos, no.

## `.gitignore` recomendado

```gitignore
# Credenciales
.env
.env.local

# Datos locales
*.csv
*.xlsx
*.parquet
datos/*
!datos/.gitkeep

# Python
__pycache__/
*.pyc
.venv/
venv/

# Notebooks
.ipynb_checkpoints/

# IDE y sistema
.vscode/
.idea/
.DS_Store
Thumbs.db
```

> **Peligro real:** si subes un `.env` con la contraseña de producción, asume la credencial comprometida. Los bots escanean GitHub 24/7 y borrar el commit después no sirve: queda en el historial. **Credenciales nunca en Git.**

## Gitflow: simplificado, no completo

El Gitflow original (`develop`, `release`, `hotfix`) sirve para software con versiones empaquetadas y QA. Un equipo de analítica necesita solo **`main` + feature branches + PRs con revisión**. La complejidad del flujo debe ser proporcional al riesgo de romper algo.

## Errores comunes

| Excusa | Por qué está mal |
|---|---|
| "Es un cambio pequeño, lo commiteo a main" | Un typo en un `WHERE` puede filtrar la mitad de los datos sin que nadie lo note. |
| "Trabajo solo, no necesito branches" | Las branches son tu historial de decisiones. |
| "No recuerdo esta branch, creo otra" | Borra la vieja primero; 30 branches abandonadas = escritorio desordenado. |
| "Me apruebo mi propio PR" | Pierde su valor: otro par de ojos caza lo que tú no ves. |

## Comandos útiles de Git

```bash
git branch                 # ramas locales
git branch -a              # locales y remotas
git log --oneline --graph --all --decorate   # historial en grafo
git branch -d nombre       # borrar rama local (ya fusionada)
git push origin --delete nombre              # borrar rama en GitHub
git fetch --prune          # limpiar referencias a ramas borradas
git reflog                 # recuperar commits de una rama borrada
```

## Para la entrevista

Si te piden describir tu flujo de Git en equipo, no recites comandos. Explica el **porqué**:

- **Branches:** para no romper lo que funciona.
- **PRs:** para que otro revise antes de que llegue a producción.
- **`main` sagrado:** porque lo usan los informes automatizados.

## Resumen

`main` funciona y nadie la toca directamente. Cada tarea va en una branch con nombre descriptivo. Al terminar, PR con revisión. Si está bien, merge a `main` y se borra la branch.