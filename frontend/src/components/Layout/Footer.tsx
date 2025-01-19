import { Box, Container, Typography, Link, Grid } from '@mui/material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
        py: 6,
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              О нас
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Устат - современная образовательная платформа, 
              предоставляющая качественные онлайн-курсы для 
              профессионального развития.
            </Typography>
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
            <Typography variant="body2" color="text.secondary">
              Адрес: г. Бишкек, ул. Примерная 123
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Ссылки
            </Typography>
            <Link href="#" color="text.secondary" display="block">
              Условия использования
            </Link>
            <Link href="#" color="text.secondary" display="block">
              Политика конфиденциальности
            </Link>
            <Link href="#" color="text.secondary" display="block">
              FAQ
            </Link>
          </Grid>
        </Grid>
        <Typography
          variant="body2"
          color="text.secondary"
          align="center"
          sx={{ mt: 4 }}
        >
          {'© '}
          {new Date().getFullYear()}
          {' Устат. Все права защищены.'}
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
