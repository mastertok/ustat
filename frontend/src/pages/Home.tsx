import { useQuery } from '@tanstack/react-query';
import { Box, Container, Grid, Typography, Skeleton } from '@mui/material';
import Hero from '../components/Home/Hero';
import PopularCourses from '../components/Home/PopularCourses';
import CategoryList from '../components/Home/CategoryList';
import FeatureSection from '../components/Home/FeatureSection';
import TestimonialSection from '../components/Home/TestimonialSection';
import PartnersSection from '../components/Home/PartnersSection';
import { CourseCard } from '../components/Course/CourseCard';
import { api } from '../services/api';
import { Course } from '../types/api';

const Home = () => {
  const { data: popularCourses, isLoading } = useQuery<Course[]>({
    queryKey: ['popularCourses'],
    queryFn: async () => {
      const response = await api.get('/api/v1/courses/courses/popular/');
      return response.data;
    },
  });

  return (
    <Box>
      {/* 1. Баннер */}
      <Hero />
      
      {/* 2. Популярные курсы */}
      <Box sx={{ py: 8 }}>
        <Container>
          <Typography
            component="h2"
            variant="h3"
            align="center"
            gutterBottom
            sx={{ mb: 6 }}
          >
            Популярные курсы
          </Typography>

          <Grid container spacing={4}>
            {isLoading ? (
              // Показываем скелетон во время загрузки
              [...Array(6)].map((_, index) => (
                <Grid item key={index} xs={12} sm={6} md={4}>
                  <Skeleton 
                    variant="rectangular" 
                    height={300} 
                    sx={{ borderRadius: 2 }} 
                  />
                </Grid>
              ))
            ) : popularCourses?.map((course) => (
              <Grid item key={course.id} xs={12} sm={6} md={4}>
                <CourseCard course={course} />
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
      
      {/* 3. Категории курсов */}
      <CategoryList />
      
      {/* 4. Почему выбирают Устат */}
      <FeatureSection />
      
      {/* 5. Отзывы студентов */}
      <TestimonialSection />
      
      {/* 6. Партнеры */}
      <PartnersSection />
    </Box>
  );
};

export default Home;
