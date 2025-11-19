"""
Configurazioni degli indicatori macro da scaricare.
Include GDP, HICP, deficit/debt, current account, sentiment, IP, retail sales e unemployment.
"""

# ==============================
# Geo disponibili
# ==============================
GEOS = [
    "EA20","AT","BE","HR","CY","EE","FI","FR","DE","GR",
    "IE","IT","LV","LT","LU","MT","NL","PT","SK","SI","ES"
]

# ==============================
# Indicatori da scaricare
# Formato: INDICATORS = { "nome": (dataset, params, freq) }
# ==============================
INDICATORS = {
    # GDP and components (quarterly)
    "GDP": ("namq_10_gdp", {"freq": "Q", "na_item": "B1GQ", "unit": "CLV20_MNAC", "s_adj": "NSA"}, "Q"),
    "GDP_HH_CONSUMPTION": ("namq_10_gdp", {"freq": "Q", "na_item": "P31_S14", "unit": "CLV20_MNAC", "s_adj": "NSA"}, "Q"),
    "GDP_GVT_CONSUMPTION": ("namq_10_gdp", {"freq": "Q", "na_item": "P3_S13", "unit": "CLV20_MNAC", "s_adj": "NSA"}, "Q"),
    "GDP_Investments": ("namq_10_gdp", {"freq": "Q", "na_item": "P51G", "unit": "CLV_I20", "s_adj": "NSA"}, "Q"),
    "GDP_ChangeInventories": ("namq_10_gdp", {"freq": "Q", "na_item": "P52_P53", "unit": "CP_MEUR", "s_adj": "NSA"}, "Q"),
    "GDP_Export": ("namq_10_gdp", {"freq": "Q", "na_item": "P6", "unit": "CLV20_MNAC", "s_adj": "NSA"}, "Q"),
    "GDP_IMPORT": ("namq_10_gdp", {"freq": "Q", "na_item": "P7", "unit": "CLV20_MNAC", "s_adj": "NSA"}, "Q"),

    # HICP and components (monthly)
    "HICP": ("prc_hicp_midx", {"unit": "I15", "coicop": "CP00", "freq": "M"}, "M"),
    "HICP_Core": ("prc_hicp_midx", {"unit": "I15", "coicop": "TOT_X_NRG_FOOD", "freq": "M"}, "M"),
    "HICP_Food": ("prc_hicp_midx", {"unit": "I15", "coicop": "CP01", "freq": "M"}, "M"),
    "HICP_Energy": ("prc_hicp_midx", {"unit": "I15", "coicop": "NRG", "freq": "M"}, "M"),
    "HICP_NEIG": ("prc_hicp_midx", {"unit": "I15", "coicop": "IGD_NNRG", "freq": "M"}, "M"),
    "HICP_Services": ("prc_hicp_midx", {"unit": "I15", "coicop": "SERV", "freq": "M"}, "M"),

    # Deficit/Surplus % PIL (annual)
    "Deficit_GDP": ("gov_10dd_edpt1", {"na_item": "B9", "sector":"S13", "freq": "A","unit": "PC_GDP"}, "A"),
    "Debt_GDP": ("gov_10dd_edpt1", {"na_item": "GD", "sector":"S13", "freq": "A","unit": "PC_GDP"}, "A"),
    "CurrentAccountBalance_GDP": ("bop_gdp6_q", {"bop_item":"CA", "partner": "WRL_REST", "S_ADJ":"NSA", "stk_flow": "BAL","freq":"Q", "unit": "PC_GDP"}, "Q"),

    # Sentiment / confidence (monthly)
    "ESI": ("teibs010", {"indic": "BS-ESI-I", "s_adj": "SA", "freq": "M"}, "M"),
    "Construction_Confidence": ("teibs020", {"indic": "BS-CCI-BAL", "s_adj": "SA", "freq": "M"}, "M"),
    "Industrial_Confidence": ("teibs020", {"indic": "BS-ICI-BAL", "s_adj": "SA", "freq": "M"}, "M"),
    "Retail_Confidence": ("teibs020", {"indic": "BS-RCI-BAL", "s_adj": "SA", "freq": "M"}, "M"),
    "Consumer_Confidence": ("teibs020", {"indic": "BS-CSMCI-BAL", "s_adj": "SA", "freq": "M"}, "M"),
    "Services_Confidence": ("teibs020", {"indic": "BS-SCI-BAL", "s_adj": "SA", "freq": "M"}, "M"),

    # Industrial Production (monthly)
    "IndustrialProduction": ("sts_inpr_m", {"indic_bt": "PRD", "s_adj": "SCA", "nace_r2": "B-D", "freq": "M", "unit": "I21"}, "M"),
    "IndustrialProduction_IntermediateGoods": ("sts_inpr_m", {"indic_bt": "PRD", "s_adj": "SCA", "nace_r2": "MIG_ING", "freq": "M", "unit": "I21"}, "M"),
    "IndustrialProduction_EnergyexElectricity": ("sts_inpr_m", {"indic_bt": "PRD", "s_adj": "SCA", "nace_r2": "MIG_NRG_X_E", "freq": "M", "unit": "I21"}, "M"),
    "IndustrialProduction_CapitalGoods": ("sts_inpr_m", {"indic_bt": "PRD", "s_adj": "SCA", "nace_r2": "MIG_CAG", "freq": "M", "unit": "I21"}, "M"),
    "IndustrialProduction_DurableConsumerGoods": ("sts_inpr_m", {"indic_bt": "PRD", "s_adj": "SCA", "nace_r2": "MIG_DCOG", "freq": "M", "unit": "I21"}, "M"),
    "IndustrialProduction_NonDurableConsumerGoods": ("sts_inpr_m", {"indic_bt": "PRD", "s_adj": "SCA", "nace_r2": "MIG_NDCOG", "freq": "M", "unit": "I21"}, "M"),

    # Retail Sales (monthly)
    "RetailSales": ("sts_trtu_m", {"indic_bt": "VOL_SLS", "s_adj": "SCA", "nace_r2": "G47", "freq": "M", "unit": "I21"}, "M"),
    "RetailSales_Food": ("sts_trtu_m", {"indic_bt": "VOL_SLS", "s_adj": "SCA", "nace_r2": "G47_FOOD", "freq": "M", "unit": "I21"}, "M"),
    "RetailSales_exFood": ("sts_trtu_m", {"indic_bt": "VOL_SLS", "s_adj": "SCA", "nace_r2": "G47_NFOOD_X_G473", "freq": "M", "unit": "I21"}, "M"),

    # Unemployment rate (monthly)
    "Unemployment": ("une_rt_m", {"sex": "T", "age": "TOTAL", "unit": "PC_ACT", "freq": "M"}, "M"),
}
