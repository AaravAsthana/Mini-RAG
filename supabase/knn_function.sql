-- knn_function.sql (repo copy)
CREATE OR REPLACE FUNCTION query_knn(query_embedding vector, match_count INT)
RETURNS TABLE (
  content TEXT,
  metadata JSONB,
  similarity DOUBLE PRECISION
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    d.content,
    d.metadata,
    1 - (d.embedding <=> query_embedding) AS similarity
  FROM documents_vector d
  ORDER BY d.embedding <=> query_embedding
  LIMIT match_count;
END;
$$ STABLE;
