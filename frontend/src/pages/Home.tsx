import { Box } from '@mui/material';
import Hero from '../components/Home/Hero';
import CategoryList from '../components/Home/CategoryList';
import PopularCourses from '../components/Home/PopularCourses';
import FeatureSection from '../components/Home/FeatureSection';
import TestimonialSection from '../components/Home/TestimonialSection';
import PartnersSection from '../components/Home/PartnersSection';

const Home = () => {
  return (
    <Box>
      {/* 1. Баннер */}
      <Hero />
      
      {/* 2. Категории курсов */}
      <CategoryList />
      
      {/* 3. Популярные курсы */}
      <PopularCourses />
      
      {/* 4. Особенности */}
      <FeatureSection />
      
      {/* 5. Отзывы */}
      <TestimonialSection />
      
      {/* 6. Партнеры */}
      <PartnersSection />
    </Box>
  );
};

export default Home;
