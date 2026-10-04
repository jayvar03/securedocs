CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tenants (
    id         bigserial PRIMARY KEY,
    name       text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS users (
    id            bigserial PRIMARY KEY,
    tenant_id     bigint NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email         text NOT NULL UNIQUE,
    password_hash text NOT NULL,
    role          text NOT NULL CHECK (role IN ('admin', 'manager', 'employee')),
    department    text,
    created_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS users_tenant_idx ON users (tenant_id);

CREATE TABLE IF NOT EXISTS documents (
    id            bigserial PRIMARY KEY,
    tenant_id     bigint NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    title         text NOT NULL,
    filename      text NOT NULL,
    allowed_roles text[] NOT NULL,
    uploaded_by   bigint REFERENCES users(id) ON DELETE SET NULL,
    created_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS documents_tenant_idx ON documents (tenant_id);

CREATE TABLE IF NOT EXISTS chunks (
    id            bigserial PRIMARY KEY,
    document_id   bigint NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    tenant_id     bigint NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    allowed_roles text[] NOT NULL,
    chunk_index   integer NOT NULL,
    content       text NOT NULL,
    embedding     vector(384) NOT NULL,
    tsv           tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);
CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS chunks_tsv_idx ON chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS chunks_tenant_idx ON chunks (tenant_id);
CREATE INDEX IF NOT EXISTS chunks_document_idx ON chunks (document_id);

CREATE TABLE IF NOT EXISTS audit_logs (
    id         bigserial PRIMARY KEY,
    tenant_id  bigint NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id    bigint REFERENCES users(id) ON DELETE SET NULL,
    question   text NOT NULL,
    chunk_ids  bigint[] NOT NULL DEFAULT '{}',
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS audit_tenant_idx ON audit_logs (tenant_id, created_at DESC);
