import { Box, Grid, Typography, Skeleton, useTheme, Container } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api';
import { Course } from '../../types/api';
import { CourseCard } from '../Course/CourseCard';

const PopularCourses = () => {
  const theme = useTheme();

  const { data: courses, isLoading } = useQuery<Course[]>({
    queryKey: ['popular-courses'],
    queryFn: async () => {
      const response = await api.get('/courses/popular/');
      return response.data.results;
    },
  });

  return (
    <Box
      sx={{
        py: 6,
        bgcolor: '#ffffff',
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ mb: 5, textAlign: 'center' }}>
          <Typography
            component="h2"
            variant="h3"
            sx={{
              fontWeight: 700,
              color: '#242424',
              fontSize: { xs: '2rem', md: '2.5rem' },
              mb: 2,
            }}
          >
            Популярные курсы
          </Typography>
          <Typography
            variant="subtitle1"
            sx={{
              color: 'text.secondary',
              maxWidth: '600px',
              mx: 'auto',
              fontSize: '1.1rem',
            }}
          >
            Самые популярные курсы на нашей платформе, выбранные тысячами студентов
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {isLoading
            ? Array.from(new Array(6)).map((_, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Skeleton
                    variant="rectangular"
                    width="100%"
                    height={300}
                    sx={{ borderRadius: 2 }}
                  />
                </Grid>
              ))
            : courses?.map((course) => (
                <Grid item xs={12} sm={6} md={4} key={course.id}>
                  <CourseCard course={course} />
                </Grid>
              ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default PopularCourses;
