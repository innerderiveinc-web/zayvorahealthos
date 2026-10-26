class HybridSearchItemMobile {
  final String documentId;
  final String title;
  final String snippet;
  final String sourceOrganization;
  final String authorityTier;
  final String evidenceLevel;
  final String studyType;
  final double finalCompositeScore;
  final double bm25Score;
  final double vectorScore;
  final double graphScore;
  final double rrfScore;
  final List<dynamic> causalPaths;
  final List<String> meshTerms;
  final String whyThisResult;

  HybridSearchItemMobile({
    required this.documentId,
    required this.title,
    required this.snippet,
    required this.sourceOrganization,
    required this.authorityTier,
    required this.evidenceLevel,
    required this.studyType,
    required this.finalCompositeScore,
    required this.bm25Score,
    required this.vectorScore,
    required this.graphScore,
    required this.rrfScore,
    required this.causalPaths,
    required this.meshTerms,
    required this.whyThisResult,
  });

  factory HybridSearchItemMobile.fromJson(Map<String, dynamic> json) {
    final scores = (json['channel_scores'] as Map<String, dynamic>?) ?? {};
    final rawMesh = (json['mesh_terms'] as List<dynamic>?) ?? [];
    return HybridSearchItemMobile(
      documentId: json['document_id'] ?? '',
      title: json['title'] ?? '',
      snippet: json['snippet'] ?? '',
      sourceOrganization: json['source_organization'] ?? '',
      authorityTier: json['authority_tier'] ?? '',
      evidenceLevel: json['evidence_level'] ?? '',
      studyType: json['study_type'] ?? '',
      finalCompositeScore: (json['final_composite_score'] as num?)?.toDouble() ?? 0.0,
      bm25Score: (scores['bm25'] as num?)?.toDouble() ?? 0.0,
      vectorScore: (scores['neural_vector'] as num?)?.toDouble() ?? 0.0,
      graphScore: (scores['causal_graph'] as num?)?.toDouble() ?? 0.0,
      rrfScore: (scores['rrf_fusion'] as num?)?.toDouble() ?? 0.0,
      causalPaths: json['causal_paths'] ?? [],
      meshTerms: rawMesh.map((e) => e.toString()).toList(),
      whyThisResult: json['why_this_result'] ?? '',
    );
  }
}

class HybridSearchResultMobile {
  final String query;
  final String fusionAlgorithm;
  final int totalResults;
  final List<HybridSearchItemMobile> results;
  final List<String> expandedMeSHTerms;

  HybridSearchResultMobile({
    required this.query,
    required this.fusionAlgorithm,
    required this.totalResults,
    required this.results,
    required this.expandedMeSHTerms,
  });

  factory HybridSearchResultMobile.fromJson(Map<String, dynamic> json) {
    final rawResults = (json['results'] as List<dynamic>?) ?? [];
    final meshInfo = (json['mesh_expansion'] as Map<String, dynamic>?) ?? {};
    final rawExp = (meshInfo['expanded_terms'] as List<dynamic>?) ?? [];

    return HybridSearchResultMobile(
      query: json['query'] ?? '',
      fusionAlgorithm: json['fusion_algorithm'] ?? 'Weighted Reciprocal Rank Fusion (k=60)',
      totalResults: json['total_results'] ?? 0,
      results: rawResults
          .map((r) => HybridSearchItemMobile.fromJson(r as Map<String, dynamic>))
          .toList(),
      expandedMeSHTerms: rawExp.map((e) => e.toString()).toList(),
    );
  }

  factory HybridSearchResultMobile.offlineFallback(String query) {
    return HybridSearchResultMobile(
      query: query,
      fusionAlgorithm: 'Weighted Reciprocal Rank Fusion (k=60) [Offline Local Mode]',
      totalResults: 1,
      results: [
        HybridSearchItemMobile(
          documentId: 'PMID:18442638',
          title: 'Efficacy of Berberine in Patients with Type 2 Diabetes',
          snippet: 'Double-blind, randomized controlled trial evaluating Berberine in human metabolic control.',
          sourceOrganization: 'National Library of Medicine / PubMed',
          authorityTier: 'Tier B (Peer-Reviewed Curated Repository)',
          evidenceLevel: 'E6_controlled_clinical_evidence',
          studyType: 'Double-Blind Randomized Controlled Trial',
          finalCompositeScore: 0.94,
          bm25Score: 3.82,
          vectorScore: 0.89,
          graphScore: 1.0,
          rrfScore: 0.048,
          causalPaths: ['Berberine -> AMPK -> Gluconeogenesis Downregulation -> Blood Glucose Reduction'],
          meshTerms: ['Berberine', 'Diabetes Mellitus, Type 2', 'Blood Glucose'],
          whyThisResult: 'High concordance across lexical MeSH, neural cosine embedding, and verified causal pathway.',
        ),
      ],
      expandedMeSHTerms: ['Berberine', 'Daruharidra', 'Tree Turmeric', 'Type 2 Diabetes'],
    );
  }
}
