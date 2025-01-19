import { Box, Container, Typography, Grid, useTheme } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api';
import { Course } from '../../types/api';
import CourseCard from '../Course/CourseCard';

const PopularCourses = () => {
  const theme = useTheme();

  const { data: courses } = useQuery<Course[]>({
    queryKey: ['popular-courses'],
    queryFn: async () => {
      const response = await api.get('/courses/popular/');
      return response.data.results;
    },
  });

  return (
    <Box
      sx={{
        py: 8,
        bgcolor: 'background.default',
      }}
    >
      <Container maxWidth="lg">
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
          {courses?.map((course) => (
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
