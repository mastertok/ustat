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

export interface Category {
  id: number;
  name: string;
  description: string;
  icon: string;
}

export interface Instructor {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface Review {
  id: number;
  user: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
  };
  course: {
    id: number;
    title: string;
  };
  rating: number;
  comment: string;
  created_at: string;
}

export interface Lesson {
  id: number;
  title: string;
  description: string;
  is_free: boolean;
  duration: string;
  order: number;
}

export interface Module {
  id: number;
  title: string;
  description: string;
  order: number;
  lessons: Lesson[];
  lessons_count: number;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  meta_title: string;
  meta_description: string;
  meta_keywords: string;
  image: string;
  preview_video: string;
  price: number;
  level: string;
  language: string;
  duration: string;
  category: Category;
  instructor: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
  };
  modules: Module[];
  reviews: Review[];
  is_favorite: boolean;
  is_enrolled: boolean;
  average_rating: number;
  created_at: string;
  updated_at: string;
}

export interface Partner {
  id: number;
  name: string;
  logo: string;
  website: string;
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

export interface Reply {
  id: number;
  review: Review;
  user: User;
  content: string;
  created_at: string;
  updated_at: string;
}
