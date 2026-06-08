# Dados

Este diretório documenta a área local de dados do projeto. A base completa, os microdados brutos do SIM/DATASUS, arquivos intermediários e bases processadas não são versionados neste repositório.

A reconstrução da base analítica deve seguir o script `scripts/rebuild_dataset_suicidio.py` e os notebooks numerados em `notebooks/`, a partir das fontes oficiais do Sistema de Informações sobre Mortalidade (SIM/DATASUS).

Estrutura local sugerida, ignorada pelo Git:

```text
data/raw/
data/interim/
data/processed/
```

Não incluir no repositório arquivos `.zip`, `.parquet`, `.dbc`, `.dbf`, modelos treinados ou datasets completos.
