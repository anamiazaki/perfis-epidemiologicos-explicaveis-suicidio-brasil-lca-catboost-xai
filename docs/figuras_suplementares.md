# Figuras suplementares e organização dos painéis

As figuras consolidadas oficiais do artigo ficam em:

```text
outputs/figures/consolidated/pdf/
```

Esses PDFs são a fonte vetorial principal para publicação e auditoria. As figuras consolidadas são as utilizadas no artigo final.

Os painéis separados ficam em subpastas de:

```text
outputs/figures/panels/
```

Esses arquivos existem para facilitar leitura ampliada no GitHub, especialmente quando uma figura consolidada contém vários painéis. Sempre que possível, os painéis são recortes vetoriais diretos dos PDFs consolidados, sem uso de PNG como fonte, sem screenshots e sem redesenho dos gráficos. Todas as figuras disponibilizadas para consulta pública estão em PDF vetorial.

## Estrutura dos painéis

```text
outputs/figures/panels/
  fig01_lca_selecao_estabilidade/
  fig02_perfis_lca/
  fig03_fidelidade_catboost/
  fig04_shap_global/
  fig05_shap_por_perfil/
  fig06_beeswarm_por_perfil/
  fig07_interacoes_ale/
```

O Painel C da figura de perfis (`outputs/figures/panels/fig02_perfis_lca/fig02C_marcadores_lift_vs_global.pdf`) também está disponível separadamente em tamanho maior. Ele preserva o formato aprovado de barras horizontais, com rótulos curtos dos marcadores e valores no formato `x | %`. A legenda de cores indica as dimensões analíticas: demográfica, socioeconômica/ocupacional, territorial e circunstancial.

A paleta aplicada ao Painel C é: demográfica = `#6A3D9A`; socioeconômica/ocupacional = `#B15928`; territorial = `#1B9E77`; circunstancial = `#D95F02`.
