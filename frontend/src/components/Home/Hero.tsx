import { Box, Button, Container, Typography, useTheme, useMediaQuery } from '@mui/material';
import { School, ArrowForward } from '@mui/icons-material';

const Hero = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));

  return (
    <Box
      sx={{
        bgcolor: 'background.paper',
        position: 'relative',
        pt: { xs: 4, sm: 6, md: 8 },
        pb: { xs: 8, sm: 12, md: 16 },
        overflow: 'hidden',
      }}
    >
      {/* Декоративные элементы */}
      <Box
        sx={{
          position: 'absolute',
          top: { xs: -100, md: -150 },
          right: { xs: -100, md: -150 },
          width: { xs: 200, md: 300 },
          height: { xs: 200, md: 300 },
          borderRadius: '50%',
          background: 'linear-gradient(45deg, #2196f3 30%, #21cbf3 90%)',
          opacity: 0.1,
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: { xs: -50, md: -100 },
          left: { xs: -50, md: -100 },
          width: { xs: 150, md: 200 },
          height: { xs: 150, md: 200 },
          borderRadius: '50%',
          background: 'linear-gradient(45deg, #ff4081 30%, #ff9100 90%)',
          opacity: 0.1,
        }}
      />

      <Container maxWidth="lg">
        <Box
          sx={{
            display: 'flex',
            flexDirection: { xs: 'column', md: 'row' },
            alignItems: 'center',
            gap: { xs: 4, md: 8 },
          }}
        >
          {/* Левая колонка с текстом */}
          <Box
            sx={{
              flex: 1,
              textAlign: { xs: 'center', md: 'left' },
              maxWidth: { xs: '100%', md: '60%' },
            }}
          >
            <Typography
              component="h1"
              variant={isMobile ? 'h3' : 'h2'}
              sx={{
                fontWeight: 'bold',
                mb: { xs: 2, md: 3 },
                fontSize: { xs: '2rem', sm: '2.5rem', md: '3.5rem' },
                lineHeight: { xs: 1.2, md: 1.1 },
              }}
            >
              Образование будущего уже сегодня
            </Typography>

            <Typography
              variant={isMobile ? 'body1' : 'h6'}
              color="text.secondary"
              sx={{
                mb: { xs: 3, md: 4 },
                fontSize: { xs: '1rem', sm: '1.1rem', md: '1.25rem' },
                maxWidth: { sm: '80%', md: '100%' },
                mx: { xs: 'auto', md: 0 },
              }}
            >
              Получайте качественные знания от лучших преподавателей в удобном для вас формате.
              Развивайтесь и достигайте новых высот вместе с нами!
            </Typography>

            <Box
              sx={{
                display: 'flex',
                flexDirection: { xs: 'column', sm: 'row' },
                gap: 2,
                justifyContent: { xs: 'center', md: 'flex-start' },
              }}
            >
              <Button
                variant="contained"
                size={isMobile ? 'medium' : 'large'}
                endIcon={<ArrowForward />}
                sx={{
                  px: { xs: 3, md: 4 },
                  py: { xs: 1, md: 1.5 },
                  borderRadius: 2,
                }}
              >
                Начать обучение
              </Button>
              <Button
                variant="outlined"
                size={isMobile ? 'medium' : 'large'}
                sx={{
                  px: { xs: 3, md: 4 },
                  py: { xs: 1, md: 1.5 },
                  borderRadius: 2,
                }}
              >
                Узнать больше
              </Button>
            </Box>
          </Box>

          {/* Правая колонка с иллюстрацией */}
          {!isTablet && (
            <Box
              sx={{
                flex: 1,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                position: 'relative',
              }}
            >
              <Box
                sx={{
                  width: '100%',
                  height: '100%',
                  minHeight: 400,
                  position: 'relative',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '80%',
                    height: '80%',
                    borderRadius: '50%',
                    background: 'linear-gradient(45deg, #e3f2fd 30%, #bbdefb 90%)',
                    opacity: 0.5,
                  },
                }}
              >
                <School
                  sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    fontSize: '15rem',
                    color: 'primary.main',
                    opacity: 0.8,
                  }}
                />
              </Box>
            </Box>
          )}
        </Box>
      </Container>
    </Box>
  );
};

export default Hero;
