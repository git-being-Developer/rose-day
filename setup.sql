-- Rose Day Database Schema
-- Run this in your Supabase SQL Editor

-- Create the roses table
CREATE TABLE IF NOT EXISTS roses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  to_name VARCHAR(100) NOT NULL,
  message TEXT NOT NULL,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  view_count INTEGER DEFAULT 0
);

-- Create an index on expires_at for faster queries
CREATE INDEX IF NOT EXISTS idx_roses_expires_at ON roses(expires_at);

-- Create an index on created_at for analytics
CREATE INDEX IF NOT EXISTS idx_roses_created_at ON roses(created_at);

-- Optional: Enable Row Level Security (RLS)
ALTER TABLE roses ENABLE ROW LEVEL SECURITY;

-- Allow public read access (anyone can view roses)
CREATE POLICY "Allow public read access" ON roses
  FOR SELECT
  USING (true);

-- Allow public insert (anyone can create roses)
CREATE POLICY "Allow public insert" ON roses
  FOR INSERT
  WITH CHECK (true);

-- Optional: Create a function to automatically delete expired roses
CREATE OR REPLACE FUNCTION delete_expired_roses()
RETURNS void AS $$
BEGIN
  DELETE FROM roses
  WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- Optional: Create a scheduled job to clean up expired roses (Supabase Pro feature)
-- You can also run this manually or via a cron job
-- SELECT cron.schedule('delete-expired-roses', '0 * * * *', 'SELECT delete_expired_roses()');
