import requests
import pandas as pd
import time
import json
from collections import defaultdict
from pathlib import Path

assets = Path("assets/")

API_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
HEADERS = {"Accept": "application/json"}
PAGE_SIZE = 100           # how many results per page request (max sensible)
REQUEST_DELAY = 1.0       # seconds between queries to be polite
TIMEOUT = 30              # requests timeout in seconds

gene_categories = {
    "Emerging Breast Cancer Target": ['CASP8'],
    "Lacks Breast Cancer Evidence": ['CDKN1A', 'VHL', 'BAX', 'NRAS', 'NF2', 'SRC', 'WT1', 'NTRK1'],
    "FDA-approved Breast Cancer Therapy": [
        'CDK4', 'FGFR1', 'ERBB2', 'KRAS', 'AKT1', 'MYC', 'BRCA1', 'TP53', 
        'PIK3CA', 'CDK6', 'BRCA2', 'EGFR', 'FGFR2'],
    "FDA-approved Other Indication": [
        'PTEN', 'CDKN2A', 'MDM2', 'HRAS', 'FOXO3', 'CCND1', 'BCL2', 'RB1',
        'NF1', 'ATR', 'SMAD4', 'CHEK2', 'TSC2', 'STK11', 'MET', 'NOTCH1',
        'ATM', 'NTRK2']
}

def search_studies_for_gene(gene_name, condition="Breast Cancer"):
    search_query = f'("{condition}") AND ({gene_name})'  # fixed formatting
    
    params = {
        "query.term": search_query,
        "pageSize": 100
    }
    
    studies = []
    try:
        response = requests.get(API_BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'studies' in data:
            studies = data['studies']
        else:
            print(f" -> No studies found for {gene_name}")

    except requests.exceptions.RequestException as e:
        print(f"Request error for {gene_name}: {e}")
        
    return studies

def extract_study_info(study):
    """
    Extract structured info from a study dict. Returns a dict with desired fields.
    """
    proto = study.get("protocolSection", {})
    ident = proto.get("identificationModule", {})
    nct_id = ident.get("nctId")
    title = ident.get("briefTitle") or ident.get("officialTitle")
    conditions = proto.get("conditionsModule", {}).get("conditions", [])
    # Add more extraction as needed (e.g., interventions, eligibility, contacts)
    interventions = proto.get("interventionsModule", {}).get("interventionList", {}).get("intervention", [])
    # Convert interventions to names if structured
    intervention_names = []
    for inv in interventions:
        name = inv.get("interventionName") or inv.get("name")
        if name:
            intervention_names.append(name)

    return {
        "nct_id": nct_id,
        "title": title,
        "conditions": conditions,
        "interventions": intervention_names,
        # keep the raw study for deeper inspection if needed
        "raw": study
    }

def analyze_gene_categories(*category_dicts, condition="Breast Cancer", sleep_between=REQUEST_DELAY):
    """
    Accepts multiple gene-category dicts, queries ClinicalTrials for each unique gene,
    and returns structured results and summaries.
    """
    # Combine and dedupe genes, but keep mapping of gene -> categories
    gene_to_categories = defaultdict(list)
    for cat_dict in category_dicts:
        for category, genes in cat_dict.items():
            for g in genes:
                gene_to_categories[g].append(category)

    unique_genes = list(gene_to_categories.keys())

    # storage
    study_rows = []   # list of rows: each row = one study hit for one gene
    summary_counts = defaultdict(dict)  # category -> gene -> count

    # Query each gene once
    for idx, gene in enumerate(unique_genes, 1):
        studies = search_studies_for_gene(gene, condition=condition)

        # Extract and store
        for st in studies:
            info = extract_study_info(st)
            study_rows.append({
                "gene": gene,
                "nct_id": info["nct_id"],
                "title": info["title"],
                "conditions": "; ".join(info["conditions"]),
                "interventions": "; ".join(info["interventions"])
            })

        # Fill per-category summary counts for this gene
        for cat in gene_to_categories[gene]:
            summary_counts[cat][gene] = len(studies)

        time.sleep(sleep_between)  # polite delay

    # Build DataFrames
    df_studies = pd.DataFrame(study_rows)
    # If no studies at all, ensure columns exist
    if df_studies.empty:
        df_studies = pd.DataFrame(columns=["gene", "nct_id", "title", "conditions", "interventions"])

    # Summary DF (one row per gene with categories flattened)
    summary_rows = []
    for cat, gene_counts in summary_counts.items():
        for gene, cnt in gene_counts.items():
            summary_rows.append({"category": cat, "gene": gene, "studies_found": cnt})
    df_summary = pd.DataFrame(summary_rows)

    return df_studies, df_summary

def assign_priority_category(df_summary):
    """
    Input:
        df_summary: DataFrame with rows {category, gene, studies_found}
    Returns:
        df_final: DataFrame with one row per gene:
                    {gene, assigned_category, studies_in_assigned_category}
        category_priority: list of categories ordered by total studies (desc)
    """

    # Compute global category priority by total studies (desc)
    cat_totals = df_summary.groupby('category')['studies_found'].sum().sort_values(ascending=False)
    category_priority = list(cat_totals.index)
    priority_index = {cat: i for i, cat in enumerate(category_priority)}

    # For each gene, find candidate categories and choose best by:
    #  a) lowest priority_index (i.e., highest priority)
    #  b) if same priority index among candidates (tie), pick category with highest per-gene studies_found
    #  c) if still tie, choose category by alphabetical order
    grouped = df_summary.groupby('gene')

    rows = []
    for gene, group in grouped:
        # group: rows for this gene across categories
        # annotate priority index to allow sorting
        group = group.copy()
        group['priority_idx'] = group['category'].map(priority_index)
        # Sort by (priority_idx asc, studies_found desc, category asc) and pick first
        group_sorted = group.sort_values(by=['priority_idx', 'studies_found', 'category'],
                                        ascending=[True, False, True])
        chosen = group_sorted.iloc[0]
        rows.append({
            'gene': gene,
            'category': chosen['category'],
            'studies': int(chosen['studies_found'])
        })

    df_final = pd.DataFrame(rows).sort_values(by='gene').reset_index(drop=True)
    return df_final, category_priority

BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def get_ensembl_id(gene_symbol):
    """
    Function to get the Ensembl ID for a given gene symbol.
    Uses the Open Targets search endpoint, which is more reliable for this purpose.
    """
    search_query = """
    query searchTarget($queryString: String!) {
        search(queryString: $queryString, entityNames: ["target"]) {
            hits {
                id
                entity
                object {
                    ... on Target {
                        approvedSymbol
                    }
                }
            }
        }
    }
    """
    variables = {"queryString": gene_symbol}
    payload = {
        'query': search_query,
        'variables': variables
    }

    try:
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Parse the response to find the Ensembl ID
        hits = data['data']['search']['hits']
        for hit in hits:
            if hit['entity'] == 'target' and hit['object']['approvedSymbol'] == gene_symbol:
                return hit['id']
    except Exception as e:
        print(f"Error finding Ensembl ID for {gene_symbol}: {e}")
    
    return None

# Your existing function for drug info
def query_open_targets_drugs(ensembl_id):
    """
    GraphQL query to get drugs targeting the gene using its Ensembl ID.
    """
    query = """
    query getKnownDrugs($ensemblId: String!)
    {
        target(ensemblId: $ensemblId)
        {
            id
            knownDrugs
            {
                rows
                {
                    drug
                    {
                        id
                        name
                    }
                    phase
                    status
                }
            }
        }
    }
    """
    variables = {"ensemblId": ensembl_id}
    payload = {
        'query': query,
        'variables': variables
    }

    try:
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data['data']['target'] is not None:
            drugs_info = data['data']['target']['knownDrugs']['rows']
            approved_drugs = [d['drug']['name'] for d in drugs_info if d['phase'] == 4]
            
            return ', '.join(set(approved_drugs)) if approved_drugs else 'No Specific Drug'
        else:
            return 'No Specific Drug'
    except Exception as e:
        print(f"Error querying drugs for {ensembl_id}: {e}")
        return 'No Specific Drug'

df_studies, df_summary = analyze_gene_categories(gene_categories, condition="Breast Cancer")
df_final, category_priority = assign_priority_category(df_summary)

# Load genes from your existing combined_df
genes = df_final['gene'].unique().tolist()

# Load DGIdb interactions file
interactions_path = assets / "interactions.tsv"
dgidb_df = pd.read_csv(interactions_path, sep="\t")

# Extract unique gene names that have interactions
targeted_genes = set(dgidb_df["gene_name"].dropna().str.upper())

# Create DGIdb status dataframe
dgidb_status_df = pd.DataFrame({
    'gene': genes,
    'DGIdb_Status': ['Targeted' if gene.upper() in targeted_genes else 'Not Targeted' 
                        for gene in genes]
})

# Process all genes to get Ensembl IDs
gene_ensembl_map = {}
for gene in genes:
    ensembl_id = get_ensembl_id(gene)
    if ensembl_id:
        gene_ensembl_map[gene] = ensembl_id
    else:
        gene_ensembl_map[gene] = None
    time.sleep(0.2)

# 1) Fetch all breast-cancer associated targets (single call)
BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"
DISEASE_EFO = "EFO_0000305"  # breast cancer
PAGE_SIZE = 500  # increase if you expect >500 associated targets

disease_query = """
query BreastCancerTargets($efoId: String!, $size: Int!)
{
    disease(efoId: $efoId)
    {
        associatedTargets(page: { index: 0, size: $size })
        {
            rows
            {
                target { approvedSymbol }
                score
            }
        }
    }
}
"""

resp = requests.post(
    BASE_URL,
    json={"query": disease_query, "variables": {"efoId": DISEASE_EFO, "size": PAGE_SIZE}},
    timeout=30
)
resp.raise_for_status()
data = resp.json()

# Defensive parsing
rows = []
try:
    rows = data["data"]["disease"]["associatedTargets"]["rows"]
except Exception:
    rows = []

# 2) Build a lookup dict mapping uppercase gene symbol -> score
#    If a symbol appears multiple times, keep the maximum score (or mean — choose what makes sense).
score_lookup = {}
for r in rows:
    targ = r.get("target") or {}
    symbol = targ.get("approvedSymbol")
    score = r.get("score")
    if symbol and score is not None:
        symu = symbol.upper()
        try:
            score_f = float(score)
        except (TypeError, ValueError):
            continue
        # keep the highest score if duplicates occur
        if symu in score_lookup:
            score_lookup[symu] = max(score_lookup[symu], score_f)
        else:
            score_lookup[symu] = score_f

score_lookup_df = pd.DataFrame(score_lookup, index=[0]).T.reset_index()
score_lookup_df.columns = ['gene', 'OpenTargets_Score']
score_lookup_df.to_csv(assets / "OpenTargets_Score.csv", index=False)

# Query both drug information and breast cancer scores
drug_map = {}
score_map = {}

for gene, ensembl_id in gene_ensembl_map.items():
    if ensembl_id:        
        # Get drug information
        drug_map[gene] = query_open_targets_drugs(ensembl_id)
        
        # Get breast cancer association score
        score_map[gene] = score_lookup.get(gene.upper(), 0.0)  

    else:
        drug_map[gene] = 'No Specific Drug'
        score_map[gene] = 0
    
    time.sleep(0.3)  # Slightly longer delay to respect API rate limits

# Create DataFrames for each data type
df_drugs = pd.DataFrame({
    'gene': list(drug_map.keys()),
    'FDA_Approved_Drug': list(drug_map.values())
})

df_scores = pd.DataFrame({
    'gene': list(score_map.keys()),
    'OpenTargets_Score': list(score_map.values())
})

# Merge all data into the final dataframe
enriched_df = df_final.merge(df_drugs, on='gene', how='left')
enriched_df = enriched_df.merge(dgidb_status_df, on='gene', how='left')
enriched_df = enriched_df.merge(df_scores, on='gene', how='left')

# Fill missing values
enriched_df['FDA_Approved_Drug'] = enriched_df['FDA_Approved_Drug'].fillna('No Specific Drug')
enriched_df['DGIdb_Status'] = enriched_df['DGIdb_Status'].fillna('Not Targeted')
enriched_df['OpenTargets_Score'] = enriched_df['OpenTargets_Score'].fillna(0)

# Add derived columns for analysis
enriched_df['Strong_BreastCancer_Support'] = enriched_df['OpenTargets_Score'] >= 0.5
enriched_df['Has_FDA_Drug'] = enriched_df['FDA_Approved_Drug'].apply(lambda x: "Yes" if x != 'No Specific Drug' else "No")

enriched_df.to_csv(assets / "Clinical_Trials_Summary.csv", index=False)