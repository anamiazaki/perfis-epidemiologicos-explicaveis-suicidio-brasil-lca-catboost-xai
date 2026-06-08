# Metodologia de Reprodução

Este documento resume a ordem recomendada para reproduzir a pipeline analítica do TCC.

1. Obter os microdados oficiais de mortalidade do SIM/DATASUS para 2010 a 2024.
2. Reconstruir a base analítica com `scripts/rebuild_dataset_suicidio.py`.
3. Executar `notebooks/01_criacao_dataset.ipynb` para preparação, padronização e recodificação da base.
4. Executar `notebooks/02_lca_perfil_integrado.ipynb` para estimação das soluções LCA e seleção da solução final.
5. Executar `notebooks/03_catboost_surrogate_xai.ipynb` para treinamento do classificador CatBoost, avaliação de fidelidade e análises SHAP/ALE.
6. Consultar `outputs/tables/` para tabelas pequenas de auditoria e resultados.
7. Consultar `outputs/figures/consolidated/` e `outputs/figures/panels/` para as figuras vetoriais consolidadas e painéis ampliados.

O modelo tem finalidade populacional e epidemiológica. Ele não prevê risco clínico individual e não deve ser usado para triagem, diagnóstico ou decisão assistencial sobre pessoas.
