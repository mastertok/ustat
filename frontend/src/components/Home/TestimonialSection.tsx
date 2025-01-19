import { useState } from 'react';
import { Box, Container, Typography, Card, CardContent, Avatar, IconButton, CircularProgress, Alert } from '@mui/material';
import { ArrowBack, ArrowForward } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api';
import { Review } from '../../types/api';

const TestimonialSection = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  
  const { data: reviews, isLoading, error } = useQuery<Review[]>({
    queryKey: ['reviews'],
    queryFn: async () => {
      try {
        console.log('Fetching reviews from:', `${api.defaults.baseURL}/reviews/`);
        const response = await api.get('/reviews/', {
          params: {
            limit: 10,
            ordering: '-created_at'
          }
        });
        console.log('Full API Response:', response);
        console.log('Response Data:', response.data);
        console.log('Response Results:', response.data.results);
        return response.data.results || [];
      } catch (error) {
        console.error('Detailed Error:', error);
        if (api.isAxiosError(error)) {
          console.error('Response Data:', error.response?.data);
          console.error('Response Status:', error.response?.status);
        }
        throw error;
      }
    },
    refetchInterval: 30000,
    staleTime: 25000,
  });

  // Если данные загружаются
  if (isLoading) {
    return (
      <Box sx={{ py: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Box>
    );
  }

  // Если произошла ошибка
  if (error) {
    return (
      <Box sx={{ py: 4 }}>
        <Container>
          <Alert severity="error">
            Не удалось загрузить отзывы. Пожалуйста, попробуйте позже.
          </Alert>
        </Container>
      </Box>
    );
  }

  // Если нет отзывов
  if (!reviews || reviews.length === 0) {
    return (
      <Box sx={{ py: 4 }}>
        <Container>
          <Box
            sx={{
              textAlign: 'center',
              mb: 6,
              position: 'relative',
              '&::after': {
                content: '""',
                position: 'absolute',
                bottom: '-10px',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '100px',
                height: '3px',
                background: 'linear-gradient(45deg, #DB4337 30%, #FF9800 90%)',
                borderRadius: '2px',
              }
            }}
          >
            <Typography
              variant="h2"
              component="h2"
              sx={{
                fontSize: { xs: '2rem', md: '2.5rem' },
                fontWeight: 700,
                color: '#DB4337',
                textTransform: 'uppercase',
                letterSpacing: '2px',
                mb: 1,
                position: 'relative',
                display: 'inline-block',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  width: '120%',
                  height: '100%',
                  top: '0',
                  left: '-10%',
                  background: 'linear-gradient(45deg, rgba(219,67,55,0.1) 0%, rgba(255,152,0,0.1) 100%)',
                  transform: 'skew(-12deg)',
                  zIndex: -1,
                }
              }}
            >
              Отзывы наших студентов
            </Typography>
            <Typography
              variant="h6"
              sx={{
                color: 'text.secondary',
                fontSize: { xs: '1rem', md: '1.25rem' },
                fontWeight: 400,
                maxWidth: '800px',
                margin: '0 auto',
                mt: 2
              }}
            >
              Узнайте, что говорят о нас наши студенты
            </Typography>
          </Box>
          <Alert severity="info">
            Пока нет отзывов. Будьте первым, кто оставит отзыв о нашей платформе!
          </Alert>
        </Container>
      </Box>
    );
  }

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? reviews.length - 1 : prevIndex - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex === reviews.length - 1 ? 0 : prevIndex + 1));
  };

  return (
    <Box sx={{ py: 4, bgcolor: 'background.default' }}>
      <Container maxWidth="lg">
        <Typography
          variant="h6"
          component="h2"
          sx={{
            fontSize: { xs: '1rem', md: '1.125rem' },
            fontWeight: 500,
            color: 'text.secondary',
            mb: 3,
            ml: { xs: 2, md: 3 },
            textTransform: 'uppercase',
            letterSpacing: '0.5px',
            pb: 2,
            borderBottom: '1px solid',
            borderColor: 'divider',
          }}
        >
          Отзывы наших студентов
        </Typography>

        <Box sx={{ position: 'relative' }}>
          <Box
            sx={{
              display: 'flex',
              overflow: 'hidden',
              position: 'relative',
              minHeight: '200px',
            }}
          >
            {reviews.map((review, index) => (
              <Card
                key={index}
                sx={{
                  position: 'absolute',
                  width: '100%',
                  transition: 'transform 0.5s ease-in-out',
                  transform: `translateX(${(index - currentIndex) * 100}%)`,
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar
                      src={review.user?.avatar || ''}
                      alt={review.user?.full_name || 'User'}
                      sx={{ width: 56, height: 56, mr: 2 }}
                    />
                    <Box>
                      <Typography variant="h6" component="div">
                        {review.user?.full_name || 'Анонимный пользователь'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(review.created_at).toLocaleDateString('ru-RU')}
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="body1">{review.text}</Typography>
                </CardContent>
              </Card>
            ))}
          </Box>

          <IconButton
            onClick={handlePrev}
            sx={{
              position: 'absolute',
              left: 0,
              top: '50%',
              transform: 'translateY(-50%)',
              bgcolor: 'background.paper',
              '&:hover': { bgcolor: 'background.paper' },
            }}
          >
            <ArrowBack />
          </IconButton>

          <IconButton
            onClick={handleNext}
            sx={{
              position: 'absolute',
              right: 0,
              top: '50%',
              transform: 'translateY(-50%)',
              bgcolor: 'background.paper',
              '&:hover': { bgcolor: 'background.paper' },
            }}
          >
            <ArrowForward />
          </IconButton>
        </Box>
      </Container>
    </Box>
  );
};

export default TestimonialSection;
