import { useState } from 'react';
import { Box, Container, Typography, Card, CardContent, Avatar, IconButton } from '@mui/material';
import { ArrowBack, ArrowForward } from '@mui/icons-material';

const testimonials = [
  {
    id: 1,
    name: 'Азамат Кадыров',
    role: 'Студент',
    avatar: 'https://source.unsplash.com/random/100x100/?man,1',
    text: 'Благодаря Устат я смог освоить программирование с нуля. Преподаватели очень внимательные и всегда готовы помочь.',
  },
  {
    id: 2,
    name: 'Айгуль Асанова',
    role: 'Дизайнер',
    avatar: 'https://source.unsplash.com/random/100x100/?woman,1',
    text: 'Отличная платформа для повышения квалификации. Курсы современные и актуальные, а формат обучения очень удобный.',
  },
  {
    id: 3,
    name: 'Бакыт Алиев',
    role: 'Предприниматель',
    avatar: 'https://source.unsplash.com/random/100x100/?man,2',
    text: 'Прошел курс по бизнес-планированию. Информация подается структурировано, много практических заданий.',
  },
  {
    id: 4,
    name: 'Жылдыз Токтоматова',
    role: 'Учитель английского',
    avatar: 'https://source.unsplash.com/random/100x100/?woman,2',
    text: 'Устат помог мне освоить новые методики преподавания. Теперь мои уроки стали еще интереснее для учеников.',
  },
];

const TestimonialSection = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const visibleTestimonials = testimonials.slice(currentIndex, currentIndex + 2);

  const handlePrev = () => {
    setCurrentIndex((prev) => Math.max(0, prev - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => Math.min(testimonials.length - 2, prev + 1));
  };

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
              gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
              gap: 4,
            }}
          >
            {visibleTestimonials.map((testimonial) => (
              <Card
                key={testimonial.id}
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  '&::before': {
                    content: '"""',
                    position: 'absolute',
                    top: 16,
                    left: 16,
                    fontSize: '4rem',
                    color: 'primary.main',
                    opacity: 0.1,
                    fontFamily: 'serif',
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1, pt: 4 }}>
                  <Typography
                    variant="body1"
                    paragraph
                    sx={{
                      mb: 4,
                      fontStyle: 'italic',
                      minHeight: 100,
                    }}
                  >
                    {testimonial.text}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Avatar
                      src={testimonial.avatar}
                      sx={{ width: 56, height: 56, mr: 2 }}
                    />
                    <Box>
                      <Typography variant="h6" component="div">
                        {testimonial.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {testimonial.role}
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
              gap: 2,
              mt: 4,
            }}
          >
            <IconButton
              onClick={handlePrev}
              disabled={currentIndex === 0}
              sx={{
                bgcolor: 'background.default',
                '&:hover': { bgcolor: 'grey.200' },
              }}
            >
              <ArrowBack />
            </IconButton>
            <IconButton
              onClick={handleNext}
              disabled={currentIndex >= testimonials.length - 2}
              sx={{
                bgcolor: 'background.default',
                '&:hover': { bgcolor: 'grey.200' },
              }}
            >
              <ArrowForward />
            </IconButton>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default TestimonialSection;
