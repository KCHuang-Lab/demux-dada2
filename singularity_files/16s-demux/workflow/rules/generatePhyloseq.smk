# Run filter2infer script on trimmed trimed reads.
rule filter2infer:
    input:
        "".join([config["trimdir"],"/{group}/lowReadsSummary.txt"])
    params:
        outdir="".join([config["outdir"], "{group}"]),
        trimdir="".join([config["trimdir"], "/{group}"])
    output:
        seqtab="".join([config["outdir"],"{group}/DADA2_output/seqtab_all.rds"])
    script:
        "../scripts/filter2infer.R"

# Run makeTree script.
rule makeTree:
    input:
        "".join([config["outdir"], "{group}/DADA2_output/seqtab_all.rds"])
    params:
        outdir="".join([config["outdir"], "{group}"])
    output:
        tree="".join([config["outdir"], "{group}/DADA2_output/dsvs_msa.tree"])
    script:
        "../scripts/makeTree.R"

# Run summary_taxa script.
rule summary_taxa:
    input:
        "".join([config["outdir"], "{group}/DADA2_output/seqtab_all.rds"])
    params:
        outdir="".join([config["outdir"], "{group}"])
    output:
        summary="".join([config["outdir"], "{group}/DADA2_output/L6_summary.txt"])
    script:
        "../scripts/summary_taxa.R"

# Run analyzeASVComposition script.
rule analyzeASVComposition:
    input:
        "".join([config["outdir"], "{group}/DADA2_output/dsvs_msa.tree"]),
        "".join([config["outdir"], "{group}/DADA2_output/ps_taxa.rds"])
    params:
        outdir="".join([config["outdir"], "{group}"]),
        metadata=config['samplesheet']
    output:
        ps="".join([config["outdir"], "{group}/DADA2_output/ps_all.rds"])
    script:
        "../scripts/analyzeASVComposition.R"
