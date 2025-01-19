export interface User {
  id: number;
  username: string;
  email: string;
  role: 'student' | 'teacher' | 'producer' | 'admin';
  first_name: string;
  last_name: string;
}

export interface TeacherProfile {
  id: number;
  user: User;
  experience_summary: string;
  education_summary: string;
  teaching_style: string;
  specializations: Specialization[];
  achievements: Achievement[];
  education: Education[];
  work_experience: WorkExperience[];
  rating: number;
  reviews_count: number;
  slug: string;
}

export interface ProducerProfile {
  id: number;
  user: User;
  company: string;
  portfolio: string;
  rating: number;
  reviews_count: number;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  teacher: TeacherProfile;
  category: Category;
  tags: Tag[];
  max_students: number;
  enrolled_students: number;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  language: string;
  course_type: 'free' | 'paid';
  price?: number;
  status: 'draft' | 'published' | 'archived';
  rating: number;
  reviews_count: number;
  created_at: string;
  updated_at: string;
}

export interface Module {
  id: number;
  course: Course;
  title: string;
  description: string;
  order: number;
}

export interface Lesson {
  id: number;
  module: Module;
  title: string;
  content: string;
  order: number;
  duration: number;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export interface Tag {
  id: number;
  name: string;
  slug: string;
}

export interface Specialization {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export interface Achievement {
  id: number;
  teacher: TeacherProfile;
  title: string;
  description: string;
  date: string;
}

export interface Education {
  id: number;
  teacher: TeacherProfile;
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date?: string;
}

export interface WorkExperience {
  id: number;
  teacher: TeacherProfile;
  company: string;
  position: string;
  description: string;
  start_date: string;
  end_date?: string;
}

export interface Review {
  id: number;
  course: Course;
  user: User;
  rating: number;
  comment: string;
  created_at: string;
  updated_at: string;
}

export interface Reply {
  id: number;
  review: Review;
  user: User;
  content: string;
  created_at: string;
  updated_at: string;
}
