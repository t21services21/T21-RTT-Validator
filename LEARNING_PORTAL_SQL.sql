-- =====================================================
-- LEARNING PORTAL - DATABASE SETUP
-- =====================================================
-- Run this in Supabase SQL Editor to add Learning Portal
-- Features: Learning Materials, Video Library, Announcements
-- Date: October 15, 2025
-- =====================================================

-- =====================================================
-- PART 1: LEARNING MATERIALS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.learning_materials (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    file_url TEXT NOT NULL,
    file_name TEXT,
    file_type TEXT,
    file_size BIGINT,
    competency TEXT,
    week INTEGER DEFAULT 0,
    required BOOLEAN DEFAULT TRUE,
    visible_to_all BOOLEAN DEFAULT TRUE,
    uploaded_by TEXT,
    uploaded_date DATE DEFAULT CURRENT_DATE,
    download_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    deleted_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_learning_materials_category ON public.learning_materials(category);
CREATE INDEX IF NOT EXISTS idx_learning_materials_week ON public.learning_materials(week);
CREATE INDEX IF NOT EXISTS idx_learning_materials_competency ON public.learning_materials(competency);
CREATE INDEX IF NOT EXISTS idx_learning_materials_status ON public.learning_materials(status);

-- =====================================================
-- PART 2: MATERIAL DOWNLOADS TRACKING
-- =====================================================

CREATE TABLE IF NOT EXISTS public.material_downloads (
    id BIGSERIAL PRIMARY KEY,
    material_id BIGINT REFERENCES public.learning_materials(id),
    student_email TEXT NOT NULL,
    download_date TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_material_downloads_material ON public.material_downloads(material_id);
CREATE INDEX IF NOT EXISTS idx_material_downloads_student ON public.material_downloads(student_email);

-- =====================================================
-- PART 3: VIDEO LIBRARY
-- =====================================================

CREATE TABLE IF NOT EXISTS public.video_library (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    vimeo_url TEXT NOT NULL,
    vimeo_id TEXT NOT NULL,
    category TEXT,
    week INTEGER DEFAULT 0,
    duration_minutes INTEGER DEFAULT 0,
    competency TEXT,
    required BOOLEAN DEFAULT TRUE,
    visible_to_all BOOLEAN DEFAULT TRUE,
    uploaded_by TEXT,
    uploaded_date DATE DEFAULT CURRENT_DATE,
    view_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    deleted_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_video_library_category ON public.video_library(category);
CREATE INDEX IF NOT EXISTS idx_video_library_week ON public.video_library(week);
CREATE INDEX IF NOT EXISTS idx_video_library_competency ON public.video_library(competency);
CREATE INDEX IF NOT EXISTS idx_video_library_status ON public.video_library(status);

-- =====================================================
-- PART 4: VIDEO VIEWS TRACKING
-- =====================================================

CREATE TABLE IF NOT EXISTS public.video_views (
    id BIGSERIAL PRIMARY KEY,
    video_id BIGINT REFERENCES public.video_library(id),
    student_email TEXT NOT NULL,
    view_date TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_video_views_video ON public.video_views(video_id);
CREATE INDEX IF NOT EXISTS idx_video_views_student ON public.video_views(student_email);

-- =====================================================
-- PART 5: ANNOUNCEMENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.announcements (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    pinned BOOLEAN DEFAULT FALSE,
    visible_to_all BOOLEAN DEFAULT TRUE,
    posted_by TEXT,
    posted_date TIMESTAMPTZ DEFAULT NOW(),
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_announcements_category ON public.announcements(category);
CREATE INDEX IF NOT EXISTS idx_announcements_pinned ON public.announcements(pinned);
CREATE INDEX IF NOT EXISTS idx_announcements_status ON public.announcements(status);

-- =====================================================
-- PART 6: HELPER FUNCTIONS
-- =====================================================

-- Function to increment download count
CREATE OR REPLACE FUNCTION increment_download_count(material_id BIGINT)
RETURNS void AS $$
BEGIN
    UPDATE public.learning_materials
    SET download_count = download_count + 1
    WHERE id = material_id;
END;
$$ LANGUAGE plpgsql;

-- Function to increment video view count
CREATE OR REPLACE FUNCTION increment_video_view_count(video_id BIGINT)
RETURNS void AS $$
BEGIN
    UPDATE public.video_library
    SET view_count = view_count + 1
    WHERE id = video_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check all tables exist
SELECT 'learning_materials' as table_name, COUNT(*) as row_count FROM public.learning_materials
UNION ALL
SELECT 'material_downloads', COUNT(*) FROM public.material_downloads
UNION ALL
SELECT 'video_library', COUNT(*) FROM public.video_library
UNION ALL
SELECT 'video_views', COUNT(*) FROM public.video_views
UNION ALL
SELECT 'announcements', COUNT(*) FROM public.announcements;

-- =====================================================
-- SUCCESS MESSAGE
-- =====================================================

SELECT '✅ LEARNING PORTAL SETUP COMPLETE!' as status,
       'All tables and functions created successfully' as message,
       NOW() as completed_at;

-- =====================================================
-- NOTES
-- =====================================================
-- 
-- This script is idempotent - safe to run multiple times
-- It uses IF NOT EXISTS and CREATE OR REPLACE
-- 
-- Tables created:
-- 1. learning_materials - Upload and manage documents
-- 2. material_downloads - Track student downloads
-- 3. video_library - Vimeo video integration
-- 4. video_views - Track video views
-- 5. announcements - Post news and updates
--
-- Functions created:
-- 1. increment_download_count() - Auto-increment downloads
-- 2. increment_video_view_count() - Auto-increment views
--
-- =====================================================
