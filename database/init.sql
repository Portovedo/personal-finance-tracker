-- Personal Finance Tracker Database Initialization
-- This script creates the database and sets up initial configurations

-- Create the database if it doesn't exist (this won't work in most PostgreSQL setups)
-- CREATE DATABASE IF NOT EXISTS finance_tracker;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC';

-- Create indexes for better performance (these will be created by SQLAlchemy models)
-- Additional custom indexes can be added here

-- Initialize with default categories (this can also be handled by the application)
-- Categories will be inserted by the application on first run

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON DATABASE finance_tracker TO postgres;

-- Create search function for transaction categorization
CREATE OR REPLACE FUNCTION normalize_text(text_to_normalize TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN lower(trim(regexp_replace(text_to_normalize, '[^a-zA-Z0-9\s]', '', 'g')));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Create function for fuzzy string matching
CREATE OR REPLACE FUNCTION fuzzy_match(search_term TEXT, target_text TEXT)
RETURNS FLOAT AS $$
BEGIN
    RETURN similarity(normalize_text(search_term), normalize_text(target_text));
END;
$$ LANGUAGE plpgsql IMMUTABLE;