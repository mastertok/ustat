import { Box } from '@mui/material';
import Hero from '../components/Home/Hero';
import CategoryCarousel from '../components/Home/CategoryCarousel';
import NewCourses from '../components/Home/NewCourses';
import FeatureSection from '../components/Home/FeatureSection';
import TestimonialSection from '../components/Home/TestimonialSection';
import PartnersSection from '../components/Home/PartnersSection';

const Home = () => {
  return (
    <Box>
      {/* 1. Баннер */}
      <Hero />
      
      {/* 2. Категории курсов */}
      <CategoryCarousel />
      
      {/* 3. Новые курсы */}
      <NewCourses />
      
      {/* 4. Почему выбирают Устат */}
      <FeatureSection />
      
      {/* 5. Отзывы */}
      <TestimonialSection />
      
      {/* 6. Партнеры */}
      <PartnersSection />
    </Box>
  );
};

export default Home;
