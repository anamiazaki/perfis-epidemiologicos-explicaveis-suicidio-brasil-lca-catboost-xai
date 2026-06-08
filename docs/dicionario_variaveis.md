# Dicionário de variáveis

Este documento resume as principais variáveis utilizadas na construção dos perfis epidemiológicos. Os nomes podem variar entre os microdados originais do SIM/DATASUS e as versões recodificadas usadas nos notebooks.

| Variável | Descrição | Uso analítico |
| --- | --- | --- |
| `ano_obito` | Ano de ocorrência ou registro do óbito. | Recorte temporal de 2010 a 2024. |
| `causabas` | Causa básica do óbito segundo CID-10. | Seleção dos registros X60 a X84. |
| `sexo` | Sexo registrado na Declaração de Óbito. | Dimensão demográfica dos perfis. |
| `faixa_etaria` | Faixa etária recodificada. | Dimensão demográfica e efeitos SHAP/ALE. |
| `raca_cor` | Raça/cor registrada no SIM. | Caracterização sociodemográfica. |
| `estado_civil` | Situação conjugal recodificada. | Caracterização dos perfis latentes. |
| `escolaridade` | Escolaridade recodificada. | Dimensão socioeconômica. |
| `ocupacao_macro` | Ocupação agregada em grupos interpretáveis. | Redução de cardinalidade e perfilamento. |
| `regiao_residencia` | Região geográfica de residência. | Dimensão territorial. |
| `deslocamento` | Indicador de deslocamento entre município de residência e ocorrência. | Dimensão territorial/assistencial. |
| `local_ocorrencia` | Local de ocorrência do óbito recodificado. | Dimensão circunstancial. |
| `meio` | Meio ou mecanismo da lesão autoprovocada. | Dimensão circunstancial. |
| `classe_lca` | Classe latente atribuída pela LCA. | Alvo do classificador CatBoost surrogate. |
| `posterior_maximo` | Maior probabilidade posterior de alocação na LCA. | Auditoria de confiança da alocação. |

As variáveis foram recodificadas para reduzir fragmentação, melhorar interpretabilidade e evitar perfis sustentados por categorias raras ou pouco informativas.
