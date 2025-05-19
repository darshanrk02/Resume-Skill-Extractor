import { ResumeData, JobDescription, ResumeMatch } from '../types';

/**
 * Sample resume data for development and testing
 */
export const sampleResumeData: ResumeData = {
  contact_info: {
    name: 'John Doe',
    title: 'Senior Software Engineer',
    location: 'San Francisco, CA',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567'
  },
  summary: 'Passionate software engineer with 5+ years of experience in full-stack development. Proven track record in building scalable web applications using React, Node.js, and cloud infrastructure. Strong collaborator with cross-functional teams to deliver robust and maintainable code.',
  skills: [
    { name: 'React' },
    { name: 'Node.js' },
    { name: 'AWS' },
    { name: 'Docker' },
    { name: 'MongoDB' },
    { name: 'TypeScript' },
    { name: 'Python' },
    { name: 'JavaScript' }
  ],
  projects: [
    {
      title: 'TaskMaster Pro',
      description: 'A productivity web app built with React and Firebase that allows teams to track tasks, set deadlines, and monitor progress in real-time.'
    },
    {
      title: 'SmartCart AI',
      description: 'An AI-powered shopping assistant using Python and OpenCV to detect items and suggest optimized purchases based on user preferences.'
    },
    {
      title: 'Resume Skill Extractor',
      description: '• Developed a resume parser using NLP techniques to extract structured data\n• Implemented machine learning models for skill classification\n• Created a RESTful API for resume processing and data extraction'
    }
  ],
  experience: [
    {
      company: 'Tech Corp',
      position: 'Senior Software Engineer',
      start_date: '2020-01',
      end_date: '2023-05',
      description: 'Led a team of 5 developers in building a cloud-based analytics platform. Improved system performance by 40% through optimization of database queries and implementation of caching strategies.',
      highlights: [
        'Led development of microservices architecture',
        'Reduced deployment time by 60%',
        'Mentored junior developers'
      ]
    },
    {
      company: 'Startup Inc',
      position: 'Full Stack Developer',
      start_date: '2018-06',
      end_date: '2019-12',
      description: '• Led development of multiple web applications using React and Node.js\n• Implemented CI/CD pipelines reducing deployment time by 50%\n• Optimized database queries improving application performance by 30%',
      highlights: [
        'Implemented automated testing',
        'Reduced bug reports by 45%',
        'Improved user satisfaction scores'
      ]
    },
    {
      company: 'Tech Innovations Inc.',
      position: 'Senior Software Engineer',
      start_date: '2020-01',
      end_date: 'Present',
      description: 'Lead developer for cloud-based enterprise solutions. Implemented microservices architecture using Node.js and Docker.'
    },
    {
      company: 'DataViz Solutions',
      position: 'Software Engineer',
      start_date: '2017-06',
      end_date: '2019-12',
      description: 'Developed data visualization dashboards using React and D3.js. Optimized database queries for improved performance.'
    }
  ],
  education: [
    {
      institution: 'Stanford University',
      degree: 'B.S.',
      field_of_study: 'Computer Science',
      start_date: '2013',
      end_date: '2017',
      gpa: '3.8'
    }
  ]
};

/**
 * Sample job description data for development and testing
 */
export const sampleJobDescription: JobDescription = {
  title: 'Senior Frontend Developer',
  company: 'InnovateTech Solutions',
  description: 'We are looking for a Senior Frontend Developer to join our growing team. The ideal candidate will have strong experience with modern JavaScript frameworks, particularly React, and a passion for creating beautiful, responsive user interfaces. You will work closely with our design and backend teams to implement new features and improve existing ones.',
  requirements: [
    { skill: 'JavaScript', required: true, weight: 1 },
    { skill: 'React', required: true, weight: 1 },
    { skill: 'Redux', required: true, weight: 1 },
    { skill: 'TypeScript', required: true, weight: 1 },
    { skill: 'CSS/SCSS', required: true, weight: 1 },
    { skill: 'Responsive Design', required: true, weight: 1 },
    { skill: 'GraphQL', required: false, weight: 0.7 },
    { skill: 'Next.js', required: false, weight: 0.7 },
    { skill: 'Testing', required: false, weight: 0.8 },
    { skill: 'Communication', required: true, weight: 1 }
  ]
};

/**
 * Sample match data for development and testing
 */
export const sampleMatchData: ResumeMatch = {
  resumeId: '1',
  name: 'Jane Smith',
  title: 'Senior Frontend Developer',
  matchPercentage: 75,
  matchedSkills: [
    { skill: 'JavaScript', matched: true, weight: 1 },
    { skill: 'React', matched: true, weight: 1 },
    { skill: 'Redux', matched: true, weight: 1 },
    { skill: 'TypeScript', matched: true, weight: 1 },
    { skill: 'Communication', matched: true, weight: 1 }
  ],
  missingSkills: [
    { skill: 'GraphQL', matched: false, weight: 0.7 },
    { skill: 'Next.js', matched: false, weight: 0.7 },
    { skill: 'Testing', matched: false, weight: 0.8 }
  ],
  recommendation: 'Strong candidate - Interview recommended',
  confidenceLevel: 'high',
  analysis: 'Strong JavaScript and React skills align well with core requirements. GraphQL experience is missing but candidate has strong foundation in related technologies. TypeScript knowledge is present which is a required skill.'
};
