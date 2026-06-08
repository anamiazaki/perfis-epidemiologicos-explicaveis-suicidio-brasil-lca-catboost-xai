from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from dbfread import DBF


BASE_DIR = Path(__file__).resolve().parent
RAW_DATASET = BASE_DIR / "Dataset Suicídio.csv"
FINAL_DATASET = BASE_DIR / "Dataset Suicídio 2010-2024.csv"
FALLBACK_FINAL_DATASET = BASE_DIR / "Dataset Suicídio 2010-2024 revisado.csv"
FINAL_PARQUET = BASE_DIR / "Dataset Suicídio 2010-2024.parquet"
FALLBACK_FINAL_PARQUET = BASE_DIR / "Dataset Suicídio 2010-2024 revisado.parquet"
DOCS_DIR = BASE_DIR / "Documentação do SIM"
CADMUN_PATH = DOCS_DIR / "Docs_Tabs_CID10" / "TABELAS" / "CADMUN.DBF"
TABUF_PATH = DOCS_DIR / "Docs_Tabs_CID10" / "TABELAS" / "TABUF.DBF"
CNV_PATH = BASE_DIR / "Arquivos CNV" / "br_municip.cnv"
OCUP_PATH = BASE_DIR / "cbo2002-ocupacao.csv"


DAY_MAP = {
    0: "Segunda-Feira",
    1: "Terça-Feira",
    2: "Quarta-Feira",
    3: "Quinta-Feira",
    4: "Sexta-Feira",
    5: "Sábado",
    6: "Domingo",
}

REGION_MAP = {
    "RO": "Norte",
    "AC": "Norte",
    "AM": "Norte",
    "RR": "Norte",
    "PA": "Norte",
    "AP": "Norte",
    "TO": "Norte",
    "MA": "Nordeste",
    "PI": "Nordeste",
    "CE": "Nordeste",
    "RN": "Nordeste",
    "PB": "Nordeste",
    "PE": "Nordeste",
    "AL": "Nordeste",
    "SE": "Nordeste",
    "BA": "Nordeste",
    "MG": "Sudeste",
    "ES": "Sudeste",
    "RJ": "Sudeste",
    "SP": "Sudeste",
    "PR": "Sul",
    "SC": "Sul",
    "RS": "Sul",
    "MS": "Centro-Oeste",
    "MT": "Centro-Oeste",
    "GO": "Centro-Oeste",
    "DF": "Centro-Oeste",
}

UF_NAME_MAP = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AM": "Amazonas",
    "AP": "Amap\u00e1",
    "BA": "Bahia",
    "CE": "Cear\u00e1",
    "DF": "Distrito Federal",
    "ES": "Esp\u00edrito Santo",
    "GO": "Goi\u00e1s",
    "MA": "Maranh\u00e3o",
    "MG": "Minas Gerais",
    "MS": "Mato Grosso Do Sul",
    "MT": "Mato Grosso",
    "PA": "Par\u00e1",
    "PB": "Para\u00edba",
    "PE": "Pernambuco",
    "PI": "Piau\u00ed",
    "PR": "Paran\u00e1",
    "RJ": "Rio De Janeiro",
    "RN": "Rio Grande Do Norte",
    "RO": "Rond\u00f4nia",
    "RR": "Roraima",
    "RS": "Rio Grande Do Sul",
    "SC": "Santa Catarina",
    "SE": "Sergipe",
    "SP": "S\u00e3o Paulo",
    "TO": "Tocantins",
}

MAP_SEXO = {"1": "Masculino", "M": "Masculino", "2": "Feminino", "F": "Feminino"}
MAP_RACACOR = {
    "1": "Branca",
    "2": "Preta",
    "3": "Amarela",
    "4": "Parda",
    "5": "Indígena",
}
MAP_ESTCIV = {
    "1": "Solteiro",
    "2": "Casado",
    "3": "Viúvo",
    "4": "Separado/Divorciado",
    "5": "União Estável",
}
MAP_ESC2010 = {
    "0": "Sem Escolaridade",
    "1": "Fundamental I",
    "2": "Fundamental II",
    "3": "Médio",
    "4": "Superior Incompleto",
    "5": "Superior Completo",
}
MAP_LOCOCOR = {
    "1": "Hospital",
    "2": "Outro Estab. Saúde",
    "3": "Domicílio",
    "4": "Via Pública",
    "5": "Outros",
    "6": "Aldeia Indígena",
}
MAP_SIM_NAO_SIM_IGN = {"1": "Sim", "2": "Não"}
MAP_FONTE = {"1": "Ocorrência Policial", "2": "Hospital", "3": "Família", "4": "Outra"}
MAP_CIRCOBITO = {"1": "Acidente", "2": "Suicídio", "3": "Homicídio", "4": "Outros"}
MAP_GEO_SOURCE = {"CADMUN": "Cadmun", "CNV": "Cnv", "SEM_MATCH": "Sem Match"}
MAP_MUN_SITUACAO = {"ATIVO": "Ativo", "TRANS": "Transferido", "IGNOR": "Ignorado", "EXTIN": "Extinto"}

MEIO_SUICIDIO_LABELS = {
    "X60": "Auto Intoxicação Por Analgésicos, Antipiréticos E Anti-Reumáticos",
    "X61": "Auto Intoxicação Por Anticonvulsivantes, Sedativos E Psicotrópicos",
    "X62": "Auto Intoxicação Por Narcóticos E Psicodislépticos",
    "X63": "Auto Intoxicação Por Outras Substâncias Do Sistema Nervoso Autônomo",
    "X64": "Auto Intoxicação Por Outras Drogas, Medicamentos E Substâncias Biológicas",
    "X65": "Auto Intoxicação Por Álcool",
    "X66": "Auto Intoxicação Por Solventes E Hidrocarbonetos",
    "X67": "Auto Intoxicação Por Outros Gases E Vapores",
    "X68": "Auto Intoxicação Por Pesticidas",
    "X69": "Auto Intoxicação Por Outros Produtos Químicos",
    "X70": "Enforcamento, Estrangulamento E Sufocação",
    "X71": "Afogamento E Submersão",
    "X72": "Arma De Fogo De Mão",
    "X73": "Arma De Fogo De Maior Calibre",
    "X74": "Outras Armas De Fogo Ou Não Especificadas",
    "X75": "Explosivos",
    "X76": "Fumaça, Fogo E Chamas",
    "X77": "Vapor D'Água, Gases E Objetos Quentes",
    "X78": "Objeto Cortante Ou Penetrante",
    "X79": "Objeto Contundente",
    "X80": "Precipitação De Lugar Elevado",
    "X81": "Precipitação Diante De Objeto Em Movimento",
    "X82": "Impacto Com Veículo A Motor",
    "X83": "Outros Meios Especificados",
    "X84": "Meios Não Especificados",
}

MEIO_SUICIDIO_GROUPS = {
    "X60": "Intoxicação Por Medicamentos E Substâncias Biológicas",
    "X61": "Intoxicação Por Medicamentos E Substâncias Biológicas",
    "X62": "Intoxicação Por Medicamentos E Substâncias Biológicas",
    "X63": "Intoxicação Por Medicamentos E Substâncias Biológicas",
    "X64": "Intoxicação Por Medicamentos E Substâncias Biológicas",
    "X65": "Intoxicação Por Álcool, Gases, Químicos E Pesticidas",
    "X66": "Intoxicação Por Álcool, Gases, Químicos E Pesticidas",
    "X67": "Intoxicação Por Álcool, Gases, Químicos E Pesticidas",
    "X68": "Intoxicação Por Álcool, Gases, Químicos E Pesticidas",
    "X69": "Intoxicação Por Álcool, Gases, Químicos E Pesticidas",
    "X70": "Enforcamento, Estrangulamento E Sufocação",
    "X71": "Afogamento E Submersão",
    "X72": "Arma De Fogo",
    "X73": "Arma De Fogo",
    "X74": "Arma De Fogo",
    "X75": "Explosivos, Fogo E Calor",
    "X76": "Explosivos, Fogo E Calor",
    "X77": "Explosivos, Fogo E Calor",
    "X78": "Objeto Cortante Ou Contundente",
    "X79": "Objeto Cortante Ou Contundente",
    "X80": "Precipitação, Impacto Ou Veículo",
    "X81": "Precipitação, Impacto Ou Veículo",
    "X82": "Precipitação, Impacto Ou Veículo",
    "X83": "Outros Meios Especificados",
    "X84": "Meios Não Especificados",
}

CID_LOCAL4_MAP = {
    "0": "Residência",
    "1": "Habitação Coletiva",
    "2": "Escola, Instituição Ou Área Administrativa Pública",
    "3": "Área De Esportes E Atletismo",
    "4": "Rua E Estrada",
    "5": "Área De Comércio E Serviços",
    "6": "Área Industrial E Construção",
    "7": "Fazenda",
    "8": "Outros Locais Especificados",
    "9": "Local Não Especificado",
}

CNV_NAME_FIXES = {
    "MOJUI DOS CAMPOS": "Mojuí Dos Campos",
    "NAZARIA": "Nazária",
    "PESCARIA BRAVA": "Pescaria Brava",
    "BALNEARIO RINCAO": "Balneário Rincão",
    "PINTO BANDEIRA": "Pinto Bandeira",
    "PARAISO DAS AGUAS": "Paraíso Das Águas",
}


def load_dbf(path: Path) -> pd.DataFrame:
    return pd.DataFrame(iter(DBF(path, load=True, char_decode_errors="ignore")))


def load_cnv_lookup(path: Path) -> pd.DataFrame:
    rows = []
    for line in path.read_text(encoding="latin-1").splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        if not parts[0].isdigit() or not re.fullmatch(r"\d{6}", parts[1]):
            continue
        code = parts[1]
        aliases = parts[-1]
        name = " ".join(parts[2:-1]).strip()
        rows.append(
            {
                "MUNCOD": code,
                "MUNNOME": name,
                "MUNNOMEX": name,
                "MUNCODDV": pd.NA,
                "UFCOD": code[:2],
                "SITUACAO": "IGNOR" if "IGNORADO" in name else pd.NA,
                "GEO_SOURCE": "CNV",
                "CNV_ALIASES": aliases,
            }
        )
    cnv = pd.DataFrame(rows).drop_duplicates(subset=["MUNCOD"])
    return cnv


def normalize_ocup_code(value: object) -> str | float:
    if pd.isna(value):
        return np.nan
    digits = re.sub(r"\D", "", str(value)).strip()
    if not digits:
        return np.nan
    return digits.zfill(6)


def load_ocup_lookup(path: Path) -> dict[str, str]:
    ocup = pd.read_csv(path, encoding="latin1", sep=";", dtype=str)
    ocup["CODIGO"] = ocup["CODIGO"].apply(normalize_ocup_code)
    ocup["TITULO"] = ocup["TITULO"].astype(str).apply(lambda x: " ".join(x.split()).title())
    ocup = ocup.dropna(subset=["CODIGO"]).drop_duplicates(subset=["CODIGO"])
    return ocup.set_index("CODIGO")["TITULO"].to_dict()

def format_place_name(name: object) -> object:
    if pd.isna(name):
        return np.nan
    text = str(name).strip()
    if not text:
        return np.nan
    if text.upper() in CNV_NAME_FIXES:
        return CNV_NAME_FIXES[text.upper()]
    return text.title()


def normalize_date(series: pd.Series) -> pd.Series:
    s = series.fillna("").astype(str).str.replace(r"\D", "", regex=True).str.strip()
    s = s.replace("", pd.NA)
    s = s.where(s.str.len() <= 8, s.str[-8:])
    s = s.str.zfill(8)
    return pd.to_datetime(s, format="%d%m%Y", errors="coerce")


def estacao_brasil(dt: pd.Timestamp) -> str | float:
    if pd.isna(dt):
        return np.nan
    year = dt.year
    if dt >= pd.Timestamp(year, 12, 21) or dt < pd.Timestamp(year, 3, 20):
        return "Verão"
    if dt < pd.Timestamp(year, 6, 21):
        return "Outono"
    if dt < pd.Timestamp(year, 9, 23):
        return "Inverno"
    return "Primavera"


def normalize_muncod(value: object) -> str | float:
    if pd.isna(value):
        return np.nan
    digits = re.sub(r"\D", "", str(value))
    if not digits:
        return np.nan
    if len(digits) >= 6:
        return digits[-6:]
    return digits.zfill(6)


def parse_idade_components(value: object) -> tuple[str | float, str | float]:
    if pd.isna(value):
        return (np.nan, np.nan)
    digits = re.sub(r"\D", "", str(value)).strip()
    if len(digits) != 3:
        return (np.nan, np.nan)
    return (digits[0], digits[1:3])


def decode_idade_anos(value: object) -> float:
    unit, qty_str = parse_idade_components(value)
    if pd.isna(unit) or pd.isna(qty_str):
        return np.nan
    qty = int(qty_str)
    if unit == "4":
        return float(qty)
    if unit == "5":
        return float(100 + qty)
    if unit == "3":
        return float(qty) / 12.0
    if unit == "2":
        return float(qty) / (24.0 * 365.0)
    if unit == "1":
        return float(qty) / (24.0 * 60.0 * 365.0)
    return np.nan


def faixa_etaria(idade_anos: float) -> str | float:
    if pd.isna(idade_anos):
        return np.nan
    if idade_anos < 15:
        return "<15"
    if idade_anos <= 29:
        return "15-29"
    if idade_anos <= 44:
        return "30-44"
    if idade_anos <= 59:
        return "45-59"
    return "60+"


def recode_categorical(
    series: pd.Series,
    mapping: dict[str, str],
    ignored_codes: set[str] | None = None,
) -> pd.Series:
    ignored_codes = {code.upper() for code in (ignored_codes or set())}
    normalized_mapping = {str(k).upper(): v for k, v in mapping.items()}

    s = series.fillna("").astype(str).str.strip().str.upper()
    out = s.map(normalized_mapping)
    out = out.mask(s.eq(""), "Não Preenchido")
    out = out.mask(s.isin(ignored_codes), "Ignorado")
    unknown_mask = out.isna() & s.ne("")
    out = out.mask(unknown_mask, "Código Inválido")
    return out


def normalize_cid_token(value: object) -> str:
    if pd.isna(value):
        return ""
    token = str(value).upper().strip()
    token = token.replace(".", "").replace(" ", "")
    token = token.lstrip("*")
    return token


def extract_cid3(value: object) -> str | float:
    token = normalize_cid_token(value)
    match = re.search(r"[A-Z]\d{2}", token)
    return match.group(0) if match else np.nan


def build_cid_flags(df: pd.DataFrame, cid_cols: list[str]) -> tuple[pd.Series, pd.Series]:
    pattern = re.compile(r"[A-Z]\d{2}")
    mental_flags = []
    subst_flags = []
    for _, row in df[cid_cols].iterrows():
        tokens = []
        for value in row:
            cleaned = normalize_cid_token(value)
            tokens.extend(pattern.findall(cleaned))
        has_mental = any(tok.startswith("F") and 20 <= int(tok[1:3]) <= 99 for tok in tokens)
        has_subst = any(tok.startswith("F") and 10 <= int(tok[1:3]) <= 19 for tok in tokens)
        mental_flags.append(int(has_mental))
        subst_flags.append(int(has_subst))
    return pd.Series(mental_flags, index=df.index), pd.Series(subst_flags, index=df.index)


def attach_geo(df: pd.DataFrame, geo_lookup: pd.DataFrame, code_col: str, prefix: str) -> pd.DataFrame:
    renamed = geo_lookup.rename(
        columns={
            "MUNCOD": code_col,
            "MUNCODDV": f"CODMUN{prefix}_DV",
            "MUNNOME": f"MUN_{prefix}_NOME",
            "MUNNOMEX": f"MUN_{prefix}_NOME_UPPER",
            "UFCOD": f"UF_{prefix}",
            "UF_SIGLA": f"UF_{prefix}_SIGLA",
            "UF_NOME": f"UF_{prefix}_NOME",
            "GEO_SOURCE": f"GEO_FONTE_{prefix}",
            "SITUACAO": f"MUN_{prefix}_SITUACAO",
        }
    )
    return df.merge(renamed, on=code_col, how="left")


def main() -> None:
    df = pd.read_csv(RAW_DATASET, encoding="utf-8-sig", dtype=str, low_memory=False)

    # Tabelas oficiais e fallback para municípios históricos.
    cadmun = load_dbf(CADMUN_PATH)
    tabuf = load_dbf(TABUF_PATH)
    cnv = load_cnv_lookup(CNV_PATH)
    ocup_lookup = load_ocup_lookup(OCUP_PATH)

    cadmun["MUNCOD"] = cadmun["MUNCOD"].astype(str).str.strip()
    cadmun["MUNCODDV"] = cadmun["MUNCODDV"].astype(str).str.strip()
    cadmun["MUNNOME"] = cadmun["MUNNOME"].astype(str).str.strip()
    cadmun["MUNNOMEX"] = cadmun["MUNNOMEX"].astype(str).str.strip()
    cadmun["UFCOD"] = cadmun["UFCOD"].astype(str).str.strip()
    cadmun["SITUACAO"] = cadmun["SITUACAO"].astype(str).str.strip()
    cadmun["GEO_SOURCE"] = "CADMUN"

    tabuf = tabuf.rename(columns={"CODIGO": "UFCOD", "SIGLA_UF": "UF_SIGLA", "DESCRICAO": "UF_NOME"})
    tabuf["UFCOD"] = tabuf["UFCOD"].astype(str).str.strip()
    tabuf["UF_SIGLA"] = tabuf["UF_SIGLA"].astype(str).str.strip()
    tabuf["UF_NOME"] = tabuf["UF_NOME"].astype(str).str.strip()

    geo_lookup = cadmun[
        ["MUNCOD", "MUNCODDV", "MUNNOME", "MUNNOMEX", "UFCOD", "SITUACAO", "GEO_SOURCE"]
    ].merge(tabuf, on="UFCOD", how="left")

    cnv_fallback = cnv[~cnv["MUNCOD"].isin(geo_lookup["MUNCOD"])].merge(tabuf, on="UFCOD", how="left")
    cnv_fallback = cnv_fallback[
        ["MUNCOD", "MUNCODDV", "MUNNOME", "MUNNOMEX", "UFCOD", "SITUACAO", "GEO_SOURCE", "UF_SIGLA", "UF_NOME"]
    ]
    geo_lookup = pd.concat([geo_lookup, cnv_fallback], ignore_index=True).drop_duplicates(subset=["MUNCOD"])

    # Datas e idade.
    df["DATA_OBITO"] = normalize_date(df["DTOBITO"])
    if "DTINVESTIG" in df.columns:
        df["DTINVESTIG"] = normalize_date(df["DTINVESTIG"])
    if "DTCONCASO" in df.columns:
        df["DTCONCASO"] = normalize_date(df["DTCONCASO"])
    df["ANO_OBITO"] = df["DATA_OBITO"].dt.year.astype("Int64")
    df["MES_OBITO"] = df["DATA_OBITO"].dt.month.astype("Int64")
    df["DIA_OBITO"] = df["DATA_OBITO"].dt.day.astype("Int64")
    df["SEMANA_OBITO"] = df["DATA_OBITO"].dt.isocalendar().week.astype("Int64")
    df["DIA_DA_SEMANA"] = df["DATA_OBITO"].dt.dayofweek.map(DAY_MAP)
    df["ESTACAO"] = df["DATA_OBITO"].apply(estacao_brasil)

    idade_anos = df["IDADE"].apply(decode_idade_anos)
    df["IDADE"] = pd.Series(np.floor(idade_anos), index=df.index).where(idade_anos.notna(), pd.NA).astype("Int64")
    df["FAIXA_ETARIA"] = idade_anos.apply(faixa_etaria)

    circobito_raw = df["CIRCOBITO"].fillna("").astype(str).str.strip()

    # Substitui códigos por categorias legíveis e permanentes.
    df["SEXO"] = recode_categorical(df["SEXO"], MAP_SEXO, {"0", "9", "I"})
    df["RACACOR"] = recode_categorical(df["RACACOR"], MAP_RACACOR, {"9"})
    df["ESTCIV"] = recode_categorical(df["ESTCIV"], MAP_ESTCIV, {"9"})
    df["ESC2010"] = recode_categorical(df["ESC2010"], MAP_ESC2010, {"9"})
    df["LOCOCOR"] = recode_categorical(df["LOCOCOR"], MAP_LOCOCOR, {"9"})
    df["ASSISTMED"] = recode_categorical(df["ASSISTMED"], MAP_SIM_NAO_SIM_IGN, {"9"})
    df["NECROPSIA"] = recode_categorical(df["NECROPSIA"], MAP_SIM_NAO_SIM_IGN, {"9"})
    df["FONTE"] = recode_categorical(df["FONTE"], MAP_FONTE, {"9"})
    df["CIRCOBITO"] = recode_categorical(df["CIRCOBITO"], MAP_CIRCOBITO, {"9"})
    ocup_raw = df["OCUP"].apply(normalize_ocup_code)
    df["OCUP"] = ocup_raw.map(ocup_lookup)
    df["OCUP"] = np.where(ocup_raw.isna(), "Não Preenchido", df["OCUP"])
    df["OCUP"] = pd.Series(df["OCUP"], index=df.index).fillna("Código Inválido")

    # Geografia corrigida.
    df["CODMUNRES"] = df["CODMUNRES"].apply(normalize_muncod)
    df["CODMUNOCOR"] = df["CODMUNOCOR"].apply(normalize_muncod)

    df = attach_geo(df, geo_lookup, "CODMUNRES", "RES")
    df = attach_geo(df, geo_lookup, "CODMUNOCOR", "OCOR")

    df["MUN_RES_NOME"] = df["MUN_RES_NOME"].apply(format_place_name)
    df["MUN_OCOR_NOME"] = df["MUN_OCOR_NOME"].apply(format_place_name)
    df["UF_RES"] = df["UF_RES_SIGLA"].map(UF_NAME_MAP)
    df["UF_OCOR"] = df["UF_OCOR_SIGLA"].map(UF_NAME_MAP)
    df["REGIAO_RES"] = df["UF_RES_SIGLA"].map(REGION_MAP)
    df["REGIAO_OCOR"] = df["UF_OCOR_SIGLA"].map(REGION_MAP)
    df["GEO_FONTE_RES"] = df["GEO_FONTE_RES"].fillna("SEM_MATCH").map(MAP_GEO_SOURCE)
    df["GEO_FONTE_OCOR"] = df["GEO_FONTE_OCOR"].fillna("SEM_MATCH").map(MAP_GEO_SOURCE)
    df["MUN_RES_SITUACAO"] = recode_categorical(df["MUN_RES_SITUACAO"], MAP_MUN_SITUACAO)
    df["MUN_OCOR_SITUACAO"] = recode_categorical(df["MUN_OCOR_SITUACAO"], MAP_MUN_SITUACAO)

    # Causa básica e meio do suicídio.
    df["CAUSABAS"] = df["CAUSABAS"].apply(normalize_cid_token)
    df["CAUSABAS_CID3"] = df["CAUSABAS"].apply(extract_cid3)
    df["LOCAL_OCOR_CID"] = (
        df["CAUSABAS"]
        .str[3]
        .where(df["CAUSABAS"].str.len() >= 4, pd.NA)
        .map(CID_LOCAL4_MAP)
        .fillna("Não Preenchido")
    )
    df["MEIO_SUICIDIO"] = df["CAUSABAS_CID3"].map(MEIO_SUICIDIO_LABELS)
    df["MEIO_SUICIDIO_GRUPO"] = df["CAUSABAS_CID3"].map(MEIO_SUICIDIO_GROUPS)

    # CIDs das linhas e indicadores.
    line_cols = [col for col in ["LINHAA", "LINHAB", "LINHAC", "LINHAD", "LINHAII"] if col in df.columns]
    if line_cols:
        for col in line_cols:
            df[col] = df[col].apply(normalize_cid_token).replace("", pd.NA)
        df["NUM_CAUSAS_INFORMADAS"] = df[line_cols].notna().sum(axis=1)
        mental_flag, subst_flag = build_cid_flags(df, line_cols)
        df["FLAG_TP_MENTAL_F20_F99"] = mental_flag
        df["FLAG_TP_SUBST_F10_F19"] = subst_flag
    else:
        df["NUM_CAUSAS_INFORMADAS"] = 0
        df["FLAG_TP_MENTAL_F20_F99"] = 0
        df["FLAG_TP_SUBST_F10_F19"] = 0

    # Qualidade / consistência.
    df["FLAG_CIRC_SUIC"] = circobito_raw.eq("2").astype(int)
    is_x60_x84 = df["CAUSABAS_CID3"].astype(str).str.match(r"^X(6[0-9]|7[0-9]|8[0-4])$", na=False)
    circ_is_2 = circobito_raw.eq("2")
    df["INCONSIST_CIRC_CAUSABAS"] = np.where(is_x60_x84 & ~circ_is_2, 1, 0)

    final_columns = [
        "DATA_OBITO",
        "ANO_OBITO",
        "MES_OBITO",
        "DIA_OBITO",
        "SEMANA_OBITO",
        "DIA_DA_SEMANA",
        "ESTACAO",
        "HORAOBITO",
        "SEXO",
        "IDADE",
        "FAIXA_ETARIA",
        "RACACOR",
        "ESTCIV",
        "ESC2010",
        "ESCFALAGR1",
        "OCUP",
        "CODMUNRES",
        "MUN_RES_NOME",
        "UF_RES",
        "REGIAO_RES",
        "GEO_FONTE_RES",
        "MUN_RES_SITUACAO",
        "CODMUNOCOR",
        "MUN_OCOR_NOME",
        "UF_OCOR",
        "REGIAO_OCOR",
        "GEO_FONTE_OCOR",
        "MUN_OCOR_SITUACAO",
        "LOCOCOR",
        "CAUSABAS",
        "CAUSABAS_CID3",
        "LOCAL_OCOR_CID",
        "MEIO_SUICIDIO",
        "MEIO_SUICIDIO_GRUPO",
        "LINHAA",
        "LINHAB",
        "LINHAC",
        "LINHAD",
        "LINHAII",
        "NUM_CAUSAS_INFORMADAS",
        "FLAG_TP_MENTAL_F20_F99",
        "FLAG_TP_SUBST_F10_F19",
        "CIRCOBITO",
        "FLAG_CIRC_SUIC",
        "INCONSIST_CIRC_CAUSABAS",
        "ASSISTMED",
        "NECROPSIA",
        "FONTE",
        "ALTCAUSA",
        "DTINVESTIG",
        "FONTEINV",
        "TPRESGINFO",
        "DIFDATA",
        "NUDIASOBCO",
        "DTCONCASO",
    ]
    final_columns = [col for col in final_columns if col in df.columns]
    df_final = df[final_columns].copy()

    output_csv_path = FINAL_DATASET
    output_parquet_path = FINAL_PARQUET
    try:
        df_final.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    except PermissionError:
        output_csv_path = FALLBACK_FINAL_DATASET
        output_parquet_path = FALLBACK_FINAL_PARQUET
        df_final.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

    try:
        df_final.to_parquet(output_parquet_path, index=False)
    except PermissionError:
        output_parquet_path = FALLBACK_FINAL_PARQUET
        df_final.to_parquet(output_parquet_path, index=False)

    print(f"CSV salvo em: {output_csv_path}")
    print(f"Parquet salvo em: {output_parquet_path}")
    print(f"Registros: {len(df_final):,}")
    print(f"Colunas: {len(df_final.columns)}")
    print("Distribuição de GEO_FONTE_RES:")
    print(df_final["GEO_FONTE_RES"].value_counts(dropna=False).to_string())
    print("Distribuição de GEO_FONTE_OCOR:")
    print(df_final["GEO_FONTE_OCOR"].value_counts(dropna=False).to_string())
    print("Top MEIO_SUICIDIO:")
    print(df_final["MEIO_SUICIDIO"].value_counts(dropna=False).head(15).to_string())


if __name__ == "__main__":
    main()
