# Perfis Epidemiológicos Explicáveis de Óbitos por Suicídio no Brasil com LCA, CatBoost e XAI

Repositório final do TCC **Perfis Epidemiológicos Explicáveis de Óbitos por Suicídio no Brasil com LCA, CatBoost e XAI**, de Ana Paula Miazaki, André Marcondes Pedott, Fernando Augusto Paulino e Júnior, Braz Izaias da Silva (Orientador).

## Objetivo

Identificar perfis epidemiológicos explicáveis de óbitos por suicídio no Brasil, combinando LCA para descoberta de classes latentes, CatBoost como modelo surrogate para reproduzir os perfis e técnicas de XAI para interpretação global e por perfil.

## Dados

A fonte dos dados é o Sistema de Informações sobre Mortalidade (SIM/DATASUS). O estudo considera óbitos registrados entre **2010 e 2024**, selecionados pelos códigos **CID-10 X60-X84**. A base final analisada contém **191.025 óbitos**.

Os microdados completos e bases intermediárias não são versionados neste repositório. Arquivos brutos, processados, `.parquet`, modelos e artefatos compactados devem permanecer localmente em `data/` ou nos diretórios de artefatos.

## Métodos

A pipeline metodológica inclui:

1. criação e padronização da base analítica a partir do SIM/DATASUS;
2. seleção de óbitos por lesões autoprovocadas intencionalmente (CID-10 X60-X84);
3. recodificação, redução de cardinalidade e auditoria de variáveis categóricas;
4. estimação de LCA com soluções de K=2 a K=6 classes;
5. treinamento de CatBoost como classificador surrogate dos perfis latentes;
6. interpretação com SHAP e ALE;
7. geração de tabelas, figuras vetoriais e artigo final em PDF.

O modelo não prevê risco clínico individual e não deve ser usado para triagem, diagnóstico ou decisão assistencial sobre pessoas. A finalidade é populacional, epidemiológica, interpretativa e auditável.

## Reprodução

Crie um ambiente Python e instale as dependências:

```bash
python -m venv .venv
pip install -r requirements.txt
```

Execute a pipeline na ordem:

```bash
python scripts/rebuild_dataset_suicidio.py
jupyter notebook notebooks/01_criacao_dataset.ipynb
jupyter notebook notebooks/02_lca_perfil_integrado.ipynb
jupyter notebook notebooks/03_catboost_surrogate_xai.ipynb
```

As figuras consolidadas oficiais já versionadas ficam em `outputs/figures/consolidated/pdf/`. Os painéis separados ficam em subpastas de `outputs/figures/panels/` para facilitar leitura ampliada no GitHub. Todas as figuras oficiais estão em PDF vetorial.

O PDF final do artigo está disponível em `article/Perfis Epidemiológicos Explicáveis de Óbitos por Suicídio no Brasil com LCA, CatBoost e XAI.pdf`.

## Estrutura

```text
article/              PDF final do artigo
notebooks/            notebooks numerados da pipeline
scripts/              script de reconstrução da base analítica
outputs/figures/      figuras consolidadas e painéis suplementares em PDF vetorial
outputs/tables/       tabelas pequenas de auditoria e resultados
data/                 documentação de dados; base completa não versionada
docs/                 documentação auxiliar
```

## Figuras

As figuras vetoriais consolidadas do artigo estão em `outputs/figures/consolidated/pdf/`:

- `fig00_pipeline_metodologica.pdf`
- `fig01_lca_selecao_estabilidade.pdf`
- `fig02_perfis_lca.pdf`
- `fig03_fidelidade_catboost.pdf`
- `fig04_shap_global.pdf`
- `fig05_shap_por_perfil.pdf`
- `fig06_beeswarm_por_perfil.pdf`
- `fig07_interacoes_ale.pdf`

Os painéis separados estão em `outputs/figures/panels/` e existem para leitura ampliada e auditoria visual no GitHub; eles são recortes vetoriais das figuras consolidadas sempre que possível.

## Citação

Use o arquivo `CITATION.cff` para citar este repositório. Em texto:

Miazaki, A. P.; Pedott, A. M.; Paulino, F. A.; Izaias, B. Perfis Epidemiológicos Explicáveis de Óbitos por Suicídio no Brasil com LCA, CatBoost e XAI. 2026.
