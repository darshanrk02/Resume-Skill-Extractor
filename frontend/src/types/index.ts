// Resume data types
export interface Skill {
  name: string;
}

export interface Project {
  title: string;
  description: string;
}

export interface WorkExperience {
  company: string;
  position: string;
  start_date: string;
  end_date?: string;
  description: string;
  highlights?: string[];
}

export interface Education {
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date: string;
  gpa?: string;
}

export interface ContactInfo {
  name: string;
  title?: string;
  email: string;
  phone: string;
  location: string;
  linkedin?: string;
  github?: string;
  portfolio?: string;
}

export interface ResumeData {
  id?: string;
  contact_info: ContactInfo;
  summary: string;
  skills: Skill[];
  projects: Project[];
  experience: WorkExperience[];
  education: Education[];
  uploadDate?: string;
}

// Job Description types
export interface JobRequirement {
  skill: string;
  required: boolean;
  weight: number;
}

export interface JobDescription {
  id?: string;
  title: string;
  company?: string;
  description: string;
  requirements: JobRequirement[];
  createdDate?: string;
}

// Matching types
export interface SkillMatch {
  skill: string;
  matched: boolean;
  weight: number;
}

export interface ResumeMatch {
  id?: number;
  resumeId: string;
  name: string;
  title: string;
  matchPercentage: number;
  matchedSkills: SkillMatch[];
  missingSkills: SkillMatch[];
  recommendation: string;
  confidenceLevel: 'high' | 'medium' | 'low';
  analysis: string;
}

export interface MatchResult {
  id: number;
  resumeId: number;
  jobDescriptionId: number;
  score: number;
  matchedSkills: SkillMatch[];
  missingSkills: SkillMatch[];
  recommendation: string;
  analysis: string;
  createdDate: string;
}
