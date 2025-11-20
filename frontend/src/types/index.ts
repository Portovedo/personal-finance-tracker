// Common types used throughout the application

export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  timezone: string;
  currency: string;
  language: string;
  avatar_url?: string;
  email_notifications: boolean;
  push_notifications: boolean;
}

export interface Account {
  id: string;
  user_id: string;
  name: string;
  type: AccountType;
  status: AccountStatus;
  current_balance: string;
  available_balance?: string;
  credit_limit?: string;
  institution_name?: string;
  institution_code?: string;
  account_number_last4?: string;
  currency: string;
  description?: string;
  is_hidden: boolean;
  created_at: string;
  updated_at: string;
  closed_at?: string;
}

export interface Transaction {
  id: string;
  user_id: string;
  account_id: string;
  category_id?: string;
  amount: string;
  currency: string;
  description: string;
  notes?: string;
  transaction_date: string;
  posted_date?: string;
  type: TransactionType;
  status: TransactionStatus;
  is_transfer: boolean;
  transfer_pair_id?: string;
  destination_account_id?: string;
  external_id?: string;
  statement_id?: string;
  merchant_name?: string;
  merchant_category_code?: string;
  location?: string;
  city?: string;
  state?: string;
  country?: string;
  is_recurring: boolean;
  is_manual: boolean;
  category_confidence: string;
  is_categorization_manually_set: boolean;
  created_at: string;
  updated_at: string;
  // Relationships
  account?: Account;
  category?: Category;
}

export interface Category {
  id: string;
  user_id?: string;
  parent_category_id?: string;
  name: string;
  description?: string;
  color: string;
  icon?: string;
  type: CategoryType;
  is_system: boolean;
  is_active: boolean;
  monthly_budget?: string;
  alert_threshold: string;
  sort_order: string;
  created_at: string;
  updated_at: string;
  // Relationships
  parent_category?: Category;
  subcategories?: Category[];
  transactions?: Transaction[];
}

export interface Portfolio {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  portfolio_type: string;
  total_value: string;
  total_cost_basis: string;
  total_gain_loss: string;
  total_gain_loss_percentage: string;
  currency: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  // Relationships
  holdings?: PortfolioHolding[];
}

export interface PortfolioHolding {
  id: string;
  portfolio_id: string;
  symbol: string;
  security_name?: string;
  security_type?: SecurityType;
  asset_type: AssetType;
  exchange?: string;
  currency: string;
  quantity: string;
  avg_cost: string;
  current_price?: string;
  current_value: string;
  cost_basis: string;
  unrealized_gain_loss: string;
  unrealized_gain_loss_percentage: string;
  realized_gain_loss: string;
  dividend_yield?: string;
  annual_dividend_income: string;
  sector?: string;
  country?: string;
  market_cap_classification?: string;
  is_active: boolean;
  last_price_update?: string;
  data_source: string;
  created_at: string;
  updated_at: string;
}

export interface FileUpload {
  id: string;
  user_id: string;
  original_filename: string;
  stored_filename: string;
  file_path: string;
  file_type: FileType;
  mime_type?: string;
  file_size: number;
  processing_status: ProcessingStatus;
  processing_started_at?: string;
  processing_completed_at?: string;
  processing_error?: string;
  extracted_text?: string;
  extracted_data?: string;
  detected_account_type?: string;
  detected_institution?: string;
  confidence_score?: number;
  upload_source: string;
  is_duplicate: boolean;
  duplicate_of?: string;
  created_at: string;
  updated_at: string;
}

export interface Statement {
  id: string;
  user_id: string;
  file_upload_id?: string;
  statement_type: StatementType;
  institution_name?: string;
  account_number_last4?: string;
  period: StatementPeriod;
  start_date: string;
  end_date: string;
  statement_date?: string;
  opening_balance?: string;
  closing_balance?: string;
  total_debits?: string;
  total_credits?: string;
  net_change?: string;
  currency: string;
  transactions_extracted: number;
  transactions_imported: number;
  processing_confidence?: number;
  status: string;
  review_status: string;
  review_notes?: string;
  account_id?: string;
  is_duplicate: boolean;
  auto_categorized: boolean;
  created_at: string;
  updated_at: string;
  reviewed_at?: string;
  reviewed_by?: string;
}

// Enums
export type AccountType = 'checking' | 'savings' | 'credit_card' | 'investment' | 'loan' | 'mortgage' | 'other';
export type AccountStatus = 'active' | 'inactive' | 'closed' | 'frozen';
export type TransactionType = 'debit' | 'credit' | 'transfer_out' | 'transfer_in';
export type TransactionStatus = 'pending' | 'completed' | 'failed' | 'cancelled';
export type CategoryType = 'income' | 'expense' | 'transfer';
export type AssetType = 'stock' | 'etf' | 'bond' | 'mutual_fund' | 'cryptocurrency' | 'commodity' | 'real_estate' | 'cash' | 'other';
export type SecurityType = 'common_stock' | 'preferred_stock' | 'etf' | 'mutual_fund' | 'bond' | 'option' | 'future' | 'cryptocurrency' | 'reit';
export type FileType = 'pdf' | 'csv' | 'xlsx' | 'xls';
export type ProcessingStatus = 'uploaded' | 'processing' | 'processed' | 'failed' | 'review';
export type StatementType = 'bank_statement' | 'credit_card_statement' | 'investment_statement' | 'loan_statement' | 'brokerage_statement' | 'other';
export type StatementPeriod = 'monthly' | 'quarterly' | 'annually' | 'custom';

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: string[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Form types
export interface LoginFormData {
  email: string;
  password: string;
}

export interface RegisterFormData {
  email: string;
  password: string;
  full_name?: string;
}

export interface TransactionFormData {
  account_id: string;
  category_id?: string;
  amount: string;
  description: string;
  transaction_date: string;
  type: TransactionType;
  notes?: string;
  merchant_name?: string;
  location?: string;
}

export interface AccountFormData {
  name: string;
  type: AccountType;
  institution_name?: string;
  current_balance: string;
  currency: string;
  description?: string;
}

// Analytics types
export interface SpendingByCategory {
  category: string;
  amount: string;
  percentage: number;
  color: string;
  transaction_count: number;
}

export interface NetWorthOverTime {
  date: string;
  net_worth: string;
  assets: string;
  liabilities: string;
}

export interface MonthlySpending {
  month: string;
  income: string;
  expenses: string;
  net: string;
}

export interface PortfolioPerformance {
  period: string;
  return: string;
  return_percentage: string;
  volatility: string;
}

// Chart data types
export interface ChartDataPoint {
  x: string | number;
  y: number;
  label?: string;
}

export interface PieChartData {
  name: string;
  value: number;
  color: string;
}

// Filter and sort types
export interface TransactionFilters {
  account_ids?: string[];
  category_ids?: string[];
  type?: TransactionType;
  status?: TransactionStatus;
  date_from?: string;
  date_to?: string;
  amount_min?: string;
  amount_max?: string;
  search?: string;
}

export interface SortOption {
  field: string;
  direction: 'asc' | 'desc';
}

// Dashboard summary types
export interface DashboardSummary {
  net_worth: string;
  total_assets: string;
  total_liabilities: string;
  monthly_income: string;
  monthly_expenses: string;
  savings_rate: number;
  portfolio_value: string;
  portfolio_change: string;
  recent_transactions: Transaction[];
  spending_by_category: SpendingByCategory[];
  upcoming_bills: any[];
}