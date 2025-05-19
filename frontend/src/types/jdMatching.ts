export interface JobDescription {
  text: string;
  title?: string;
  company?: string;
}

export interface SkillMatch {
  skill: string;
  similarity_score: number;
  is_required: boolean;
}

export interface MissingSkill {
  name: string;
  weight: number;
  reason: string;
}

export interface BackendMatch {
  match_percentage: number;
  skill_matches: SkillMatch[];
  missing_skills: MissingSkill[];
  explanation: string[];
  recommendation: string;
  confidence_score: number;
  resume_name?: string;
}

export interface UIResumeMatch {
  resumeId: string;
  name: string;
  title: string;
  matchPercentage: number;
  matchedSkills: {
    skill: string;
    matched: boolean;
    weight: number;
  }[];
  missingSkills: {
    skill: string;
    matched: boolean;
    weight: number;
  }[];
  recommendation: string;
  confidenceLevel: 'high' | 'medium' | 'low';
  analysis: string;
}

export interface ResumeUploadResponse {
  id: string;
  filename: string;
  size: number;
  content_type: string;
  upload_date: string;
}
