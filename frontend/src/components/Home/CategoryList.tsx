import { Box, Card, CardContent, Typography, Container, Grid, Skeleton } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api';
import { Category } from '../../types/api';
import {
  Code,
  Business,
  Brush,
  Language,
  Psychology,
  FitnessCenter,
  MusicNote,
  Camera,
  School,
} from '@mui/icons-material';

// Маппинг иконок для категорий
const categoryIcons: { [key: string]: any } = {
  'Программирование': Code,
  'Бизнес': Business,
  'Дизайн': Brush,
  'Языки': Language,
  'Психология': Psychology,
  'Спорт': FitnessCenter,
  'Музыка': MusicNote,
  'Фотография': Camera,
  'default': School,
};

const CategoryList = () => {
  const { data: categories, isLoading } = useQuery<Category[]>({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await api.get('/courses/categories/');
      return response.data.results;
    },
  });

  if (isLoading) {
    return (
      <Box sx={{ py: 8, bgcolor: 'background.default' }}>
        <Container>
          <Typography variant="h3" align="center" gutterBottom sx={{ mb: 6 }}>
            Категории курсов
          </Typography>
          <Grid container spacing={3}>
            {[1, 2, 3, 4].map((item) => (
              <Grid item xs={6} sm={3} key={item}>
                <Skeleton variant="rectangular" height={140} sx={{ borderRadius: 2 }} />
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ py: 8, bgcolor: 'background.default' }}>
      <Container>
        <Typography
          component="h2"
          variant="h3"
          align="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Категории курсов
        </Typography>
        <Grid container spacing={3}>
          {categories?.map((category) => {
            const Icon = categoryIcons[category.name] || categoryIcons.default;
            return (
              <Grid item xs={6} sm={3} key={category.id}>
                <Card
                  component={RouterLink}
                  to={`/courses?category=${category.slug}`}
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    textDecoration: 'none',
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                    },
                  }}
                >
                  <CardContent>
                    <Box
                      sx={{
                        width: 60,
                        height: 60,
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        bgcolor: 'primary.light',
                        color: 'primary.main',
                        mb: 2,
                        mx: 'auto',
                      }}
                    >
                      <Icon sx={{ fontSize: 30 }} />
                    </Box>
                    <Typography
                      variant="h6"
                      component="h3"
                      align="center"
                      color="text.primary"
                    >
                      {category.name}
                    </Typography>
                    <Typography
                      variant="body2"
                      align="center"
                      color="text.secondary"
                      sx={{
                        mt: 1,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                      }}
                    >
                      {category.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </Container>
    </Box>
  );
};

export default CategoryList;
