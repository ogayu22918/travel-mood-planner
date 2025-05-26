-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create areas table
CREATE TABLE IF NOT EXISTS areas (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_en VARCHAR(100),
    prefecture VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    boundary GEOGRAPHY(POLYGON, 4326),
    center_point GEOGRAPHY(POINT, 4326) NOT NULL,
    characteristics JSONB DEFAULT '{}',
    transport_hub JSONB DEFAULT '{}',
    seasonal_info JSONB DEFAULT '{}',
    popularity_rank FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create spots table
CREATE TABLE IF NOT EXISTS spots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    google_place_id VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    area_id VARCHAR(50) REFERENCES areas(id),
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    price_range INTEGER CHECK (price_range BETWEEN 1 AND 5),
    price_info JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    contact_info JSONB DEFAULT '{}',
    business_hours JSONB DEFAULT '{}',
    popularity_score FLOAT DEFAULT 0.5,
    uniqueness_score FLOAT DEFAULT 0.5,
    family_friendly_score FLOAT,
    accessibility_score FLOAT,
    avg_duration_min INTEGER DEFAULT 60,
    min_duration_min INTEGER DEFAULT 30,
    max_duration_min INTEGER DEFAULT 180,
    weather_dependency VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create vectors table
CREATE TABLE IF NOT EXISTS vectors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    vector_type VARCHAR(50) DEFAULT 'description',
    embedding vector(1536) NOT NULL,
    text_source TEXT,
    model_version VARCHAR(50) DEFAULT 'text-embedding-ada-002',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_spots_location ON spots USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_areas_center ON areas USING GIST(center_point);
CREATE INDEX IF NOT EXISTS idx_vectors_embedding ON vectors USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
