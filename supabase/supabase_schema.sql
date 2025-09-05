-- supabase_schema.sql (repo copy)
CREATE EXTENSION IF NOT EXISTS vector;

-- old table (keep for audit) - ensure the repo shows both for clarity
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding FLOAT8[] NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- new table using pgvector
CREATE TABLE IF NOT EXISTS documents_vector (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(3072),
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);
