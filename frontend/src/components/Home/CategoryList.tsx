import { Box, Card, CardContent, Typography, Grid, Skeleton } from '@mui/material';
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
  const { data: categories, isLoading, error } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      try {
        const response = await api.get('/api/v1/courses/categories/');
        return response.data.results;
      } catch (error) {
        console.error('Error fetching categories:', error);
        throw error;
      }
    },
  });

  if (error) {
    console.error('Error in CategoryList:', error);
    return (
      <Box sx={{ py: 8, bgcolor: 'background.default' }}>
        <Typography color="error" align="center">
          Ошибка при загрузке категорий
        </Typography>
      </Box>
    );
  }

  if (isLoading) {
    return (
      <Box sx={{ py: 8, bgcolor: 'background.default' }}>
        <Box
          sx={{
            width: '100%',
            maxWidth: '100vw',
            px: { xs: 2, sm: 4, md: 6, lg: 8 },
          }}
        >
          <Typography variant="h3" align="center" gutterBottom sx={{ mb: 6 }}>
            Категории курсов
          </Typography>
          <Grid 
            container 
            spacing={{ xs: 2, sm: 3, md: 4 }}
            sx={{
              width: '100%',
              margin: 0,
            }}
          >
            {[1, 2, 3, 4].map((item) => (
              <Grid item xs={6} sm={3} key={item}>
                <Skeleton 
                  variant="rectangular" 
                  height={140} 
                  sx={{ borderRadius: 2 }} 
                  data-testid="skeleton"
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ py: 8, bgcolor: 'background.default' }}>
      <Box
        sx={{
          width: '100%',
          maxWidth: '100vw',
          px: { xs: 2, sm: 4, md: 6, lg: 8 },
        }}
      >
        <Typography
          component="h2"
          variant="h3"
          align="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Категории курсов
        </Typography>
        <Grid 
          container 
          spacing={{ xs: 2, sm: 3, md: 4 }}
          sx={{
            width: '100%',
            margin: 0,
          }}
        >
          {categories?.map((category: Category) => {
            const Icon = categoryIcons[category.name] || categoryIcons.default;
            return (
              <Grid 
                item 
                xs={12} 
                sm={6} 
                md={4} 
                lg={3} 
                key={category.id}
              >
                <Card
                  component={RouterLink}
                  to={`/courses?category=${category.id}`}
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    textDecoration: 'none',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: (theme) => theme.shadows[4],
                    },
                  }}
                >
                  <CardContent sx={{ width: '100%', p: { xs: 2, sm: 3 } }}>
                    <Box
                      sx={{
                        width: { xs: 48, sm: 60 },
                        height: { xs: 48, sm: 60 },
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        bgcolor: 'primary.light',
                        color: 'primary.main',
                        mb: { xs: 1.5, sm: 2 },
                        mx: 'auto',
                      }}
                    >
                      <Icon sx={{ fontSize: { xs: 24, sm: 30 } }} />
                    </Box>
                    <Typography
                      variant="h6"
                      component="h3"
                      align="center"
                      color="text.primary"
                      sx={{
                        fontSize: { xs: '1.1rem', sm: '1.25rem' },
                        mb: { xs: 0.5, sm: 1 },
                      }}
                    >
                      {category.name}
                    </Typography>
                    <Typography
                      variant="body2"
                      align="center"
                      color="text.secondary"
                      sx={{
                        fontSize: { xs: '0.875rem', sm: '1rem' },
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
      </Box>
    </Box>
  );
};

export default CategoryList;
