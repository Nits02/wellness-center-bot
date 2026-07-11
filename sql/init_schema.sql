-- Run this in Supabase SQL Editor
-- Creates core tables for the Wellness Center POC

create extension if not exists pgcrypto;

create table if not exists public.users (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    phone text not null,
    created_at timestamptz not null default now()
);

create table if not exists public.appointments (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.users(id) on delete cascade,
    service_type text not null,
    appointment_time timestamptz not null,
    status text not null check (status in ('scheduled', 'completed', 'cancelled')),
    created_at timestamptz not null default now()
);

create table if not exists public.occupancy (
    id uuid primary key default gen_random_uuid(),
    "timestamp" timestamptz not null default now(),
    current_count integer not null check (current_count >= 0)
);

-- Helpful indexes
create index if not exists idx_appointments_user_id on public.appointments(user_id);
create index if not exists idx_appointments_time on public.appointments(appointment_time);
create index if not exists idx_occupancy_timestamp on public.occupancy("timestamp");
