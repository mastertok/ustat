import { Box, Card, CardContent, Typography, Container, Grid } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import {
  Code,
  Business,
  Brush,
  Language,
  Psychology,
  FitnessCenter,
  MusicNote,
  Camera,
} from '@mui/icons-material';

const categories = [
  { name: 'Программирование', icon: Code, color: '#2196f3' },
  { name: 'Бизнес', icon: Business, color: '#4caf50' },
  { name: 'Дизайн', icon: Brush, color: '#f44336' },
  { name: 'Языки', icon: Language, color: '#ff9800' },
  { name: 'Психология', icon: Psychology, color: '#9c27b0' },
  { name: 'Спорт', icon: FitnessCenter, color: '#795548' },
  { name: 'Музыка', icon: MusicNote, color: '#607d8b' },
  { name: 'Фотография', icon: Camera, color: '#00bcd4' },
];

const CategoryList = () => {
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
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <Grid item xs={6} sm={3} key={category.name}>
                <Card
                  component={RouterLink}
                  to={`/courses?category=${category.name}`}
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
                        bgcolor: `${category.color}15`,
                        color: category.color,
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
