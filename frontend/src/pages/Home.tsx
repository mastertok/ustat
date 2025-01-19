import { useQuery } from '@tanstack/react-query';
import { Box, Container, Grid, Typography } from '@mui/material';
import Hero from '../components/Home/Hero';
import CategoryList from '../components/Home/CategoryList';
import TestimonialSection from '../components/Home/TestimonialSection';
import FeatureSection from '../components/Home/FeatureSection';
import CourseCard from '../components/Course/CourseCard';
import { api } from '../services/api';
import { Course } from '../types/api';

const Home = () => {
  const { data: popularCourses, isLoading } = useQuery<Course[]>({
    queryKey: ['popularCourses'],
    queryFn: async () => {
      const response = await api.get('/courses/courses/', {
        params: {
          ordering: '-rating',
          limit: 6,
        },
      });
      return response.data.results;
    },
  });

  return (
    <Box>
      <Hero />
      
      <CategoryList />

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
            {!isLoading &&
              popularCourses?.map((course) => (
                <Grid item key={course.id} xs={12} sm={6} md={4}>
                  <CourseCard course={course} />
                </Grid>
              ))}
          </Grid>
        </Container>
      </Box>

      <TestimonialSection />
      
      <FeatureSection />
    </Box>
  );
};

export default Home;
