import { Box, Button, Container, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Hero = () => {
  return (
    <Box
      sx={{
        bgcolor: 'background.paper',
        pt: 8,
        pb: 6,
        background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
        color: 'white',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Декоративные элементы */}
      <Box
        sx={{
          position: 'absolute',
          top: -100,
          right: -100,
          width: 400,
          height: 400,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: -50,
          left: -50,
          width: 200,
          height: 200,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
        }}
      />

      <Container maxWidth="md" sx={{ position: 'relative', zIndex: 1 }}>
        <Typography
          component="h1"
          variant="h2"
          align="center"
          gutterBottom
          sx={{ 
            fontWeight: 'bold',
            textShadow: '2px 2px 4px rgba(0,0,0,0.2)',
          }}
        >
          Устат - Ваш путь к знаниям
        </Typography>
        <Typography
          variant="h5"
          align="center"
          paragraph
          sx={{ 
            mb: 4,
            textShadow: '1px 1px 2px rgba(0,0,0,0.2)',
          }}
        >
          Онлайн-платформа для профессионального роста и развития.
          Учитесь у лучших преподавателей и развивайте свои навыки.
        </Typography>
        <Box
          sx={{
            display: 'flex',
            gap: 2,
            justifyContent: 'center',
          }}
        >
          <Button
            component={RouterLink}
            to="/register"
            variant="contained"
            color="secondary"
            size="large"
            sx={{
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              boxShadow: '0 4px 6px rgba(0,0,0,0.2)',
              '&:hover': {
                transform: 'translateY(-2px)',
                boxShadow: '0 6px 8px rgba(0,0,0,0.3)',
              },
              transition: 'all 0.2s',
            }}
          >
            Начать обучение
          </Button>
          <Button
            component={RouterLink}
            to="/courses"
            variant="outlined"
            size="large"
            sx={{
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              color: 'white',
              borderColor: 'white',
              '&:hover': {
                borderColor: 'white',
                bgcolor: 'rgba(255,255,255,0.1)',
              },
            }}
          >
            Смотреть курсы
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default Hero;
