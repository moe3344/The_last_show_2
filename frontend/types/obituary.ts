export interface Obituary {
  id: string;
  user_id: string;
  name: string;
  birth_date: string;
  death_date: string;
  obituary_text: string;
  image_url?: string | null;
  audio_url?: string | null;
  is_public: boolean;
  created_at: string;
}

export interface ObituaryListResponse {
  obituaries: Obituary[];
  total: number;
}
