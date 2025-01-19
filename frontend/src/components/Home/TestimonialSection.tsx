import { useState } from 'react';
import { Box, Container, Typography, Card, CardContent, Avatar, IconButton, Skeleton } from '@mui/material';
import { ArrowBack, ArrowForward } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api';
import { Review } from '../../types/api';

const TestimonialSection = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  
  const { data: reviews, isLoading } = useQuery<Review[]>({
    queryKey: ['testimonials'],
    queryFn: async () => {
      const response = await api.get('/reviews/reviews/', {
        params: {
          rating__gte: 4, // Только хорошие отзывы
          ordering: '-created_at', // Сначала новые
          limit: 10,
        },
      });
      return response.data.results;
    },
  });

  const handlePrev = () => {
    setCurrentIndex((prev) => Math.max(0, prev - 1));
  };

  const handleNext = () => {
    if (!reviews) return;
    setCurrentIndex((prev) => Math.min(reviews.length - 2, prev + 1));
  };

  if (isLoading) {
    return (
      <Box sx={{ py: 8, bgcolor: 'background.paper' }}>
        <Container>
          <Typography variant="h3" align="center" gutterBottom sx={{ mb: 6 }}>
            Отзывы наших студентов
          </Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 4 }}>
            {[1, 2].map((item) => (
              <Skeleton key={item} variant="rectangular" height={200} sx={{ borderRadius: 2 }} />
            ))}
          </Box>
        </Container>
      </Box>
    );
  }

  const visibleTestimonials = reviews?.slice(currentIndex, currentIndex + 2);

  return (
    <Box sx={{ py: 8, bgcolor: 'background.paper' }}>
      <Container>
        <Typography
          component="h2"
          variant="h3"
          align="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Отзывы наших студентов
        </Typography>

        <Box sx={{ position: 'relative' }}>
          <Box
            sx={{
              display: 'grid',
              gridTemplateColumns: {
                xs: '1fr',
                md: '1fr 1fr',
              },
              gap: { xs: 3, sm: 4 },
            }}
          >
            {visibleTestimonials?.map((review) => (
              <Card
                key={review.id}
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  transition: 'all 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: (theme) => theme.shadows[4],
                  },
                  '&::before': {
                    content: '"""',
                    position: 'absolute',
                    top: { xs: 8, sm: 16 },
                    left: { xs: 8, sm: 16 },
                    fontSize: { xs: '3rem', sm: '4rem' },
                    color: 'primary.main',
                    opacity: 0.1,
                    fontFamily: 'serif',
                  },
                }}
              >
                <CardContent sx={{ 
                  flexGrow: 1, 
                  pt: { xs: 3, sm: 4 },
                  px: { xs: 2, sm: 3 },
                }}>
                  <Typography
                    variant="body1"
                    paragraph
                    sx={{
                      mb: { xs: 2, sm: 4 },
                      fontStyle: 'italic',
                      minHeight: { xs: 80, sm: 100 },
                      fontSize: { xs: '0.875rem', sm: '1rem' },
                      lineHeight: 1.6,
                    }}
                  >
                    {review.comment}
                  </Typography>
                  <Box sx={{ 
                    display: 'flex', 
                    alignItems: 'center',
                    flexDirection: { xs: 'column', sm: 'row' },
                    textAlign: { xs: 'center', sm: 'left' },
                    gap: { xs: 1, sm: 2 },
                  }}>
                    <Avatar
                      src={`https://source.unsplash.com/random/100x100/?person,${review.id}`}
                      sx={{ 
                        width: { xs: 48, sm: 56 }, 
                        height: { xs: 48, sm: 56 },
                        mb: { xs: 1, sm: 0 },
                      }}
                    />
                    <Box>
                      <Typography 
                        variant="h6" 
                        component="div"
                        sx={{
                          fontSize: { xs: '1rem', sm: '1.25rem' },
                          mb: { xs: 0.5, sm: 0 },
                        }}
                      >
                        {review.user.first_name} {review.user.last_name}
                      </Typography>
                      <Typography 
                        variant="body2" 
                        color="text.secondary"
                        sx={{
                          fontSize: { xs: '0.75rem', sm: '0.875rem' },
                        }}
                      >
                        {review.course.title}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>

          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              gap: { xs: 1, sm: 2 },
              mt: { xs: 2, sm: 4 },
            }}
          >
            <IconButton
              onClick={handlePrev}
              disabled={currentIndex === 0}
              sx={{
                bgcolor: 'background.default',
                '&:hover': { bgcolor: 'grey.200' },
                width: { xs: 40, sm: 48 },
                height: { xs: 40, sm: 48 },
              }}
            >
              <ArrowBack sx={{ fontSize: { xs: 20, sm: 24 } }} />
            </IconButton>
            <IconButton
              onClick={handleNext}
              disabled={!reviews || currentIndex >= reviews.length - 2}
              sx={{
                bgcolor: 'background.default',
                '&:hover': { bgcolor: 'grey.200' },
                width: { xs: 40, sm: 48 },
                height: { xs: 40, sm: 48 },
              }}
            >
              <ArrowForward sx={{ fontSize: { xs: 20, sm: 24 } }} />
            </IconButton>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default TestimonialSection;
