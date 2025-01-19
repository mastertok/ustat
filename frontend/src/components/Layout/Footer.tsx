import { Box, Container, Typography, Link, Grid } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Устат
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Образовательная платформа для профессионального роста
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Ссылки
            </Typography>
            <Link
              component={RouterLink}
              to="/courses"
              color="text.secondary"
              display="block"
            >
              Курсы
            </Link>
            <Link
              component={RouterLink}
              to="/teachers"
              color="text.secondary"
              display="block"
            >
              Преподаватели
            </Link>
            <Link
              component={RouterLink}
              to="/about"
              color="text.secondary"
              display="block"
            >
              О нас
            </Link>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Контакты
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Email: info@ustat.kg
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Телефон: +996 XXX XXX XXX
            </Typography>
          </Grid>
        </Grid>
        <Box mt={3}>
          <Typography variant="body2" color="text.secondary" align="center">
            {'© '}
            {new Date().getFullYear()}
            {' Устат. Все права защищены.'}
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
