-- ============================================================
-- Gateway Metal Detectors — Supabase Profiles Table Schema
-- Run this in your Supabase SQL Editor (Dashboard → SQL Editor)
-- ============================================================

-- Create the profiles table for user gear rig data
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    display_name TEXT,
    avatar_url TEXT,
    metal_detector TEXT,
    pinpointer TEXT,
    headphones TEXT,
    hand_digger TEXT,
    shovel TEXT,
    sand_scoop TEXT,
    finds_pouch TEXT,
    gloves TEXT,
    knee_pads TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Users can view their own profile
CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile"
    ON profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Auto-create a profile row when a new user signs up
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, display_name)
    VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users insert
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================================
-- Community Map Pins Schema
-- ============================================================

CREATE TABLE IF NOT EXISTS community_pins (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    item_name TEXT NOT NULL,
    age TEXT,
    composition TEXT,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE community_pins ENABLE ROW LEVEL SECURITY;

-- Anyone can read pins
CREATE POLICY "Anyone can view community pins"
    ON community_pins FOR SELECT
    USING (true);

-- Authenticated users can insert their own pins
CREATE POLICY "Authenticated users can insert pins"
    ON community_pins FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- ============================================================
-- Finds Storage Bucket Setup
-- ============================================================

-- Create the "finds" bucket
INSERT INTO storage.buckets (id, name, public) 
VALUES ('finds', 'finds', true)
ON CONFLICT (id) DO NOTHING;

-- Storage policies for the "finds" bucket
CREATE POLICY "Finds images are publicly accessible"
    ON storage.objects FOR SELECT
    USING (bucket_id = 'finds');

CREATE POLICY "Authenticated users can upload find images"
    ON storage.objects FOR INSERT
    WITH CHECK (bucket_id = 'finds' AND auth.role() = 'authenticated');
-- Create storage bucket for avatars (run separately if needed)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('avatars', 'avatars', true);
