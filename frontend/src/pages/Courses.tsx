import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Container,
  Grid,
  Typography,
  TextField,
  MenuItem,
  Pagination,
  Skeleton,
} from '@mui/material';
import { CourseCard } from '../components/Course/CourseCard';
import { api } from '../services/api';
import { Course } from '../types/api';
import SEO from '../components/Shared/SEO';

const Courses = () => {
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState('-created_at');
  const [searchQuery, setSearchQuery] = useState('');

  const { data, isLoading } = useQuery<{
    results: Course[];
    count: number;
  }>({
    queryKey: ['courses', page, sortBy, searchQuery],
    queryFn: async () => {
      const response = await api.get('/api/v1/courses/courses/', {
        params: {
          page,
          ordering: sortBy,
          search: searchQuery,
          page_size: 12,
        },
      });
      return response.data;
    },
  });

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  return (
    <Box sx={{ py: 4 }}>
      <SEO
        title="Все курсы | Устат"
        description="Изучайте новые навыки с нашими онлайн-курсами"
        keywords="курсы, обучение, онлайн образование"
      />
      
      <Container>
        <Typography variant="h3" component="h1" gutterBottom>
          Все курсы
        </Typography>

        <Box sx={{ mb: 4, display: 'flex', gap: 2 }}>
          <TextField
            label="Поиск курсов"
            variant="outlined"
            fullWidth
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <TextField
            select
            label="Сортировка"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="-created_at">Сначала новые</MenuItem>
            <MenuItem value="created_at">Сначала старые</MenuItem>
            <MenuItem value="-rating">По рейтингу</MenuItem>
            <MenuItem value="price">По цене (возр.)</MenuItem>
            <MenuItem value="-price">По цене (убыв.)</MenuItem>
          </TextField>
        </Box>

        <Grid container spacing={4}>
          {isLoading
            ? [...Array(12)].map((_, index) => (
                <Grid item key={index} xs={12} sm={6} md={4}>
                  <Skeleton variant="rectangular" height={320} />
                </Grid>
              ))
            : data?.results.map((course) => (
                <Grid item key={course.id} xs={12} sm={6} md={4}>
                  <CourseCard course={course} />
                </Grid>
              ))}
        </Grid>

        {data && (
          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
            <Pagination
              count={Math.ceil(data.count / 12)}
              page={page}
              onChange={handlePageChange}
              color="primary"
            />
          </Box>
        )}
      </Container>
    </Box>
  );
};

export default Courses;
