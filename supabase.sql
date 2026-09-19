-- Villa Caetano Owner Dashboard - Supabase starter schema
-- Local version currently uses browser storage. This schema is ready for the later Supabase connection.
create extension if not exists pgcrypto;

create table if not exists public.dashboard_settings (
  id uuid primary key default gen_random_uuid(),
  manager_percent numeric(5,2) not null default 40,
  tds_percent numeric(5,2) not null default 10,
  gst_percent numeric(5,2) not null default 18,
  currency text not null default 'INR',
  updated_at timestamptz not null default now()
);

create table if not exists public.income_records (
  id uuid primary key default gen_random_uuid(),
  month date not null,
  gross_income numeric(14,2) not null,
  manager_percent numeric(5,2) not null default 40,
  tds_percent numeric(5,2) not null default 10,
  gst_percent numeric(5,2) not null default 18,
  note text,
  created_at timestamptz not null default now()
);

create table if not exists public.one_off_expenses (
  id uuid primary key default gen_random_uuid(),
  expense_date date not null,
  category text not null,
  description text,
  amount numeric(14,2) not null,
  created_at timestamptz not null default now()
);

create table if not exists public.monthly_billing (
  id uuid primary key default gen_random_uuid(),
  month date not null,
  category text not null,
  description text,
  amount numeric(14,2) not null,
  paid_by text not null default 'Property Manager',
  source text,
  created_at timestamptz not null default now()
);

create table if not exists public.issues (
  id uuid primary key default gen_random_uuid(),
  reported_date date not null,
  title text not null,
  description text,
  priority text not null default 'Medium',
  status text not null default 'Open',
  due_date date,
  created_at timestamptz not null default now()
);

-- User accounts should use Supabase Auth rather than storing passwords in a custom table.
-- A future profile table can reference auth.users(id) for display name and role.

-- One-off expenses are stored separately and affect owner cashflow. Monthly billing is
-- also stored separately so regular bills do not become owner one-off expenses.
-- Calculated fields are intentionally not stored; the app calculates GST, manager share,
-- owner share, TDS and net owner revenue from the rates stored with each income record.
